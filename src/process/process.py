import os
import pandas as pd
import requests
from selenium import webdriver
import yaml
from password_generator import generate_random_password
from src.proxy.proxy_utils import get_proxy_for_item

def feed_queue(config):
    """
    Creates a DataFrame based on NUMBER_OF_ACCOUNTS_TO_BE_CREATED from the config file.

    Args:
        config (dict): Configuration dictionary.

    Returns:
        pd.DataFrame: A DataFrame containing the data.
    """
    try:
        number_of_accounts_to_be_created = config.get('NUMBER_OF_ACCOUNTS_TO_BE_CREATED')

        # Create a list of dictionaries
        data_list = []
        for i in range(number_of_accounts_to_be_created):
            data_list.append({
                'Username': f'username{i}',
                'Email': f'email{i}',
                'IP_Address': f'ip_address{i}',
            })

        # Convert the list to a DataFrame
        df_combined = pd.DataFrame(data_list, columns=['Username', 'Email', 'IP_Address', 'Password'])

        print(f"Queue successfully fed. Number of items in queue: {len(df_combined)}")
        return df_combined

    except Exception as e:
        raise ValueError(f"Error feeding the queue: {e}")


def process_queue(queue, config):
    """
    Processes items in the queue, performs actions based on configuration.

    Args:
        queue (pd.DataFrame): DataFrame containing items to process.
        config (dict): Configuration dictionary.
    """
    example_page_url = config.get('EXAMPLE_PAGE_URL')
    starting_page = config.get('PROCESS_STARTING_PAGE')

    proxies = config.get('PROXIES', [])
    last_used_proxy_index = -1

    # MAIN LOOP
    for idx, item in queue.iterrows():
        username = item.get('Username', '')
        email = item.get('Email', '')
        
        # Generate a random password for the item
        password = generate_random_password(length=12, use_numbers=True, use_special_chars=True)
        queue.at[idx, 'Password'] = password

        # Get the country for the item
        country = get_country_for_item(item)
        print(f"Country for item {idx + 1}: {country}")

        proxy = get_proxy_for_item(item, proxies, last_used_proxy_index)
        print(f"Processing item {idx + 1} completed.")
    print("Processing complete.")

def get_country_for_item(item):
    """
    Gets the country for an item based on its IP address.

    Args:
        item (pd.Series): DataFrame row representing an item.

    Returns:
        str: The country or 'N/A' if no IP address is available.
    """
    ip_address = item.get('IP_Address', '')  
    if ip_address:
        return get_country_by_ip(ip_address)
    else:
        return "N/A"  # Replace with an appropriate default value

def get_country_by_ip(ip_address):
    """
    Gets the country based on an IP address.

    Args:
        ip_address (str): IP address.

    Returns:
        str: The country or 'N/A' if an error occurs.
    """
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        data = response.json()
        country = data.get('country')
        return country
    except Exception as e:
        print(f"Error retrieving IP information: {e}")
        return "N/A"  # Replace with an appropriate default value

def go_to_page(url, proxy=None, do_print_debug=False):
    """
    Navigates to a web page using a specified proxy.

    Args:
        url (str): URL of the web page.
        proxy (str): Proxy to use.
        do_print_debug (bool): Whether to print debug information.

    Returns:
        bool: True if navigation is successful, False otherwise.
    """
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
    """
    Prints a message indicating the completion of program execution.
    """
    print("Program execution complete.")
