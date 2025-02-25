====================================================

# Secure File Storage using Hybrid Cryptography

====================================================

A Streamlit-based web app that encrypts files using **Hybrid Cryptography** (AES + RSA) before uploading them to AWS S3. 
Users can securely download and decrypt files using their private keys.

----------------------------------------------------
🔹 Features:
----------------------------------------------------   

✅ End-to-End Encryption – Uses RSA (2048-bit) + AES for strong security.  
✅ Secure Cloud Storage – Upload encrypted files to AWS S3.  
✅ Hybrid Cryptography – AES encrypts files; RSA encrypts AES keys.  
✅ File Integrity – Files cannot be accessed without the private key.  
✅ User-Friendly UI – Built with Streamlit for ease of use.  

----------------------------------------------------
🔹  Installation Steps:
----------------------------------------------------
🔧 **Prerequisites**

1. Python 3.x  
2. AWS IAM credentials (Access Key & Secret Key)  
3. Dependencies from requirements.txt
4. Write your own access key, secret key, and bucket name from AWS console where you created S3 bucket in keys.env file. 
     
🚀 **Installation Steps:-**

# Clone the repository
```
git clone https://github.com/hetkumark/Secure-File-Storage.git
```
# Navigate to the project folder
```
cd Secure-File-Storage
```
# Install dependencies
```
pip install -r requirements.txt
```
# Run the Streamlit app
```
streamlit run app.py
```
----------------------------------------------------
🔹 How to Use:
----------------------------------------------------

1️⃣ **Upload & Encrypt a File**  
   - Select a file using the file uploader.  
   - The file will be encrypted and uploaded to **AWS S3**.  
   - A success message will confirm the upload.  

2️⃣ **Download & Decrypt a File**  
   - Enter the **original file name** (e.g., `document.pdf`).  
   - Click **Download & Decrypt** to retrieve the file.  
   - The decrypted file will be available for download.

----------------------------------------------------
🔹 Project Screenshots:
---------------------------------------------------- 

#### 1. Home Page.
![image](https://github.com/user-attachments/assets/08de9e73-8c8e-466a-9654-f0821da53ae7)


#### 2. File encrypted and uploaded successfully on Cloud.
![image](https://github.com/user-attachments/assets/2f01e1e1-f8d9-4cdd-b12e-7b027bfca2d6)

#### 3. Same file decrypted and ready to download in Local PC. 
![image](https://github.com/user-attachments/assets/4cf1d88b-4de6-455d-9ed9-4ada8119e366)


----------------------------------------------------
🔹 Important Notes:
----------------------------------------------------
📌 Ensure that AWS credentials are correctly set in environment variables:  
   - `AWS_ACCESS_KEY`  
   - `AWS_SECRET_KEY`  
   - `S3_BUCKET_NAME`  

📌 The system generates RSA keys automatically if they don't exist.  
📌 The `.enc` file stored in S3 is the encrypted version of your file.  
📌 The decrypted file is downloaded **without being saved locally**.  


