from discord import SyncWebhook

webhook_url = "https://discord.com/api/webhooks/1226806125266210887/Lq3dM6PPIif4NSi3owWhLia8Rm0zUFtEtz06LJBkbwGrPzt4NAD-ttgIkWFt3eMfpxM1"

message = "Well... this was easier than I expected"



webhook = SyncWebhook.from_url(webhook_url)
webhook.send(message)