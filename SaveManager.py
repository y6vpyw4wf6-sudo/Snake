import os
import json
from datetime import datetime


class SaveManager:
    def __init__(self):
        pass
    
    def get_new_save_filename(self): #Save by date
        os.makedirs("saves", exist_ok=True)
    
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return f"saves/save_{timestamp}.json"    
    
    def get_auto_save_filename(self):
        os.makedirs("saves", exist_ok=True)
        
        return "saves/auto_save.json"
    
    def save(self, data, filename):   
        os.makedirs("saves", exist_ok=True)

        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
        except OSError:
            return
        
    def load(self, filename):
        if not os.path.exists(filename):
            return None
        
        try:
            with open(filename, "r") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            return None
            
        return data   
                 