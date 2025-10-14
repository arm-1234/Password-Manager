import json
import os
from datetime import datetime
from encryption import EncryptionManager


class PasswordManager:
    
    def __init__(self, master_password, storage_file="passwords.enc"):
        self.storage_file = storage_file
        self.encryption = EncryptionManager(master_password)
        self.passwords = {}
        self._load_passwords()
    
    def _load_passwords(self):
        if not os.path.exists(self.storage_file):
            self.passwords = {}
            return
        
        try:
            with open(self.storage_file, 'rb') as f:
                encrypted_data = f.read()
                if encrypted_data:
                    decrypted_json = self.encryption.decrypt(encrypted_data)
                    self.passwords = json.loads(decrypted_json)
        except Exception as e:
            raise ValueError(f"Failed to load passwords. Wrong master password or corrupted file: {e}")
    
    def _save_passwords(self):
        json_data = json.dumps(self.passwords, indent=2)
        encrypted_data = self.encryption.encrypt(json_data)
        
        with open(self.storage_file, 'wb') as f:
            f.write(encrypted_data)
    
    def add_password(self, service, username, password, notes=""):
        if service.lower() in self.passwords:
            return False
        
        self.passwords[service.lower()] = {
            'service': service,
            'username': username,
            'password': password,
            'notes': notes,
            'created_at': datetime.now().isoformat(),
            'modified_at': datetime.now().isoformat()
        }
        self._save_passwords()
        return True
    
    def get_password(self, service):
        return self.passwords.get(service.lower())
    
    def update_password(self, service, username=None, password=None, notes=None):
        if service.lower() not in self.passwords:
            return False
        
        entry = self.passwords[service.lower()]
        
        if username is not None:
            entry['username'] = username
        if password is not None:
            entry['password'] = password
        if notes is not None:
            entry['notes'] = notes
        
        entry['modified_at'] = datetime.now().isoformat()
        self._save_passwords()
        return True
    
    def delete_password(self, service):
        if service.lower() not in self.passwords:
            return False
        
        del self.passwords[service.lower()]
        self._save_passwords()
        return True
    
    def search_passwords(self, query):
        query_lower = query.lower()
        results = []
        
        for entry in self.passwords.values():
            if query_lower in entry['service'].lower() or query_lower in entry['username'].lower():
                results.append(entry)
        
        return results
    
    def list_all_services(self):
        return [entry['service'] for entry in self.passwords.values()]
    
    def get_all_passwords(self):
        return list(self.passwords.values())
