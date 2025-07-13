import json
import os
import hashlib
import time
from flask import Flask, request, render_template
from PIL import Image

app = Flask(__name__)

# Load the database
DB_FILE = 'C:\\Users\\S Barath\\Desktop\\TIPNo-M2501\\TIPNo-M2501\\Code\db.json'
with open(DB_FILE, 'r') as db_file:
    database = json.load(db_file)

# Generate hash for an image
def generate_image_hash(image_path):
    with open(image_path, 'rb') as f:
        file_data = f.read()
    return hashlib.sha256(file_data).hexdigest()

# Simulate fingerprint matching
def process_and_match_fingerprint(uploaded_image_path):
    try:
        print("Processing fingerprint...")
        time.sleep(3)  # Simulate processing delay

        # Generate hash of the uploaded fingerprint image
        uploaded_hash = generate_image_hash(uploaded_image_path)
        print(f"Generated hash for uploaded image: {uploaded_hash}")

        # Compare the hash with stored hashes in the database
        for criminal in database['criminals']:
            if criminal['ImageHash'] == uploaded_hash:
                print("Match found!")
                return criminal

        print("No match found.")
        return None
    except Exception as e:
        print(f"Error during fingerprint matching: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return "No file uploaded", 400

    file = request.files['image']
    if file.filename == '':
        return "No file selected", 400

    # Save uploaded image
    upload_folder = './uploads'
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)

    # Process the fingerprint and match with the database
    matched_criminal = process_and_match_fingerprint(filepath)

    if matched_criminal:
        return render_template('result.html', details=matched_criminal["Details"])
    else:
        return render_template('result.html', details=None)

if __name__ == "__main__":
    app.run(debug=True)
