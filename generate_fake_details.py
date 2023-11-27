import requests
import pandas as pd
from datetime import datetime, timedelta
import random
import logging

LOG_FILENAME = 'fake_data_generator.log'

# Configure logging
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

API_URL = 'api.namefake.com'  # Update the API_URL
DATE_FORMAT = '%d.%m.%Y'


def get_name_data(api_url, num_per_request):
    api_endpoint = f"https://{api_url}/"
    print(api_endpoint)
    headers = {'Accept': 'application/json'}  # Adding the Accept header

    try:
        response = requests.get(api_endpoint, params={'number': num_per_request}, headers=headers)
        response.raise_for_status()
        name_data = response.json()

        # Check if the response contains the expected fields
        if 'name' in name_data:
            return [name_data]
        else:
            logging.warning(f"Unexpected API response: {name_data}")
            return []
    except requests.exceptions.RequestException as e:
        logging.error(f"Error in get_name_data: {e}")
        return []


def clean_name_surname(name_data):
    cleaned_name = name_data.get('name', '')
    cleaned_surname = name_data.get('maiden_name', '')

    return cleaned_name, cleaned_surname


def generate_fake_details(api_url, num, email_domain):
    fake_details_list = []

    num_per_request = num  # You may adjust this based on your needs

    for _ in range(num):
        name_data_list = get_name_data(api_url, num_per_request)

        for name_data in name_data_list:
            cleaned_name, cleaned_surname = clean_name_surname(name_data)

            if not cleaned_name or not cleaned_surname:
                continue

            random_days = random.randint(int(365.25 * 21), int(365.25 * (datetime.now().year - 1988)))
            birthdate = (datetime.now() - timedelta(days=random_days)).strftime(DATE_FORMAT)

            random_number1 = random.randint(1, 999)
            random_number2 = random.randint(1, 999)
            email = f"{cleaned_name.lower()}_{random_number1}_{cleaned_surname.lower()}_{random_number2}@{email_domain}"

            fake_details_list.append({
                "name": cleaned_name,
                "surname": cleaned_surname,
                "email": email,
                "birthdate": birthdate,
            })

            logging.info(f"Fake details created: {cleaned_name} {cleaned_surname} ({email}), Birthdate: {birthdate}")

    logging.info(f"Total amount of fake data created: {len(fake_details_list)}")

    # Extracting data to variables
    names = [details["name"] for details in fake_details_list]
    surnames = [details["surname"] for details in fake_details_list]
    emails = [details["email"] for details in fake_details_list]
    birthdates = [details["birthdate"] for details in fake_details_list]

    return names, surnames, emails, birthdates


# Usage example
api_url = API_URL
num = 1
email_domain = 'johnsmith2222.sbs'
names, surnames, emails, birthdates = generate_fake_details(api_url, num, email_domain)
# Now you have the data in the specified variables
print("Names:", names)
print("Surnames:", surnames)
print("Emails:", emails)
print("Birthdates:", birthdates)
