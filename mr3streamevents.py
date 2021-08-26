import os
import signal
from lib.common import *
from lib.twitch import twitch_class

# Load config file
config_file = get_config_file()

# Define the signal handler so we can exit the script
def signal_handler(signal, frame):
    """Raises a flag when a keyboard interrupt is raised."""
    global interrupted
    interrupted = True


# Define our providers
twitch_provider = None

if __name__ == '__main__':
    interrupted = False
    signal.signal(signal.SIGINT, signal_handler)

    # Start the main loop
    while not interrupted:
        # Pull the data from each platform and perform the requested actions
        for stream in config_file['source_streams']:
            if stream['provider'].lower() == 'twitch':
                if twitch_provider is None:
                    twitch_provider = twitch_class(stream['provider_settings']['stream_name'])
                
                twitch_provider.check_for_events(stream['provider_settings']['events'])
    
    # Close any existing sockets after an interrupt            
    twitch_provider.close_socket()