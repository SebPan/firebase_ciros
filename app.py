import firebase_admin
import os
import json
from firebase_admin import credentials, db
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize Firebase directly at startup
try:
    firebase_credentials = os.environ.get('FIREBASE_CREDENTIALS')
    if firebase_credentials:
        cred_dict = json.loads(firebase_credentials)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {"databaseURL": "https://prueba-7ce87-default-rtdb.firebaseio.com/"})
        print("Firebase initialized successfully")
    else:
        print("FIREBASE_CREDENTIALS environment variable not found")
except Exception as e:
    print(f"Error initializing Firebase: {str(e)}")

@app.route('/update-temp', methods=['POST'])
def update_temp():
    try:
        # Print request details for debugging
        print(f"Request headers: {dict(request.headers)}")
        print(f"Request content type: {request.content_type}")
        print(f"Request data: {request.data}")
        
        # Check if the request has any data
        if not request.data:
            return jsonify({"status": "error", "message": "No data provided in request"}), 400
            
        # Try to parse JSON
        try:
            data = request.get_json(force=True)
        except Exception as e:
            return jsonify({"status": "error", "message": f"Invalid JSON format: {str(e)}"}), 400
            
        # Check if valor exists in the data
        if 'valor' not in data:
            return jsonify({"status": "error", "message": "Missing 'valor' field in request"}), 400
            
        temp_value = data['valor']
        
        # Update Firebase
        ref = db.reference("datos/temp")
        ref.set({"valor": temp_value})
        
        return jsonify({"status": "success", "message": f"Temperature updated to {temp_value}"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/test', methods=['POST'])
def test_endpoint():
    """Simple endpoint to echo back the received data for debugging"""
    try:
        data = request.get_json(force=True) if request.data else {}
        print(data)
        return jsonify({
            "status": "success",
            "received_data": data,
            "content_type": request.content_type,
            "headers": dict(request.headers)
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Firebase temperature update service is running. Send POST requests to /update-temp"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
