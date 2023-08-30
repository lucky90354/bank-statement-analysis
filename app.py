from flask import Flask, request, jsonify
import os
import datetime
import uuid
import main

app = Flask(__name__)

# Path to upload files
UPLOAD_FOLDER = 'UPLOAD_FOLDER/'

# Route to uploading PDF file
@app.route('/file/upload', methods=['POST'])
def upload_file():
    if 'document' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    # Saving current timestamp
    current_time = str(datetime.datetime.now()).replace('-', '_').replace(':', '_')
    ID = uuid.uuid4().hex

    # Setting filename that is being received to current timestamp with its directory
    filename = os.path.join(UPLOAD_FOLDER, ID, current_time + '.pdf')

    # If the UUID folder doesn't already exist, create it
    if not os.path.exists(os.path.join(UPLOAD_FOLDER, ID)):
        os.makedirs(os.path.join(UPLOAD_FOLDER, ID))

    # Get PDF file
    file = request.files['document']
    file.save(filename)

    print("FILENAME:", filename)

    # Call the main function to process the uploaded file
    result = main.main(filename)

    return jsonify(result)


# GET
@app.route('/')
@app.route('/index')
def home():
    return 'Welcome to the file upload API!'


if __name__ == '__main__':
    app.run(debug=True)
