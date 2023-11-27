import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import random

def get_name_data(api_url, country, gender, num_per_gender):
    api_endpoint = f"{api_url}/{country}/{gender}/"
    response = requests.get(api_endpoint, params={'number': num_per_gender})

    if response.status_code == 200:
        try:
            name_data = json.loads(response.text)
            if isinstance(name_data, list):
                return name_data
            else:
                return [name_data]
        except json.JSONDecodeError as e:
            print(f"Error decoding API response as JSON: {e}")
    else:
        print(f"Error: Unable to fetch data for {gender} gender. Status Code: {response.status_code}")
        return []

def clean_name_surname(name_data):
    if 'name' in name_data:
        name_parts = name_data['name'].split()
        cleaned_name = ''.join(filter(str.isalpha, name_parts[0]))
        cleaned_surname = ''.join(filter(str.isalpha, name_parts[1]))
        return cleaned_name.capitalize(), cleaned_surname.capitalize()
    else:
        print("Error: 'name' not found in name_data.")
        return None, None

def generate_fake_details(api_url, country, num, email_domain):
    fake_details_list = []

    num_per_gender = num // 2

    for _ in range(num):
        # Randomly select gender for each entry
        gender = random.choice(['male', 'female'])
        name_data_list = get_name_data(api_url, country, gender, 1)

        for name_data in name_data_list:
            cleaned_name, cleaned_surname = clean_name_surname(name_data)

            if cleaned_name is None or cleaned_surname is None:
                continue  # Skip this entry if cleaning fails

            random_days = random.randint(int(365.25 * 21), int(365.25 * (datetime.now().year - 1988)))
            birthdate = (datetime.now() - timedelta(days=random_days)).strftime('%d.%m.%Y')

            # Introduce additional randomness in the email
            random_number1 = random.randint(1, 999)
            random_number2 = random.randint(1, 999)
            email = f"{cleaned_name.lower()}_{random_number1}_{cleaned_surname.lower()}_{random_number2}@{email_domain}"

            fake_details_list.append({
                "name": cleaned_name,
                "surname": cleaned_surname,
                "email": email,
                "gender": gender,
                "birthdate": birthdate,
            })

            print(f"Fake details created: {cleaned_name} {cleaned_surname} ({email}), Gender: {gender}, Birthdate: {birthdate}")

    print(f"Total amount of fake data created: {len(fake_details_list)}")

    fake_details_df = pd.DataFrame(fake_details_list)
    return fake_details_df

# Usage example
#fake_details_df = generate_fake_details(api_url='https://api.namefake.com', country='united-states', num=10, email_domain='johnsmith2222.sbs')
