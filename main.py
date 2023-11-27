import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback
import os
import pandas as pd
from fake_data_generator import generate_fake_details

config_file_path = 'config.yaml'

def read_config(config_file_path):
    try:
        with open(config_file_path, 'r') as yaml_file:
            config_data = yaml.safe_load(yaml_file)
        return config_data
    except Exception as e:
        create_dummy_config(config_file_path)
        raise ValueError(f"Error reading configuration file: {e}")

def create_dummy_config(config_file_path):
    print("Configuration file not found. Creating a new one...")

    sample_config = {
        'CONFIG_FILE': 'CONFIG.xlsx',
        'LOG_FILE': 'log.txt',
        'DEBUG_LOG_LEVEL': 'DEBUG',
        'INFO_LOG_LEVEL': 'INFO',
        'MAX_RETRIES': 3,
        'DELAY_BETWEEN_RETRIES': 2,
        'PROXY_CHECK_WEBSITE': 'https://www.example.com',
        'PROXY_RETRY_ON_ERROR': 3,
        'DO_PRINT_DEBUG': True,
        'SENDER_EMAIL': 'your_email@gmail.com',
        'SENDER_PASSWORD': 'your_email_password',
        'RECEIVER_EMAIL': 'receiver_email@gmail.com',
        'SMTP_SERVER': 'smtp.gmail.com',
        'SMTP_PORT': 587,
        'EXAMPLE_PAGE_URL': 'https://example.com',
        'PROXY_FILE': 'proxies.txt',  # Added the proxy file key
        'DATA_FILE': 'data.yaml',
        'PROCESS_STARTING_PAGE': 'https://example.com',  # Added the starting page for processing items
    }

    with open(config_file_path, 'w') as yaml_file:
        yaml.dump(sample_config, yaml_file, default_flow_style=False)

    print(f"Configuration file created: {config_file_path}")

def read_proxies_from_file(file_path="proxies.txt"):
    try:
        with open(file_path, 'r') as file:
            proxies = [line.strip() for line in file.readlines()]
        return proxies
    except Exception as e:
        raise ValueError(f"Error reading proxies file: {e}")

def get_proxy_for_item(item, proxies, last_used_proxy_index):
    if not proxies:
        return None

    last_used_proxy_index = (last_used_proxy_index + 1) % len(proxies)
    return proxies[last_used_proxy_index]

def initialize(config):
    try:
        config_data = read_config(config_file_path)
        required_keys = {'Username', 'Password', 'Email'}
        if not set(config_data.keys()).issuperset(required_keys):
            raise ValueError("Invalid keys in the configuration file.")

        config.update(config_data)

        # Read proxies from file and add to the config
        proxy_file_path = config_data.get('PROXY_FILE', 'proxies.txt')
        proxies = read_proxies_from_file(proxy_file_path)
        config['PROXIES'] = proxies

    except Exception as e:
        raise ValueError(f"Error reading configuration file: {e}")

    print(f"Configuration file loaded: {config_file_path}")

def feed_queue(config):
    data_file_path = config.get('DATA_FILE', 'data.yaml')  # Use 'data.yaml' by default

    # Check if the data file exists
    if not os.path.isfile(data_file_path):
        raise ValueError(f"Data file not found. Please create a valid {data_file_path} file.")

    try:
        with open(data_file_path, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)

        df_combined = pd.DataFrame(data)
        queue = df_combined.to_dict(orient='records')
        return queue

    except Exception as e:
        raise ValueError(f"Error reading data file: {e}")

def process_queue(queue, config):
    example_page_url = config.get('EXAMPLE_PAGE_URL', 'https://example.com')
    starting_page = config.get('PROCESS_STARTING_PAGE', 'https://example.com')

    proxies = config.get('PROXIES', [])
    last_used_proxy_index = -1

    for idx, item in enumerate(queue, start=1):
        username = item['Username']
        password = item['Password']
        email = item['Email']

        # Get a proxy for the current item
        proxy = get_proxy_for_item(item, proxies, last_used_proxy_index)

        # Log: Using proxy for the current item
        print(f"Using proxy for item {idx}: {proxy}")

        # Use the proxy when navigating to the starting page
        if go_to_page(starting_page, proxy=proxy, doPrintDebug=True):
            # Log: Successful navigation to the starting page with the current proxy
            print(f"Successfully navigated to {starting_page} using proxy: {proxy}")

            # Placeholder: Add your processing functions here
            print(f"Processing item {idx}: {username}, {email}, {proxy}")
            # Placeholder: Add more processing steps as needed

            # Update the last used proxy index
            last_used_proxy_index = proxies.index(proxy)

    print("Processing complete.")

def go_to_page(url, proxy=None, doPrintDebug=False):
    try:
        options = webdriver.ChromeOptions()

        if proxy:
            options.add_argument(f'--proxy-server={proxy}')

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Placeholder: Add additional logic as needed

        return True  # Return True if the page navigation is successful

    except Exception as e:
        # Placeholder: Handle exceptions if needed
        print(f"Error navigating to {url} with proxy {proxy}: {e}")
        return False
    finally:
        if driver:
            driver.quit()

def end_program():
    print("Program execution complete.")

# Main Execution Flow
try:
    CONFIG_FILE_PATH = 'config.yaml'
    config = read_config(CONFIG_FILE_PATH)
    
    # Log: Starting program execution
    print("Starting program execution...")

    initialize(config)
    
    queue = feed_queue(config)
    
    process_queue(queue, config)

except Exception as e:
    # Log: An error occurred
    print(f"An error occurred: {e}")
    # Log: Detailed error traceback
    traceback.print_exc()

finally:
    # Log: Ending program execution
    end_program()
