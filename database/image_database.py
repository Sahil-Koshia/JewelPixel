
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from utils.image_processing import extract_features

class ImageDatabase:
    def __init__(self, socketio, db_path='database/images.npy'):
        self.socketio = socketio
        self.db_path = db_path
        self.images = []
        self.features = []
        if os.path.exists(self.db_path):
            self.load_database()
        else:
            print("No existing database found, starting fresh.")
        print(f"Database loaded with {len(self.images)} images.")

    def add_image(self, img_path, features=None):
        if img_path in self.images:
            return False  # Image already in database
        if features is None:
            features = extract_features(img_path)
        self.images.append(img_path)
        self.features.append(features)
        return True

    def save_database(self):
        np.save(self.db_path, {'images': self.images, 'features': self.features})
        print(f"Database saved with {len(self.images)} images.")

    def load_database(self):
        data = np.load(self.db_path, allow_pickle=True).item()
        self.images = data['images']
        self.features = data['features']
        print(f"Loaded {len(self.images)} unique images from database.")

    def clear_database(self):
        self.images = []
        self.features = []
        print("Database cleared.")

    def find_similar_images(self, features=None, query=None, max_results=50, similarity_threshold=0.5):
        if query:
            # Search by name
            return self.search_by_name(query, max_results)
        if features is not None:
            # Search by image features
            similarities = cosine_similarity([features], self.features)
            indices = np.argsort(similarities[0])[::-1]

            similar_images = []
            for index in indices:
                if len(similar_images) >= max_results:
                    break
                if similarities[0][index] >= similarity_threshold:
                    similar_images.append(self.images[index])
                else:
                    break
            return similar_images
        return []

    def search_by_name(self, query, max_results=50):
        matching_images = []
        query_lower = query.lower()
        for img_path in self.images:
            img_name = os.path.basename(img_path).lower()
            if query_lower in img_name:
                matching_images.append(img_path)
            if len(matching_images) >= max_results:
                break
        return matching_images

    def populate_database(self, image_folder, hard_update=False):
        print("Populating database...")
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')
        new_images = []
        for root, _, files in os.walk(image_folder):
            for filename in files:
                if filename.lower().endswith(valid_extensions):
                    img_path = os.path.join(root, filename)
                    if img_path not in self.images or hard_update:
                        new_images.append(img_path)

        print(f"New images to add: {len(new_images)}")
        self.socketio.emit('update_status', {'message': f'Found {len(new_images)} new images.'})

        added_count = 0
        total_images = len(new_images)
        for i, img_path in enumerate(new_images):
            try:
                if self.add_image(img_path):
                    added_count += 1
                    self.socketio.emit('update_status', {'message': f'Added image: {img_path}'})
                    progress = int((i + 1) / total_images * 100)
                    self.socketio.emit('progress_update', {'progress': progress})
            except Exception as e:
                print(f"Failed to process {img_path}: {e}")
                self.socketio.emit('update_status', {'message': f'Failed to process {img_path}: {e}'})

        self.save_database()
        self.socketio.emit('update_status', {'message': f'Database population complete. Added {added_count} new images.'})
        print(f"Database population complete. Added {added_count} new images.")
