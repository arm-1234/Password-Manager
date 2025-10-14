import random
import string


class PasswordGenerator:
    
    @staticmethod
    def generate(length=16, use_uppercase=True, use_lowercase=True, 
                 use_digits=True, use_symbols=True):
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
        
        char_pool = ""
        if use_uppercase:
            char_pool += string.ascii_uppercase
        if use_lowercase:
            char_pool += string.ascii_lowercase
        if use_digits:
            char_pool += string.digits
        if use_symbols:
            char_pool += string.punctuation
        
        if not char_pool:
            raise ValueError("At least one character type must be selected")
        
        password_chars = []
        
        if use_uppercase:
            password_chars.append(random.choice(string.ascii_uppercase))
        if use_lowercase:
            password_chars.append(random.choice(string.ascii_lowercase))
        if use_digits:
            password_chars.append(random.choice(string.digits))
        if use_symbols:
            password_chars.append(random.choice(string.punctuation))
        
        remaining_length = length - len(password_chars)
        password_chars.extend(random.choices(char_pool, k=remaining_length))
        
        random.shuffle(password_chars)
        
        return ''.join(password_chars)
    
    @staticmethod
    def generate_simple(length=12):
        return PasswordGenerator.generate(length, use_symbols=False)
