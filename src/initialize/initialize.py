import yaml
from generate_fake_details import generate_fake_details
from src.proxy.proxy_utils import read_proxies_from_file

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
        'PROXY_FILE': 'config/proxies.txt',
        'DATA_FILE': 'data.yaml',
        'PROCESS_STARTING_PAGE': 'https://example.com',
        'API_URL': "http://api.name-fake.com",
        'COUNTRY': "english-united-states",
        'NAME_FORMAT': "{name}_{surname}_{number}",
        'NUMBER_OF_ACCOUNTS_TO_BE_CREATED': 10,
        'EMAIL_DOMAIN': 'johnsmith2222.sbs',
    }

    with open(config_file_path, 'w') as yaml_file:
        yaml.dump(sample_config, yaml_file, default_flow_style=False)

    print(f"Configuration file created: {config_file_path}")

def initialize(config_file_path, config):
    try:
        config_data = read_config(config_file_path)
        config.update(config_data)

        proxy_file_path = config_data.get('PROXY_FILE', 'proxies.txt')
        proxies = read_proxies_from_file(proxy_file_path)
        config['PROXIES'] = proxies

        number_of_accounts = config.get('NUMBER_OF_ACCOUNTS_TO_BE_CREATED', 10)
        fake_details_df = generate_fake_details(
            api_url=config['API_URL'],
            country=config['COUNTRY'],
            name_format=config['NAME_FORMAT'],
            num=number_of_accounts,
            email_domain=config['EMAIL_DOMAIN'],
        )
        print(f"{number_of_accounts} fake accounts created")

    except Exception as e:
        raise ValueError(f"Error reading configuration file: {e}")

    print(f"Configuration file loaded: {config_file_path}")
