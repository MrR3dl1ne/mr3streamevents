# Mr3StreamEvents

## Description

This libary contains a range of functionality to help streamers of all types. The tools within are able to capture events from some of the major stream providers (twitch, youtube, etc..) and perform actions.

At the time of writing this, the only actions supported are sending a request to a remote REST endpoint (like Home Assistant) or playing a variety of sounds. More actions will be coming shortly as we build on this base. Using the REST integration would allow a streamer to execution automations in their Home Assistant or other automation software when events occur, like follows, subs and comments.

## Prequisites

The only prerequisite is to have python 3.7+ installed


## Installation

To install this tool, download the zip archive from github and extract it to a folder on your local system. After the archive has been extracted, you will need to customize the config.yaml file.

## Running The Script

After customizing the config.yaml file below, running the script is simple. Just execute it like the following:

```
# python3 mr3streamevents.py
```

## Configuration File (config.yaml)

### Simple Sound Use Case

A common use case is to play a sound when a comment received after a certain period of silence. This will be most helpful for new streamers with not so active chat channels. You can configure the silence threshold (a new comment has been added after x amount of seconds of silence) by setting the "threshold_sec" value. 

**Here is a sample config.yaml for a sound only action, based on comment activity:**

```
source_streams:
- provider: twitch
  provider_settings:
    stream_name: mrr3dl1ner
    api_token: ''
    username: watchinu
    events:
    - type: comment_activity
      settings:
        threshold_sec: 1
      actions:
      - type: sound
        settings:
          sound_file: 'sounds/alert.wav'
```

### REST Endpoint Use Case Only

Another frequently requested use case is triggering a home automation process when a chat comment is received after a certain delay of silence. Like the previous use-case, this one is handy for newer streamers who dont want to miss new chat messages. This can be used instead of, or in addition to, the sound use case above.

** Here is a sample config.yaml for a REST Endpoint Use Case Only **
In this use case, we are communicating with a local Home Assistant server to trigger an automation named "alert_comment". This particular automation makes our nanoleaf light flash a few different colors to alert us of the new comment.

```
rest_services:
  myonlyhomeassistant:
    fqdn: homeassistant
    base_path: /api/webhook
    port: '8123'
    ssl: False

source_streams:
- provider: twitch
  provider_settings:
    stream_name: mrr3dl1ner
    api_token: ''
    username: watchinu
    events:
    - type: comment_activity
      settings:
        threshold_sec: 1
      actions:
      - type: rest_service
        settings: 
          rest_service: myonlyhomeassistant
          method: POST
          endpoint: alert_comment
```

### Combining Sound and REST Use Cases

To combine these use cases, just simply define both actions under the twitch provider

** Here is a sample combined config.yaml **

```
rest_services:
  myonlyhomeassistant:
    fqdn: homeassistant
    base_path: /api/webhook
    port: '8123'
    ssl: False

source_streams:
- provider: twitch
  provider_settings:
    stream_name: mrr3dl1ner
    api_token: ''
    username: watchinu
    events:
    - type: comment_activity
      settings:
        threshold_sec: 1
      actions:
      - type: sound
        settings:
          sound_file: 'sounds/alert.wav'
      - type: rest_service
        settings: 
          rest_service: myonlyhomeassistant
          method: POST
          endpoint: alert_comment

```