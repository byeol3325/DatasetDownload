import os
import requests
import hashlib
from tqdm import tqdm
import zipfile

# ////////////////////////////////// PLEASE CHECK THIS PARAMETERS //////////////////////////////////
# Output directory where the dataset will be downloaded
output_dir = "your/path/to/save/kitti"  # 🔴 <== Set your download path.

# Select KITTI datasets to download (True/False)
datasets_to_download = {
    "data_object_image_2.zip": {
        "url": "https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip",
        "md5": "351c61aab5caa90eb126ace1d12e6fa2",
        "description": "Left color images (2D) of object data"
    },
    "data_object_label_2.zip": {
        "url": "https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_label_2.zip",
        "md5": "e03858159cab2d3f8f2c6ed83a0d29c7",
        "description": "Labels for object data (2D/3D)"
    },
    "data_object_velodyne.zip": {
        "url": "https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_velodyne.zip",
        "md5": "8f0e5eafcf9fd1e047105c9b3d022249",
        "description": "Velodyne point clouds (3D)"
    },
    "data_object_calib.zip": {
        "url": "https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_calib.zip",
        "md5": "d2946e815a27c5d1e25f1d4f8f62a5ee",
        "description": "Calibration files for object data"
    }
}
# ////////////////////////////////// PLEASE CHECK THIS PARAMETERS //////////////////////////////////


# 🔍 Function to verify MD5 checksum
def verify_md5(file_path, expected_md5):
    md5obj = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5obj.update(chunk)
    file_md5 = md5obj.hexdigest()
    return file_md5 == expected_md5


# 🌐 Function to download a file with progress bar
def download_file(url, output_file, expected_md5):
    if os.path.exists(output_file):
        print(f"[✔] {output_file} already exists.")
        if verify_md5(output_file, expected_md5):
            print(f"[🔒] MD5 checksum verified for {output_file}.")
            return output_file
        else:
            print(f"[⚠] MD5 mismatch for {output_file}. Re-downloading...")
            os.remove(output_file)

    response = requests.get(url, stream=True)
    file_size = int(response.headers.get('Content-Length', 0))

    progress = tqdm(total=file_size, unit='B', unit_scale=True, desc=output_file, ascii=True)
    with open(output_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                progress.update(len(chunk))
    progress.close()

    if verify_md5(output_file, expected_md5):
        print(f"[🔒] Download complete and MD5 verified for {output_file}.")
    else:
        raise Exception(f"[❌] MD5 verification failed for {output_file}.")

    return output_file


# 🗂️ Function to extract ZIP files
def extract_zip(file_path, extract_to):
    print(f"[📦] Extracting {file_path} to {extract_to} ...")
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"[✅] Extraction complete for {file_path}.")


# 🚀 Main function to download and extract KITTI dataset
def main():
    os.makedirs(output_dir, exist_ok=True)
    print(f"[🚀] Starting KITTI dataset download to {output_dir}\n")

    for filename, file_info in datasets_to_download.items():
        print(f"\n[🔄] Dataset: {filename} - {file_info['description']}")
        save_path = os.path.join(output_dir, filename)
        try:
            downloaded_file = download_file(file_info['url'], save_path, file_info['md5'])
            extract_zip(downloaded_file, output_dir)
        except Exception as e:
            print(str(e))
            continue

    print("\n🎉 [🏁] All selected KITTI datasets have been downloaded and extracted successfully!")


if __name__ == "__main__":
    main()
