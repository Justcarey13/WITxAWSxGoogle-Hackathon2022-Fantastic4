
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("fantastic-4-17e97-firebase-adminsdk-bt1mc-455424f7ee.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Create dummy data
pipe_dummy_data = {'id': '1', ' material ': 'steel', 'age': 10, 'diameter': 300, 'pressure': 1.1, 'depth': 0.7 }
db.collection('infrastructure').document('10-09-2022').collection('pipe').add(pipe_dummy_data)

