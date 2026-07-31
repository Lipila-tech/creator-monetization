import os
import json
import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    if not firebase_admin._apps:
        cred_path = os.getenv("FIREBASE_CREDENTIALS")
        try:
            cred_dict = json.loads(cred_path, strict=False)
            if cred_path:
                cred = credentials.Certificate(cred_dict)
            else:
                cred = {}
        except (TypeError, json.JSONDecodeError):
            cred = {}
        firebase_admin.initialize_app(cred)
