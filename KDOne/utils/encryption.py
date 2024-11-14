import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidKey


def decrypt(salt, key, data):
    try:
        # Derive AES key and IV using PBKDF2
        derived_key = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=48,
            salt=salt,
            iterations=5,
            backend=default_backend(),
        ).derive(key.encode("utf-8"))

        # Split the derived key into AES key and IV
        aes_key, iv = derived_key[:32], derived_key[32:48]

        # Initialize AES-CBC decryption
        cipher = Cipher(
            algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend()
        )
        decryptor = cipher.decryptor()

        # Perform decryption
        decrypted_data = decryptor.update(data) + decryptor.finalize()

        # Remove PKCS7 padding
        padding_len = decrypted_data[-1]
        decrypted_data = decrypted_data[:-padding_len]

        return decrypted_data
    except InvalidKey as e:
        print("Invalid Key:", e)
    except ValueError as e:
        print("Invalid Input:", e)
    except Exception as e:
        print("An error occurred during decryption:", e)


def encrypt(salt, key, data):
    try:
        # Derive AES key and IV using PBKDF2
        derived_key = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=48,
            salt=salt,
            iterations=5,
            backend=default_backend(),
        ).derive(key.encode("utf-8"))

        # Split the derived key into AES key and IV
        aes_key, iv = derived_key[:32], derived_key[32:48]

        # Initialize AES-CBC encryption
        cipher = Cipher(
            algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend()
        )
        encryptor = cipher.encryptor()

        # Apply PKCS7 padding
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        # Perform encryption
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        return encrypted_data
    except Exception as e:
        print("An error occurred during encryption:", e)


def decrypt_payload(key, payload):
    reversed_key = key[::-1]
    # use as salt
    salt = key[:4].encode()

    print("key:", key)
    print("reversed_key:", reversed_key)
    print("salt:", salt)

    decrypted_data = decrypt(salt, reversed_key, base64.b64decode(payload))

    return decrypted_data.decode("utf-8")


def encrypt_payload(key, data):
    reversed_key = key[::-1]
    # use as salt
    salt = key[:4].encode()

    print("key:", key)
    print("reversed_key:", reversed_key)
    print("salt:", salt)

    encrypted_data = encrypt(salt, reversed_key, data.encode("utf-8"))

    return base64.b64encode(encrypted_data).decode("utf-8")


def random_key():
    import random
    import string

    return "".join(random.choices(string.ascii_letters + string.digits, k=32))
