import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json

class DataEncryption:
    def __init__(self, secret_key=None):
        """Initialize encryption with a secret key or generate one"""
        if secret_key:
            self.secret_key = secret_key
        else:
            # Generate a key from environment variable or create a new one
            env_key = os.getenv('ENCRYPTION_KEY')
            if env_key:
                self.secret_key = env_key.encode()
            else:
                self.secret_key = Fernet.generate_key()
                print(f"Generated new encryption key: {self.secret_key.decode()}")
                print("Please set this as ENCRYPTION_KEY environment variable for production")
        
        self.cipher_suite = Fernet(self.secret_key)
    
    def encrypt_data(self, data):
        """Encrypt sensitive data"""
        try:
            if isinstance(data, dict):
                # Convert dict to JSON string then encrypt
                json_data = json.dumps(data)
                encrypted_data = self.cipher_suite.encrypt(json_data.encode())
                return base64.b64encode(encrypted_data).decode()
            elif isinstance(data, str):
                encrypted_data = self.cipher_suite.encrypt(data.encode())
                return base64.b64encode(encrypted_data).decode()
            else:
                # Convert to string and encrypt
                encrypted_data = self.cipher_suite.encrypt(str(data).encode())
                return base64.b64encode(encrypted_data).decode()
        except Exception as e:
            print(f"Encryption error: {e}")
            return None
    
    def decrypt_data(self, encrypted_data):
        """Decrypt sensitive data"""
        try:
            if not encrypted_data:
                return None
            
            # Decode from base64
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            decrypted_data = self.cipher_suite.decrypt(encrypted_bytes)
            
            # Try to parse as JSON first, if it fails return as string
            try:
                return json.loads(decrypted_data.decode())
            except json.JSONDecodeError:
                return decrypted_data.decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            return None
    
    def encrypt_user_data(self, user_data):
        """Encrypt specific user fields that contain sensitive information"""
        sensitive_fields = {
            'phone': user_data.get('phone'),
            'business_pancard': user_data.get('business_pancard'),
            'company_address': user_data.get('company_address'),
            'age': str(user_data.get('age')) if user_data.get('age') else None,
            'gender': user_data.get('gender')
        }
        
        encrypted_data = {}
        for field, value in sensitive_fields.items():
            if value:
                encrypted_data[field] = self.encrypt_data(value)
        
        return encrypted_data
    
    def decrypt_user_data(self, encrypted_user_data):
        """Decrypt user data fields and return all as strings"""
        decrypted_data = {}
        for field, encrypted_value in encrypted_user_data.items():
            if encrypted_value:
                val = self.decrypt_data(encrypted_value)
                if val is not None:
                    decrypted_data[field] = str(val)
        return decrypted_data

# Create a global encryption instance
encryption = DataEncryption()

def encrypt_field(value):
    """Helper function to encrypt a single field"""
    if value is None:
        return None
    return encryption.encrypt_data(value)

def decrypt_field(encrypted_value):
    """Helper function to decrypt a single field"""
    if encrypted_value is None:
        return None
    return encryption.decrypt_data(encrypted_value)

def encrypt_user_sensitive_data(user_data):
    """Encrypt sensitive user information"""
    return encryption.encrypt_user_data(user_data)

def decrypt_user_sensitive_data(encrypted_data):
    """Decrypt sensitive user information"""
    return encryption.decrypt_user_data(encrypted_data) 