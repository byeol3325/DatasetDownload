# 📦 DatasetDownload  
This repository provides a simple Python script to **download and extract the entire NuScenes dataset**.  
You don't need to run multiple commands — just edit one file and run it! The script will handle everything, including verifying and extracting files.


## 🚗 **Nuscenes Dataset Download Guide**

### 🔧 **Step 1: Set Up Your Information**

Before running the script, you need to edit some settings in the `Download_NuScenes.py` file.  
Look for the section below and replace the placeholders with your own information:

```bash
# ////////////////////////////////// PLEASE CHECK THIS PARAMETERS //////////////////////////////////
useremail = "your email"           # Your NuScenes login email
password = "your password"         # Your NuScenes login password
output_dir = "your path"           # The folder path where the dataset will be saved
region = 'asia'                    # Choose the region: 'us' or 'asia'
# ////////////////////////////////// PLEASE CHECK THIS PARAMETERS //////////////////////////////////
```


### 💻 **Step 2: Run the Script. Just Type It!!!!**

After setting up your information, run the following command in your terminal or command prompt:

```bash
python Download_Nuscenes.py
✅ Log in to the NuScenes server using your email and password.
✅ Download all NuScenes dataset files to your specified folder.
✅ Verify the files using MD5 checksums to make sure the download is correct.
✅ Automatically extract the .tgz and .tar files — no manual unzipping needed!
```



### 🙏 **Acknowledge**

Special thanks to the open-source project that made this work possible:

[https://github.com/li-xl/nuscenes-download]



## 🚗 **KITTI Dataset Download Guide**

### 🔧 **Step 1: Set Up Your Information**

