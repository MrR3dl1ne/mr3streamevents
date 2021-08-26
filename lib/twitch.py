import socket
from lib.common import *
from datetime import datetime

twitch_fqdn = 'irc.chat.twitch.tv'
twitch_port = 6667

class twitch_class():
    
    def __init__(self, stream_name, api_token, username):
        
        stream_name=stream_name.lower()
        
        self.sock = socket.socket()
        self.sock.connect((twitch_fqdn, twitch_port))
        self.sock.send(f"PASS {api_token}\n".encode('utf-8'))
        self.sock.send(f"NICK {username}\n".encode('utf-8'))
        self.sock.send(f"JOIN #{stream_name}\n".encode('utf-8'))
        
        # Define some globals for comment activity
        self.last_comment_activity = None

    def close_socket(self):
        self.sock.close()
          
    def check_for_events(self, events):
        for event in events:
            if event['type'].lower() == 'comment_activity':
                self.check_for_comment_activity(event)

    
    def check_for_comment_activity(self, event):
        
        current_datetime = datetime.now()
        response = self.sock.recv(2048).decode('utf-8')
       
        if response.startswith('PING'):
            self.sock.send("PONG\n".encode('utf-8'))
        elif 'PRIVMSG' in response:
            if self.last_comment_activity is None:
                print(f"[TWITCH][COMMENT_ACTIVITY] Comment received that meets alert threshold, sending to specified endpoints")
                print(f"[TWITCH][COMMENT_ACTIVITY] {response}")
                self.last_comment_activity = current_datetime
                
                try:
                    for action in event['actions']:
                        if action['type'].lower() == 'rest_service':
                            call_rest_service(action)
                        elif action['type'].lower() == 'sound':
                            play_sound(action)
                        else:
                            print("Unsupported action type: " + action['type'])
                except Exception as e:
                    print("Exception: There was a problem communicating with the specified REST endpoint.")
                    print(str(e))
            else:
                time_delta = (current_datetime - self.last_comment_activity).total_seconds()
                if time_delta >= event['settings']['threshold_sec']:
                    print(f"[TWITCH][COMMENT_ACTIVITY] Comment received that meets alert threshold, sending to specified endpoints")
                    print(f"[TWITCH][COMMENT_ACTIVITY] {response}")
                    self.last_comment_activity = current_datetime
                    
                    try:
                        for action in event['actions']:
                            if action['type'].lower() == 'rest_service':
                                call_rest_service(action)
                            elif action['type'].lower() == 'sound':
                                play_sound(action)
                            else:
                                print("Unsupported action type: " + action['type'])
                    except Exception as e:
                        print("Exception: There was a problem communicating with the specified REST endpoint.")
                        print(str(e))
                    
                else:
                    self.last_comment_activity = current_datetime