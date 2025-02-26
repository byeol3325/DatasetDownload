import requests
import os
import hashlib
from tqdm import tqdm
import tarfile
import gzip
import json


# ////////////////////////////////// PLEASE CHECK THIS PARAMETERS //////////////////////////////////
# User credentials for NuScenes login
useremail = "your email"
password = "your password"

# Output directory where the dataset will be downloaded
output_dir = "your path"

# Region selection for NuScenes dataset ('us' or 'asia')
region = 'asia'
# ////////////////////////////////// PLEASE CHECK THIS PARAMETERS //////////////////////////////////

# List of NuScenes dataset files with their MD5 checksum for verification
download_files = {
    "v1.0-test_meta.tgz":"b0263f5c41b780a5a10ede2da99539eb",
    "v1.0-test_blobs.tgz":"e065445b6019ecc15c70ad9d99c47b33",
    "v1.0-trainval01_blobs.tgz":"cbf32d2ea6996fc599b32f724e7ce8f2",
    "v1.0-trainval02_blobs.tgz":"aeecea4878ec3831d316b382bb2f72da",
    "v1.0-trainval03_blobs.tgz":"595c29528351060f94c935e3aaf7b995",
    "v1.0-trainval04_blobs.tgz":"b55eae9b4aa786b478858a3fc92fb72d",
    "v1.0-trainval05_blobs.tgz":"1c815ed607a11be7446dcd4ba0e71ed0",
    "v1.0-trainval06_blobs.tgz":"7273eeea36e712be290472859063a678",
    "v1.0-trainval07_blobs.tgz":"46674d2b2b852b7a857d2c9a87fc755f",
    "v1.0-trainval08_blobs.tgz":"37524bd4edee2ab99678909334313adf",
    "v1.0-trainval09_blobs.tgz":"a7fcd6d9c0934e4052005aa0b84615c0",
    "v1.0-trainval10_blobs.tgz":"31e795f2c13f62533c727119b822d739",
    "v1.0-trainval_meta.tgz":"537d3954ec34e5bcb89a35d4f6fb0d4a",
}

# Function to authenticate user and retrieve access token
def login(username, password):
    headers = {
        "Content-Type": "application/x-amz-json-1.1",
        "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
    }

    # Prepare login request data
    data = json.dumps({
        "AuthFlow": "USER_PASSWORD_AUTH",
        "ClientId": "7fq5jvs5ffs1c50hd3toobb3b9",
        "AuthParameters": {
            "USERNAME": username,
            "PASSWORD": password
        },
        "ClientMetadata": {}
    })

    # Send authentication request
    response = requests.post(
        "https://cognito-idp.us-east-1.amazonaws.com/",
        headers=headers,
        data=data,
    )

    if response.status_code == 200:
        try:
            token = json.loads(response.content)["AuthenticationResult"]["IdToken"]
            return token  # Return authentication token
        except KeyError:
            print("Authentication failed. 'AuthenticationResult' not found in response.")
    else:
        print("Failed to login. Status code:", response.status_code)

    return None  # Return None if authentication fails

# Function to download files and verify their MD5 checksum
def download_file(url, save_file, md5):
    response = requests.get(url, stream=True)

    # Check if file already exists and verify MD5 checksum
    if os.path.exists(save_file):
        print(save_file, "has already been downloaded.")
        md5obj = hashlib.md5()
        with open(save_file, 'rb') as file:
            for chunk in file:
                md5obj.update(chunk)
        hash = md5obj.hexdigest()
        if hash != md5:
            print(save_file, "MD5 checksum failed, downloading again.")
        else:
            print(save_file, "MD5 checksum verified.")
            return save_file  # If checksum is valid, return file

    # Display progress bar while downloading
    file_size = int(response.headers.get('Content-Length', 0))
    progress_bar = tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024, desc=save_file, ascii=True)

    # Download file and calculate MD5 checksum
    md5obj = hashlib.md5()
    with open(save_file, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                md5obj.update(chunk)
                file.write(chunk)
                progress_bar.update(len(chunk))
    progress_bar.close()

    # Verify downloaded file integrity
    hash = md5obj.hexdigest()
    if hash != md5:
        print(save_file, "MD5 checksum failed.")
    else:
        print(save_file, "MD5 checksum verified.")

    return save_file

# Function to extract .tgz files
def extract_tgz_to_original_folder(tgz_file_path):
    original_folder = os.path.dirname(tgz_file_path)
    print(f"Extracting {tgz_file_path} to {original_folder}")

    with gzip.open(tgz_file_path, 'rb') as f_in:
        with tarfile.open(fileobj=f_in, mode='r') as tar:
            tar.extractall(original_folder)

# Function to extract .tar files
def extract_tar_to_original_folder(tar_file_path):
    original_folder = os.path.dirname(tar_file_path)
    print(f"Extracting {tar_file_path} to {original_folder}")

    with tarfile.open(tar_file_path, 'r') as tar:
        tar.extractall(original_folder)

# Main function to handle dataset download and extraction
def main():
    print("Logging in...")
    bearer_token = login(useremail, password)  # Authenticate user
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json',
    }

    print("Fetching download URLs...")
    download_data = {}
    for filename, md5 in download_files.items():
        api_url = f'https://o9k5xn5546.execute-api.us-east-1.amazonaws.com/v1/archives/v1.0/{filename}?region={region}&project=nuScenes'

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            print(filename, 'request successful.')
            download_url = response.json()['url']
            download_data[filename] = [download_url, os.path.join(output_dir, filename), md5]
        else:
            print(f'Request failed: {response.status_code}')
            print(response.text)

    print("Downloading files...")
    os.makedirs(output_dir, exist_ok=True)
    for output_name, (download_url, save_file, md5) in download_data.items():
        save_file = download_file(download_url, save_file, md5)
        download_data[output_name] = [download_url, save_file, md5]

    print("Extracting files...")
    for output_name, (download_url, save_file, md5) in download_data.items():
        if output_name.endswith(".tgz"):
            extract_tgz_to_original_folder(save_file)
        elif output_name.endswith(".tar"):
            extract_tar_to_original_folder(save_file)
        else:
            print("Unknown file type:", output_name)

    print("Download and extraction complete!")

# Execute the main function
if __name__ == "__main__":
    main()
