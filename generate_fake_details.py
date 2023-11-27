import requests
import pandas as pd

def clean_name_surname(name_data):
    """
    Clean the name and surname to contain only basic alphabet characters.

    Args:
    - name_data (dict): The name data obtained from the Fake Name Generator API.

    Returns:
    - tuple: Cleaned name and surname.
    """
    name_parts = name_data['name'].split()
    cleaned_name = ''.join(filter(str.isalpha, name_parts[0]))
    cleaned_surname = ''.join(filter(str.isalpha, name_parts[1]))
    return cleaned_name.capitalize(), cleaned_surname.capitalize()

def generate_fake_details(api_url, country, name_format, num):
    """
    Generate fake details using the Fake Name Generator API with an equal distribution of male and female.

    Args:
    - api_url (str): The base URL of the Fake Name Generator API.
    - country (str): Country for the generated name (e.g., 'united-states').
    - name_format (str): The format of the generated name (e.g., '{name}_{surname}_{number}').
    - num (int): Number of fake details to generate.

    Returns:
    - pd.DataFrame: DataFrame containing fake details (name, surname, email, gender).
    """
    fake_details_list = []

    # Calculate half of the total details for each gender
    num_per_gender = num // 2

    for gender in ['male', 'female']:
        # Generate fake details for the specified gender
        api_endpoint = f"{api_url}/{country}/{gender}/"
        response = requests.get(api_endpoint, params={'number': num_per_gender})

        if response.status_code == 200:
            name_data_list = response.json()

            for idx, name_data in enumerate(name_data_list, start=1):
                cleaned_name, cleaned_surname = clean_name_surname(name_data)
                number = idx + (num_per_gender if gender == 'female' else 0)

                email = f"{cleaned_name.lower()}_{cleaned_surname.lower()}_{number}@johnsmith2222.sbs"
                
                # Append the generated details to the list
                fake_details_list.append({
                    "name": cleaned_name,
                    "surname": cleaned_surname,
                    "email": email,
                    "gender": gender,
                })

                print(f"Fake details created: {cleaned_name} {cleaned_surname} ({email}), Gender: {gender}")

    print(f"Total amount of fake data created: {len(fake_details_list)}")

    # Convert the list of dictionaries to a DataFrame
    fake_details_df = pd.DataFrame(fake_details_list)

    return fake_details_df

# Example usage:
api_url = "http://api.name-fake.com"
country = "english-united-states"
name_format = "{name}_{surname}_{number}"
num_fake_details = 10  # The total number of fake details, so it will generate 5 for each gender

fake_details_df = generate_fake_details(api_url, country, name_format, num_fake_details)
print("\nGenerated Fake Details:")
print(fake_details_df)
