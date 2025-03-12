import firebase_admin
import os
import json
import logging
from firebase_admin import credentials, db
from flask import Flask, request

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize Firebase only if not already initialized
@app.before_first_request
def initialize_firebase():
    try:
        if not firebase_admin._apps:  # Check if Firebase is not already initialized
            firebase_credentials = os.environ.get('FIREBASE_CREDENTIALS')
            if not firebase_credentials:
                logger.error("FIREBASE_CREDENTIALS environment variable not found")
                return
            
            logger.info("Initializing Firebase...")
            cred_dict = json.loads(firebase_credentials)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {"databaseURL": "https://prueba-7ce87-default-rtdb.firebaseio.com/"})
            logger.info("Firebase initialized successfully")
        else:
            logger.info("Firebase already initialized")
    except Exception as e:
        logger.error(f"Error initializing Firebase: {str(e)}")
        raise

@app.route('/update-temp', methods=['POST'])
def update_temp():
    try:
        # Log request information
        logger.info(f"Received request: {request.json}")
        
        # Check if Firebase is initialized
        if not firebase_admin._apps:
            logger.error("Firebase not initialized")
            return {"status": "error", "message": "Firebase not initialized"}, 500
        
        # Get data from request
        data = request.json
        if not data:
            return {"status": "error", "message": "No JSON data provided"}, 400
            
        temp_value = data.get('valor')
        if temp_value is None:
            return {"status": "error", "message": "Missing 'valor' field in request"}, 400
        
        # Update Firebase
        logger.info(f"Updating Firebase with value: {temp_value}")
        ref = db.reference("datos/temp")
        ref.set({"valor": temp_value})
        
        return {"status": "success", "message": f"Temperature updated to {temp_value}"}, 200
    except Exception as e:
        logger.error(f"Error updating temperature: {str(e)}")
        return {"status": "error", "message": str(e)}, 500

@app.route('/', methods=['GET'])
def home():
    return "Firebase temperature update service is running. Send POST requests to /update-temp"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
