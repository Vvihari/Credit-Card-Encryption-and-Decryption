from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

# Generate a random key and initialization vector (IV)
key = os.urandom(32)  # AES-256 requires a 32-byte key
iv = os.urandom(16)  # AES block size is 16 bytes

def encrypt(credit_card_number, key, iv):
    # Pad the credit card number to be a multiple of the block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(credit_card_number.encode()) + padder.finalize()

    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the padded data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data

def decrypt(encrypted_data, key, iv):
    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Unpad the decrypted data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data.decode()

# Get user input for the credit card number
credit_card_number = input("Enter your credit card number: ")

# Encrypt the credit card number
encrypted_data = encrypt(credit_card_number, key, iv)
print(f"Encrypted: {encrypted_data.hex()}")

# Decryption on user request
decrypt_request = input("Do you want to decrypt the credit card number? (y/n): ")
if decrypt_request.lower() == 'y':
    decrypted_data = decrypt(encrypted_data, key, iv)
    print(f"Decrypted: {decrypted_data}")
else:
    print("Decryption not requested.")
