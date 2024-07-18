import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('credentials/compiladores-f45fd-firebase-adminsdk-b17c4-c64692aa7d.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

