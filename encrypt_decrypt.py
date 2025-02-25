import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEYS_DIR = "keys"
PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, "private_key.pem")
PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, "public_key.pem")

def generate_rsa_keys():
    """Generate or load RSA keys from the 'keys' directory."""
    if not os.path.exists(KEYS_DIR):
        os.makedirs(KEYS_DIR)

    if os.path.exists(PRIVATE_KEY_PATH) and os.path.exists(PUBLIC_KEY_PATH):
        print("RSA keys already exist. Loading existing keys...")

        with open(PRIVATE_KEY_PATH, "rb") as priv_file:
            private_key = serialization.load_pem_private_key(
                priv_file.read(),
                password=None
            )

        with open(PUBLIC_KEY_PATH, "rb") as pub_file:
            public_key = serialization.load_pem_public_key(pub_file.read())

        return private_key, public_key

    print("Generating new RSA keys...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    with open(PRIVATE_KEY_PATH, "wb") as priv_file:
        priv_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    with open(PUBLIC_KEY_PATH, "wb") as pub_file:
        pub_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    print("RSA keys generated and saved successfully.")
    return private_key, public_key

def encrypt_file(data, public_key):
    """Encrypt file data using RSA and AES hybrid encryption."""
    aes_key = os.urandom(32)  # Generate a random 256-bit AES key

    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    iv = os.urandom(16)  # Initialization vector for AES
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    pad_len = 16 - (len(data) % 16)
    padded_data = data + bytes([pad_len] * pad_len)

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return encrypted_aes_key + iv + encrypted_data  # Concatenate encrypted AES key + IV + encrypted file data

def decrypt_file(encrypted_data, private_key):
    """Decrypt file data using RSA and AES hybrid decryption."""
    encrypted_aes_key = encrypted_data[:256]  # First 256 bytes (RSA encrypted AES key)
    iv = encrypted_data[256:272]  # Next 16 bytes (AES IV)
    aes_encrypted_data = encrypted_data[272:]  # Remaining bytes (AES encrypted file data)

    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(aes_encrypted_data) + decryptor.finalize()

    pad_len = decrypted_data[-1]  # Last byte contains padding length
    return decrypted_data[:-pad_len]  # Remove padding and return original data
