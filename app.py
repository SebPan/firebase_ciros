import firebase_admin
import os
import json
from firebase_admin import credentials, db
from flask import Flask, request

app = Flask(__name__)

# Initialize Firebase using environment variables
firebase_credentials = os.environ.get('FIREBASE_CREDENTIALS')
if firebase_credentials:
    cred_dict = json.loads(firebase_credentials)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {"databaseURL": "https://prueba-7ce87-default-rtdb.firebaseio.com/"})

@app.route('/update-temp', methods=['POST'])
def update_temp():
    try:
        # Get data from request
        data = request.json
        temp_value = data.get('valor', 'No value provided')
        
        # Update Firebase
        ref = db.reference("datos/temp")
        ref.set({"valor": temp_value})
        
        return {"status": "success", "message": f"Temperature updated to {temp_value}"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
