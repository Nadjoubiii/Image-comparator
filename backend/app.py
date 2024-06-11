from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import cv2
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim
from sklearn.metrics import mean_squared_error

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '' or file2.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
        file1.save(filepath1)
        file2.save(filepath2)

        # Call your image comparison function here
        score = compare_images(filepath1, filepath2)

        return jsonify({'result': score}), 200

    return jsonify({'error': 'Invalid file type'}), 400

def compare_images(img_path1, img_path2):
    # Open images
    original = Image.open(img_path1)
    tampered = Image.open(img_path2)

    # Resize images to be the same size
    original = original.resize((250, 160))
    tampered = tampered.resize((250, 160))

    # Save resized images temporarily
    original.save('uploads/original_resized.png')
    tampered.save('uploads/tampered_resized.png')

    # Convert images to OpenCV format
    original = cv2.imread('uploads/original_resized.png')
    tampered = cv2.imread('uploads/tampered_resized.png')

    # Convert images to grayscale
    original_converted = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    tampered_converted = cv2.cvtColor(tampered, cv2.COLOR_BGR2GRAY)

    # Compute Structural Similarity Index (SSI)
    (score, difference) = ssim(original_converted, tampered_converted, full=True)
    difference = (difference * 255).astype('uint8')

    # Optionally: Save the difference image
    cv2.imwrite('uploads/difference.png', difference)

    # Compute Mean Squared Error (MSE) - Optional
    mse_value = mean_squared_error(original_converted, tampered_converted)

    # Print or return both scores if needed
    print(f"SSIM: {score}")
    print(f"MSE: {mse_value}")

    return score

if __name__ == '__main__':
    app.run(debug=True)
