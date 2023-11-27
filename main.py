import traceback
from src.initialize import initialize as init_module
from src.process.process import feed_queue, process_queue, end_program

CONFIG_FILE_PATH = 'config/config.yaml'

try:
    config = {}  # Provide an empty config dictionary or load it from somewhere

    # Call read_config to get the config data
    config_data = init_module.read_config(CONFIG_FILE_PATH)

    # Pass config_file_path and config to the initialize function
    init_module.initialize(CONFIG_FILE_PATH, config)
 
    print("Starting program execution...")

    # Use init_module to reference the module
    init_module.initialize(config)
 
    queue = feed_queue(config)
 
    process_queue(queue, config)

except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()

finally:
    end_program()
