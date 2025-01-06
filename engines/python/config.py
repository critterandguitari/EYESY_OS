import json

# Function to load configuration
def load_config(file_path, defaults):
    """Load a configuration file with fallback to defaults."""
    try:
        # Attempt to read the file
        with open(file_path, 'r') as f:
            config = json.load(f)
        print(f"Successfully loaded config from {file_path}")
    except FileNotFoundError as e:
        print(f"Config file {file_path} not found.")
        raise FileNotFoundError(f"Configuration file not found: {file_path}") from e
    except json.JSONDecodeError as e:
        print(f"Config file {file_path} is not valid JSON.")
        raise ValueError(f"Invalid JSON in configuration file: {file_path}") from e

    # Populate missing keys with defaults
    final_config = {}
    for key, default_value in defaults.items():
        if key in config:
            print(f"Loaded '{key}' from file: {config[key]}")
            final_config[key] = config[key]
        else:
            print(f"Using default for '{key}': {default_value}")
            final_config[key] = default_value
    
    return final_config

# Function to save configuration back to file
def save_config(file_path, config):
    """Save the configuration back to the file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"Config saved to {file_path}")
    except Exception as e:
        print(f"Failed to save config: {e}")
        raise

def example() :
    DEFAULT_CONFIG = {
        "midi_channel": 1,
        "video_resolution": 720,
        "audio_gain": 50
    }

    config_file = "config.json"

    try:
        # Load configuration, raising errors for file or JSON issues
        config = load_config(config_file, DEFAULT_CONFIG)
    except FileNotFoundError as e:
        print(f"Error loading configuration: {e}")
        print("Using all default values. Saving File.")
        config = DEFAULT_CONFIG
        save_config(config_file, config)
    except ValueError as e:
        print(f"Error loading configuration: {e}")
        print("Using all default values.")
        config = DEFAULT_CONFIG

    # Modify or access configuration
    print("Current Configuration:", config)
    #config['audio_gain'] = 75  # Example modification

    # Save updated configuration
    # save_config(config_file, config)

