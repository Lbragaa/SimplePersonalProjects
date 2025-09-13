import os  # To access environment variables
import requests  # Sends HTTP requests
import json  # Formats the response data, for pretty printing (optional)
import time
import random
import hashlib

def send_discord_notification(content):
    """Send a message to Discord via webhook."""
    webhook_url = os.environ.get('WEBHOOK_URL')
    
    if not webhook_url:
        print("❌ No Webhook URL provided.")
        return
    
    data = {"content": content}

    try:
        response = requests.post(webhook_url, json=data)  # <-- Fixed typo here!

        if response.status_code == 204:
            print("✅ Discord notification sent!")
        else:
            print(f"❌ Failed to send notification: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception occurred while sending Discord notification: {e}")

def generate_ds(): 
    """Generate the DS header required for API authentication."""
    salt = "xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs"
    t = str(int(time.time()))
    r = str(random.randint(100000, 200000))
    
    to_hash = f"salt={salt}&t={t}&r={r}"
    hash_result = hashlib.md5(to_hash.encode()).hexdigest()
    
    return f"{t},{r},{hash_result}"

# Retrieve authentication tokens from environment variables
ltoken = os.environ.get('LTOKEN')
ltuid = os.environ.get('LTUID')
cookie_token = os.environ.get('COOKIE_TOKEN')

# Prepare cookies for the requests
cookies = {
    "ltoken_v2": ltoken,
    "ltuid_v2": ltuid,
    "cookie_token_v2": cookie_token
}

# Set default headers
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Referer": "https://webstatic-sea.hoyolab.com/",
    "x-rpc-client_type": "5",
    "x-rpc-language": "en-us",
    "x-rpc-app_version": "2.36.1"
}

# Define the games and their check-in API info
games = {
    "Genshin Impact": {
        "act_id": "e202102251931481",
        "url": "https://sg-hk4e-api.hoyolab.com/event/sol/sign"
    },
    "Honkai Star Rail": {
        "act_id": "e202303301540311",
        "url": "https://sg-public-api.hoyolab.com/event/luna/hkrpg/os/sign"
    },
    # "Zenless Zone Zero": {
    #     "act_id": "e202309261540311",
    #     "url": "https://sg-public-api.hoyolab.com/event/luna/zzz/os/sign"
    # }
}

# Loop through each game and perform check-in
for game, info in games.items():
    start_time = time.time()

    headers["DS"] = generate_ds()  # Generate DS for each request

    # Optional ZZZ code commented out
    # if game == "Zenless Zone Zero":
    #     headers["x-rpc-device_fp"] = "b3725dd5d768b7785bc0db3e7ec982e6_0.4772665154817586"
    #     headers["x-rpc-device_id"] = "b3725dd5d768b7785bc0db3e7ec982e6_0.4772665154817586"
    #     headers["x-rpc-platform"] = "4"
    #     headers["x-rpc-signgame"] = "zzz"

    data = {"act_id": info["act_id"]}
    url = info["url"]

    print(f"\n 🔹 Checking in for {game}...")

    # Perform the POST request to check-in
    response = requests.post(url, headers=headers, cookies=cookies, json=data)

    end_time = time.time()
    elapsed = round(end_time - start_time, 2)

    print(f"⏱️ Response time: {elapsed}s")

    # Prepare the Discord message based on the result
    msg = ""
    
    if response.status_code == 200:
        res_json = response.json()

        if res_json['retcode'] == 0:
            msg = f"✅ {game}: Successfully checked in!"
        elif res_json['retcode'] == -5003:
            msg = f"⚠️ {game}: Already checked in today!"
        else:
            msg = f"⚠️ {game}: Something happened - {res_json['message']}"
    else:
        msg = f"❌ {game}: HTTP Error! Status code: {response.status_code}"

    print(msg)
    send_discord_notification(msg)
