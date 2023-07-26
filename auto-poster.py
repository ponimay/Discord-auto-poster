import requests
import time

payload = {
    'content': "message"
}

header = {
    'Authorization': 'token discord'
}

cooldown_time = 5  # Set the cooldown time in seconds

while True:
    try:
        # Make a request
        r = requests.post("https://discord.com/api/v9/channels/id_channel/messages", data=payload, headers=header)

        # Check the response
        if r.status_code == 200:
            print("Message sent successfully.")
        else:
            print(f"Failed to send the message. Status code: {r.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

    # Add a cooldown to avoid making requests too frequently
    time.sleep(cooldown_time)
