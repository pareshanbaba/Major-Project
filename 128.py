from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import os

# Generate a 128-bit ECC private key
private_key = ec.generate_private_key(
    ec.SECP256R1(),
    default_backend()
)

# Extract the 128-bit private key bytes
private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Compute the 128-bit public key bytes
public_key = private_key.public_key()
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print(f"Private Key (128-bit): {private_key_bytes.hex()}")
print(f"Public Key (128-bit): {public_key_bytes.hex()}")