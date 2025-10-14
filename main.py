import os
import sys
import getpass
import pyperclip
from password_manager import PasswordManager
from password_generator import PasswordGenerator


class PasswordManagerCLI:
    
    def __init__(self):
        self.manager = None
        self.generator = PasswordGenerator()
    
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self):
        print("\n" + "="*60)
        print("SECURE PASSWORD MANAGER".center(60))
        print("="*60 + "\n")
    
    def authenticate(self):
        self.clear_screen()
        self.print_header()
        
        print("Welcome to Password Manager!\n")
        
        if not os.path.exists("passwords.enc"):
            print("First time setup - Create a master password")
            print("WARNING: Remember this password! You cannot recover it if lost.\n")
            
            while True:
                master_pass = getpass.getpass("Create master password: ")
                if len(master_pass) < 6:
                    print("ERROR: Password must be at least 6 characters long.\n")
                    continue
                
                confirm_pass = getpass.getpass("Confirm master password: ")
                
                if master_pass == confirm_pass:
                    self.manager = PasswordManager(master_pass)
                    print("\nMaster password set successfully!")
                    input("\nPress Enter to continue...")
                    return True
                else:
                    print("ERROR: Passwords don't match. Try again.\n")
        else:
            print("Enter your master password to unlock\n")
            
            attempts = 3
            while attempts > 0:
                master_pass = getpass.getpass("Master password: ")
                
                try:
                    self.manager = PasswordManager(master_pass)
                    print("\nAccess granted!")
                    input("\nPress Enter to continue...")
                    return True
                except ValueError:
                    attempts -= 1
                    if attempts > 0:
                        print(f"\nWrong password! {attempts} attempts remaining.\n")
                    else:
                        print("\nToo many failed attempts. Exiting for security.")
                        return False
    
    def show_menu(self):
        self.clear_screen()
        self.print_header()
        
        print("MAIN MENU\n")
        print("1. Add New Password")
        print("2. View Password")
        print("3. Update Password")
        print("4. Delete Password")
        print("5. List All Services")
        print("6. Search Passwords")
        print("7. Generate Strong Password")
        print("8. Exit")
        print("\n" + "-"*60)
    
    def add_password(self):
        self.clear_screen()
        self.print_header()
        print("ADD NEW PASSWORD\n")
        
        service = input("Service/Website name: ").strip()
        if not service:
            print("\nERROR: Service name cannot be empty!")
            input("\nPress Enter to continue...")
            return
        
        username = input("Username/Email: ").strip()
        
        print("\nPassword options:")
        print("1. Enter password manually")
        print("2. Generate strong password")
        choice = input("\nChoice (1-2): ").strip()
        
        if choice == "2":
            password = self.generator.generate()
            print(f"\nGenerated password: {password}")
            print("Password copied to clipboard!")
            try:
                pyperclip.copy(password)
            except:
                print("WARNING: Clipboard copy failed, but you can still see the password above.")
        else:
            password = getpass.getpass("Password: ")
        
        notes = input("Notes (optional): ").strip()
        
        if self.manager.add_password(service, username, password, notes):
            print(f"\nPassword for '{service}' added successfully!")
        else:
            print(f"\nERROR: Password for '{service}' already exists!")
        
        input("\nPress Enter to continue...")
    
    def view_password(self):
        self.clear_screen()
        self.print_header()
        print("VIEW PASSWORD\n")
        
        service = input("Service/Website name: ").strip()
        entry = self.manager.get_password(service)
        
        if entry:
            print("\n" + "="*60)
            print(f"Service:  {entry['service']}")
            print(f"Username: {entry['username']}")
            print(f"Password: {entry['password']}")
            if entry['notes']:
                print(f"Notes:    {entry['notes']}")
            print(f"Created:  {entry['created_at'][:19]}")
            print(f"Modified: {entry['modified_at'][:19]}")
            print("="*60)
            
            copy = input("\nCopy password to clipboard? (y/n): ").strip().lower()
            if copy == 'y':
                try:
                    pyperclip.copy(entry['password'])
                    print("Password copied to clipboard!")
                except:
                    print("WARNING: Clipboard copy failed.")
        else:
            print(f"\nNo password found for '{service}'")
        
        input("\nPress Enter to continue...")
    
    def update_password(self):
        self.clear_screen()
        self.print_header()
        print("UPDATE PASSWORD\n")
        
        service = input("Service/Website name: ").strip()
        entry = self.manager.get_password(service)
        
        if not entry:
            print(f"\n❌ No password found for '{service}'")
            input("\nPress Enter to continue...")
            return
        
        print(f"\nCurrent details for '{service}':")
        print(f"Username: {entry['username']}")
        print(f"Password: {entry['password']}")
        print(f"Notes: {entry['notes']}")
        
        print("\n(Press Enter to keep current value)")
        
        new_username = input(f"\nNew username [{entry['username']}]: ").strip()
        
        print("\nPassword options:")
        print("1. Enter new password manually")
        print("2. Generate strong password")
        print("3. Keep current password")
        choice = input("\nChoice (1-3): ").strip()
        
        new_password = None
        if choice == "1":
            new_password = getpass.getpass("New password: ")
        elif choice == "2":
            new_password = self.generator.generate()
            print(f"\nGenerated password: {new_password}")
            try:
                pyperclip.copy(new_password)
                print("Password copied to clipboard!")
            except:
                print("WARNING: Clipboard copy failed.")
        
        new_notes = input(f"\nNew notes [{entry['notes']}]: ").strip()
        
        username_to_update = new_username if new_username else None
        notes_to_update = new_notes if new_notes else None
        
        self.manager.update_password(
            service, 
            username=username_to_update,
            password=new_password,
            notes=notes_to_update
        )
        
        print(f"\nPassword for '{service}' updated successfully!")
        input("\nPress Enter to continue...")
    
    def delete_password(self):
        self.clear_screen()
        self.print_header()
        print("DELETE PASSWORD\n")
        
        service = input("Service/Website name: ").strip()
        entry = self.manager.get_password(service)
        
        if not entry:
            print(f"\nNo password found for '{service}'")
            input("\nPress Enter to continue...")
            return
        
        print(f"\nWARNING: Are you sure you want to delete the password for '{service}'?")
        confirm = input("Type 'yes' to confirm: ").strip().lower()
        
        if confirm == 'yes':
            self.manager.delete_password(service)
            print(f"\nPassword for '{service}' deleted successfully!")
        else:
            print("\nDeletion cancelled.")
        
        input("\nPress Enter to continue...")
    
    def list_services(self):
        self.clear_screen()
        self.print_header()
        print("ALL STORED SERVICES\n")
        
        services = self.manager.list_all_services()
        
        if not services:
            print("No passwords stored yet.")
        else:
            print(f"Total: {len(services)} service(s)\n")
            for i, service in enumerate(sorted(services), 1):
                print(f"{i}. {service}")
        
        input("\nPress Enter to continue...")
    
    def search_passwords(self):
        self.clear_screen()
        self.print_header()
        print("SEARCH PASSWORDS\n")
        
        query = input("Search query: ").strip()
        
        if not query:
            print("\nERROR: Search query cannot be empty!")
            input("\nPress Enter to continue...")
            return
        
        results = self.manager.search_passwords(query)
        
        if not results:
            print(f"\nNo passwords found matching '{query}'")
        else:
            print(f"\nFound {len(results)} result(s):\n")
            for i, entry in enumerate(results, 1):
                print(f"{i}. {entry['service']} ({entry['username']})")
        
        input("\nPress Enter to continue...")
    
    def generate_password_menu(self):
        self.clear_screen()
        self.print_header()
        print("GENERATE STRONG PASSWORD\n")
        
        try:
            length = int(input("Password length (default 16): ").strip() or "16")
            
            print("\nInclude:")
            use_upper = input("Uppercase letters? (Y/n): ").strip().lower() != 'n'
            use_lower = input("Lowercase letters? (Y/n): ").strip().lower() != 'n'
            use_digits = input("Digits? (Y/n): ").strip().lower() != 'n'
            use_symbols = input("Symbols? (Y/n): ").strip().lower() != 'n'
            
            password = self.generator.generate(
                length=length,
                use_uppercase=use_upper,
                use_lowercase=use_lower,
                use_digits=use_digits,
                use_symbols=use_symbols
            )
            
            print(f"\n{'='*60}")
            print(f"Generated Password: {password}")
            print(f"{'='*60}")
            
            try:
                pyperclip.copy(password)
                print("\nPassword copied to clipboard!")
            except:
                print("\nWARNING: Clipboard copy failed, but you can still see the password above.")
        
        except ValueError as e:
            print(f"\nError: {e}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        if not self.authenticate():
            return
        
        while True:
            self.show_menu()
            
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                self.add_password()
            elif choice == '2':
                self.view_password()
            elif choice == '3':
                self.update_password()
            elif choice == '4':
                self.delete_password()
            elif choice == '5':
                self.list_services()
            elif choice == '6':
                self.search_passwords()
            elif choice == '7':
                self.generate_password_menu()
            elif choice == '8':
                self.clear_screen()
                print("\nThank you for using Password Manager! Stay secure!\n")
                sys.exit(0)
            else:
                print("\nInvalid choice! Please select 1-8.")
                input("\nPress Enter to continue...")


def main():
    try:
        cli = PasswordManagerCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nExiting... Stay secure!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
