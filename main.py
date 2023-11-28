import requests
import time
import datetime
import random
import re
import sys, os
import json

os.system("")

with open('config.json') as f:
    config = json.load(f)
    webhook = config['discord_webhook']

if webhook == "":
    useWebhook = False
else:
    useWebhook = True

def log(text):
    timestamp = datetime.datetime.utcfromtimestamp(time.time()).strftime("%H:%M:%S")
    print(f"[{timestamp}] {text}")

def check(session, assetId):
    try:
        url = re.search('<url>(.*?)</url>', session.get(f'https://assetdelivery.roblox.com/v1/asset?id={assetId}', timeout=5).text).group(1).replace('http://www.roblox.com/asset/?id=', 'https://assetdelivery.roblox.com/v1/asset?id=')
    except:
        return False
    
    r = session.get(url, timeout=5).content
    if len(r) >= 7500:
        return True

if len(sys.argv) < 2:
    print("No assets given.\nUsage: main.py assetId1-assetType1 assetId2-assetType2 ...")
    sys.exit(1)

with open("useragents.txt", "r") as file:
    useragents = file.read().splitlines()

assets = {}
for arg in sys.argv[1:]:
    assetId, assetType = arg.split("-")
    assets[assetId] = False

with requests.Session() as session:
    log(f"Monitoring {len(sys.argv[1:])} assets...")
    while True:
        for arg in sys.argv[1:]:
            assetId, assetType = arg.split("-")
            if assets[assetId]:
                time.sleep(0.5)
            else:
                useragent = random.choice(useragents)
                session.headers.update({"User-Agent": useragent})
                try:
                    if check(session,assetId):
                        log(f"{assetId} is \u001b[32maccepted\u001b[0m")
                        assets[assetId] = True
                        if useWebhook:
                            embed_data = {"title": "Asset just got accepted","fields": [{"name": "ID","value": f"```{assetId}```"}],"color": 65280,"footer": {"text": "github.com/emppu-dev/accept-monitor"}}
                            payload = {"embeds": [embed_data]}
                            response = requests.post(webhook, data=json.dumps(payload), headers={"Content-Type": "application/json"})

                except:
                    log("Something went wrong")
                time.sleep(5)