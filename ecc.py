from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.fernet import Fernet
import base64

# Key Generation
def generate_keys():
    private_key = ec.generate_private_key(ec.SECP256R1())  # Choose an appropriate curve
    public_key = private_key.public_key()
    return private_key, public_key 

# ECDH Key Exchange
def shared_key(private_key, peer_public_key):
    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
    # Derive a symmetric key using HKDF
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)

    # Base64 encoding of the derived key
    encoded_key = base64.urlsafe_b64encode(derived_key)
    return encoded_key

# Encryption
def encrypt_message(message, symmetric_key):
    f = Fernet(symmetric_key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

# Decryption
def decrypt_message(encrypted_message, symmetric_key):
    f = Fernet(symmetric_key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()

# Example Usage
alice_private, alice_public = generate_keys()
bob_private, bob_public = generate_keys()

# Exchange public keys (simulated)
alice_shared_key = shared_key(alice_private, bob_public)
bob_shared_key = shared_key(bob_private, alice_public)

# Encryption by Alice
message = "Secret message"
ciphertext = encrypt_message(message, alice_shared_key)

# Decryption by Bob
decrypted_message = decrypt_message(ciphertext, bob_shared_key)
print("The decrypted message is:-",decrypted_message)
