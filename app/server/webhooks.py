"""building webhooks"""
import json
import requests

from app.server.models import Army
from app.server.response import ResponseCreate



class WebhookService:
    """Service for handling webhooks"""
    def __init__(self):
        self.headers = {"Content-Type": "application/json",
                        "Webhook-Topic": None}
        self.response_create = ResponseCreate()

    def create_army_join_webhook(self, payload):
        self.headers["Webhook-Topic"] = "army.join"
        armys = Army.query.filter(Army.status == 'alive', Army.id != payload.id).all()
        webhook_payload = self.response_create.create_army_join_webhook_response(payload)

        webhook_urls = [army.webhook_url for army in armys]
        for url in webhook_urls:
            requests.post(
                url, data=json.dumps(webhook_payload), headers=self.headers)

    def create_army_leave_webhook(self, payload, leave_type):
        self.headers["Webhook-Topic"] = "army.leave"

        armys = Army.query.filter(Army.status == 'alive', Army.id != payload.id).all()
        webhook_payload = self.response_create.create_army_leave_webhook_response(
            payload, leave_type)

        webhook_urls = [army.webhook_url for army in armys]
        for url in webhook_urls:
            requests.post(
                url, data=json.dumps(webhook_payload), headers=self.headers)

    def create_army_update_webhook(self, defence_army, attack_army):
        self.headers["Webhook-Topic"] = "army.update"
        url = defence_army.webhook_url
        webhook_payload = self.response_create.create_army_update_webhook_response(defence_army)

        requests.post(
            url, data=json.dumps(webhook_payload), headers=self.headers)

        url = attack_army.webhook_url
        requests.post(
            url, data=json.dumps(webhook_payload), headers=self.headers)
