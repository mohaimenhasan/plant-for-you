import json
import os
import datetime

class PlayerData:
    """Manages player progress and game state data"""
    
    def __init__(self):
        self.save_file = 'player_data.json'
        
        # Default values
        self.plant_level = 1
        self.plant_growth = 0.0  # 0.0 to 1.0 for each level
        self.watered_today = False
        self.affirmation_done_today = False
        self.journal_entries = []
        self.unlocked_messages = [
            "You're at the beginning of an amazing journey!"
        ]
        self.last_login = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Try to load saved data
        self.load_data()
    
    def save_data(self):
        """Save player data to file"""
        data = {
            'plant_level': self.plant_level,
            'plant_growth': self.plant_growth,
            'watered_today': self.watered_today,
            'affirmation_done_today': self.affirmation_done_today,
            'journal_entries': self.journal_entries,
            'unlocked_messages': self.unlocked_messages,
            'last_login': self.last_login
        }
        
        try:
            with open(self.save_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        """Load player data from file"""
        if not os.path.exists(self.save_file):
            # No save file exists yet
            return
            
        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
                
            self.plant_level = data.get('plant_level', 1)
            self.plant_growth = data.get('plant_growth', 0.0)
            self.watered_today = data.get('watered_today', False)
            self.affirmation_done_today = data.get('affirmation_done_today', False)
            self.journal_entries = data.get('journal_entries', [])
            self.unlocked_messages = data.get('unlocked_messages', 
                                            ["You're at the beginning of an amazing journey!"])
            self.last_login = data.get('last_login', datetime.datetime.now().strftime("%Y-%m-%d"))
            
            # Check if it's a new day since last login
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            if today != self.last_login:
                self.reset_daily()
                self.last_login = today
                
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def reset_daily(self):
        """Reset daily activities"""
        self.watered_today = False
        self.affirmation_done_today = False
        self.save_data()
    
    def water_plant(self):
        """Water the plant to increase growth"""
        if not self.watered_today:
            self.watered_today = True
            self.add_growth(0.15)  # Add 15% growth
            return True
        return False
    
    def complete_affirmation(self):
        """Complete an affirmation challenge"""
        if not self.affirmation_done_today:
            self.affirmation_done_today = True
            self.add_growth(0.2)  # Add 20% growth
            return True
        return False
    
    def add_journal_entry(self, entry):
        """Add a new journal entry"""
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.journal_entries.append({
            'date': today,
            'text': entry
        })
        self.add_growth(0.1)  # Add 10% growth for journaling
        self.save_data()
    
    def add_growth(self, amount):
        """Add growth to the plant, level up if needed"""
        self.plant_growth += amount
        
        # Check for level up
        if self.plant_growth >= 1.0:
            self.level_up()
        
        self.save_data()
    
    def level_up(self):
        """Level up the plant and unlock new messages"""
        self.plant_level += 1
        self.plant_growth = 0.0
        
        # Unlock new message based on level
        messages = {
            2: "You're making great progress! Just like this plant, you're growing every day.",
            3: "Look how much you've grown! Remember, everyone starts somewhere.",
            4: "Your dedication is inspiring! You're proving that persistence pays off.",
            5: "You've reached level 5! Your journey in CS is just like this plant - needing care and patience.",
            6: "The plant is flourishing! Remember that doubt is normal, but don't let it stop you.",
            7: "Amazing growth! Similarly, your coding skills grow with each challenge you face.",
            8: "You've created something beautiful! Your potential in CS is just as limitless.",
            9: "Nearly at the top! Remember that even experts were beginners once.",
            10: "Maximum level reached! You've shown incredible persistence - carry this into your studies!"
        }
        
        if self.plant_level in messages:
            self.unlocked_messages.append(messages[self.plant_level])
