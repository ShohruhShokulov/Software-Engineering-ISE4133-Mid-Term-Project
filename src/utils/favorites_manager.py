import json
import os

class FavoritesManager:
    def __init__(self):
        self.favorites_file = 'data/favorites.json'
        self.ensure_data_dir()
        self.favorites = self.load_favorites()
    
    def ensure_data_dir(self):
        os.makedirs('data', exist_ok=True)
        if not os.path.exists(self.favorites_file):
            with open(self.favorites_file, 'w') as f:
                json.dump({}, f)
    
    def load_favorites(self):
        try:
            with open(self.favorites_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_favorites(self):
        with open(self.favorites_file, 'w') as f:
            json.dump(self.favorites, f, indent=2)
    
    def add_favorite(self, name, location):
        self.favorites[name.lower()] = location
        self.save_favorites()
        return True
    
    def remove_favorite(self, name):
        if name.lower() in self.favorites:
            del self.favorites[name.lower()]
            self.save_favorites()
            return True
        return False
    
    def get_favorite(self, name):
        return self.favorites.get(name.lower())
    
    def list_favorites(self):
        return self.favorites