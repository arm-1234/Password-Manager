import base64
import hashlib
from cryptography.fernet import Fernet


class EncryptionManager:
    
    def __init__(self, master_password: str):
        self.key = self._derive_key(master_password)
        self.cipher = Fernet(self.key)
    
    @staticmethod
    def _derive_key(master_password: str) -> bytes:
        key = hashlib.sha256(master_password.encode()).digest()
        return base64.urlsafe_b64encode(key)
    
    def encrypt(self, data: str) -> bytes:
        return self.cipher.encrypt(data.encode())
    
    def decrypt(self, encrypted_data: bytes) -> str:
        return self.cipher.decrypt(encrypted_data).decode()
