import os, yaml, requests
from sys import platform


def get_config_file():
    # Define our global variables
    config_file = os.path.dirname(os.path.realpath(__file__)) + '/../config.yaml'

    # Check if the config file exists or exception
    if not os.path.isfile(config_file):
        raise Exception(f"Unable to locate config.yaml file at location {config_file}")
    
    # Let's load the user config
    with open(config_file) as script_config:
        script_config = yaml.safe_load(script_config)
        
    return script_config
        
def describe_rest_service(name):
    config_file = get_config_file()
    
    return {
        "name": name,
        "details": config_file['rest_services'][name]
    }
  

def play_sound(action):
    sound_file = action['settings']['sound_file']
    
    if "linux" in platform:
        import os
        os.system(f"aplay -q {sound_file}")

    elif "darwin" in platform:
        import os
        os.system(f"afplay {sound_file}")

    elif "win" in platform:
        import winsound
        winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)

    else:
        raise Exception('ERROR: Unsupported platform to play audio. Edit config.py and disable audio.')
    

def call_rest_service(action):
    rest_service = describe_rest_service(action['settings']['rest_service'])
    endpoint_url = rest_service['details']['fqdn']+ ':' + rest_service['details']['port'] + rest_service['details']['base_path'] + '/' + action['settings']['endpoint']
        
    if rest_service['details']['ssl']:
        endpoint_url = f"https://{endpoint_url}"
    else:
        endpoint_url = f"http://{endpoint_url}"
    
    req = requests.request(
        action['settings']['method'],
        endpoint_url,
        verify=False,
        timeout=5
    )
    
    if req.status_code != 200:
        raise Exception(f"REST service responded with code {req.status_code}")
