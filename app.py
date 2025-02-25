import streamlit as st
import boto3
import os
from encrypt_decrypt import encrypt_file, decrypt_file, generate_rsa_keys
from s3_utils import upload_to_s3, download_from_s3

# Initialize AWS S3 Client
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

if S3_BUCKET_NAME is None:
    st.error("S3_BUCKET_NAME environment variable not set!")  
    st.stop()  

page_bg_gradient = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #09203F, #537895);  /* Dark green to light green gradient */
    color: white;  /* Set default text color to white for better contrast */
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);  /* Hide Header */
}
[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #16222A, #3A6073); /* Dark blue gradient sidebar */
}
.stButton>button {
    background-color:rgb(0, 0, 0);  /* Stylish blue button */
    color: white;
    border-radius: 10px;
    padding: 10px;
}
</style>
"""
st.markdown(page_bg_gradient, unsafe_allow_html=True)
hide_anchor_css = """
<style>

h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
    display: none !important;
    visibility: hidden !important;
}
</style>
"""
st.markdown(hide_anchor_css, unsafe_allow_html=True)

st.title(" Secure Cloud Storage with Hybrid Cryptography")

PRIVATE_KEY, PUBLIC_KEY = generate_rsa_keys()

st.subheader(" Upload & Encrypt File")
uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "jpg", "png", "docx", "xlsx"])

if uploaded_file is not None:
    file_name = uploaded_file.name  
    file_bytes = uploaded_file.read()

    encrypted_data = encrypt_file(file_bytes, PUBLIC_KEY)

    st.success("File encrypted successfully!")

    try:
        upload_to_s3(S3_BUCKET_NAME, f"{file_name}.enc", encrypted_data)
        st.success(" Encrypted file securely uploaded to S3!")
    except Exception as e:
        st.error(f"Failed to upload file: {e}")

st.subheader(" Download & Decrypt File")
file_name = st.text_input("Enter file name to download (e.g., document.pdf):")

if st.button("Download & Decrypt"):
    if file_name:
        encrypted_file_key = f"{file_name}.enc"  # File stored in S3

        try:
            encrypted_data = download_from_s3(S3_BUCKET_NAME, encrypted_file_key)

            if encrypted_data:
                decrypted_data = decrypt_file(encrypted_data, PRIVATE_KEY)

                if decrypted_data:
                    st.success(" File decrypted successfully! Ready for download.")

                    st.download_button(" Download Decrypted File", decrypted_data, file_name)
                else:
                    st.error(" Decryption failed!")

            else:
                st.error(" Failed to download encrypted file from S3!")

        except Exception as e:
            st.error(f" Error downloading or decrypting file: {e}")

    else:
        st.error(" Please enter a valid file name!")
