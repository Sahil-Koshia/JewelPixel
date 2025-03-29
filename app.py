from flask import Flask, request, render_template, send_from_directory, url_for, jsonify, send_file
from flask_socketio import SocketIO, emit
import os
import threading
import zipfile
import tempfile
import shutil
from io import BytesIO
from utils.image_processing import preprocess_image, extract_features
from database.image_database import ImageDatabase

app = Flask(__name__)

# Local static/images path
app.config['UPLOAD_FOLDER'] = 'static/images'

# Initialize SocketIO
socketio = SocketIO(app)

# Pass socketio to ImageDatabase
db = ImageDatabase(socketio)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request.'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400
    if file:
        # Save the uploaded file to a temporary directory
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, file.filename)
        file.save(temp_file_path)

        # Process the image to extract features and find similar images
        features = extract_features(temp_file_path)
        similar_images = db.find_similar_images(features=features, max_results=300, similarity_threshold=0.5)

        # Normalize paths to use forward slashes
        similar_image_urls = [
            url_for('send_image', filename=os.path.relpath(img, app.config['UPLOAD_FOLDER']).replace("\\", "/"))
            for img in similar_images
        ]

        # Serve the uploaded image from the temporary directory
        uploaded_image_url = url_for('send_temp_image', temp_dir=temp_dir, filename=file.filename)

        # Render the template with the results
        return render_template('index.html', uploaded_image=uploaded_image_url, similar_images=similar_image_urls)

@app.route('/search', methods=['POST'])
def search_by_text():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'No query provided.'}), 400
    
    # First, find images that match the query by name
    matching_images = db.find_similar_images(query=query, max_results=1)
    
    if not matching_images:
        return jsonify({'error': 'No images found with the given name.'}), 404
    
    # Use the first matching image to find similar images
    first_match = matching_images[0]
    features = extract_features(first_match)
    similar_images = db.find_similar_images(features=features, max_results=300, similarity_threshold=0.5)

    # Normalize paths to use forward slashes
    similar_image_urls = [
        url_for('send_image', filename=os.path.relpath(img, app.config['UPLOAD_FOLDER']).replace("\\", "/"))
        for img in similar_images
    ]

    return render_template('index.html', uploaded_image=first_match, similar_images=similar_image_urls)

@app.route('/temp/<path:temp_dir>/<path:filename>')
def send_temp_image(temp_dir, filename):
    return send_from_directory(temp_dir, filename)

@app.route('/static/images/<path:filename>')
def send_image(filename):
    # Serve the image from the local static/images path
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download_selected', methods=['POST'])
def download_selected():
    selected_images = request.form.getlist('selected_images')
    if not selected_images:
        return jsonify({'error': 'No images selected.'}), 400
    
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for image_path in selected_images:
            # Normalize the path
            image_path_normalized = os.path.normpath(image_path.replace('/static/images/', '').replace('%20', ' '))
            image_full_path = os.path.join(app.config['UPLOAD_FOLDER'], image_path_normalized)

            if os.path.exists(image_full_path):
                image_name = os.path.basename(image_full_path)
                zip_file.write(image_full_path, image_name)
            else:
                return jsonify({'error': f'File not found: {image_full_path}'}), 404
    
    zip_buffer.seek(0)
    
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='selected_images.zip')

def async_update_database(hard_update=False):
    print("Starting async database update...")
    if hard_update:
        socketio.emit('hard_update_start', namespace='/')
        # Clear the database before repopulating
        db.clear_database()
    
    socketio.emit('update_status', {'message': 'Starting database update...'}, namespace='/')
    processed_images = db.populate_database(app.config['UPLOAD_FOLDER'], hard_update)
    if processed_images:
        total_images = len(processed_images)
        for i, img_path in enumerate(processed_images):
            progress = int((i + 1) / total_images * 100)
            socketio.emit('progress_update', {'progress': progress}, namespace='/')
    print("Async database update complete.")
    socketio.emit('update_status', {'message': 'Database update complete.'}, namespace='/')
    if hard_update:
        socketio.emit('hard_update_end', namespace='/')

@app.route('/update_database', methods=['POST'])
def update_database():
    print("Updating database...")
    thread = threading.Thread(target=async_update_database, kwargs={'hard_update': False})
    thread.start()
    return jsonify({'message': 'Database update started'}), 202

@app.route('/hard_update_database', methods=['POST'])
def hard_update_database():
    print("Hard updating database...")
    thread = threading.Thread(target=async_update_database, kwargs={'hard_update': True})
    thread.start()
    return jsonify({'message': 'Hard database update started'}), 202

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
