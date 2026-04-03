import os
import json
import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    if not firebase_admin._apps:
        cred_path = os.getenv("FIREBASE_CREDENTIALS")
        cred_dict = json.loads(cred_path, strict=False)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
