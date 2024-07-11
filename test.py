import requests
import json

msg = "asd"

webhook_url = "https://discord.com/api/webhooks/1260238289743511644/cXYGPvAeZVhjmGlOQ8txKTVkgABwPcYV4Bre1YlSeM147qfeSq9r4kcxV0HPWd1-IsNO"
params = "?wait=true"
data = {
            "content": msg
        }

response = requests.post(webhook_url,json=data).json()

message_id = json.loads(response)["id"]
print(message_id)
data = {
            "content": "qwe"
        }
requests.patch(webhook_url+"/messages/"+message_id+params,json=data)