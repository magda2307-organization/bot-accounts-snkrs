import os
import pandas as pd
from selenium import webdriver
import yaml
from src.proxy.proxy_utils import get_proxy_for_item
from password_generator import generate_random_password

def feed_queue(config):
    data_file_path = config.get('DATA_FILE', 'config/config.yaml')

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
        username = item.get('Username', '')
        email = item.get('Email', '')

        # Generate a random password using your function
        password = generate_random_password(length=12, use_numbers=True, use_special_chars=True)

        # Add the generated password to the item
        item['Password'] = password

        # Placeholder: Add more processing steps as needed

        proxy = get_proxy_for_item(item, proxies, last_used_proxy_index)

        print(f"Using proxy for item {idx}: {proxy}")

        if go_to_page(starting_page, proxy=proxy, doPrintDebug=True):
            print(f"Successfully navigated to {starting_page} using proxy: {proxy}")

            print(f"Processing item {idx}: {username}, {email}, {proxy}")
            # Placeholder: Add more processing steps as needed

            last_used_proxy_index = proxies.index(proxy)

    print("Processing complete.")

def go_to_page(url, proxy=None, doPrintDebug=False):
    try:
        options = webdriver.ChromeOptions()

        if proxy:
            options.add_argument(f'--proxy-server={proxy}')

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        return True

    except Exception as e:
        print(f"Error navigating to {url} with proxy {proxy}: {e}")
        return False
    finally:
        if driver:
            driver.quit()

def end_program():
    print("Program execution complete.")
