"""
Simplified version of MotivaPlant that can run without pygame.
This uses tkinter which comes with Python by default.
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import json
import random
import datetime

class SimpleMotivaPlant:
    def __init__(self, root):
        self.root = root
        root.title("MotivaPlant - Simple Version")
        root.geometry("800x600")
        root.configure(bg="#eef7f6")
        
        # Initialize player data
        self.load_player_data()
        
        # Set up the interface
        self.setup_ui()
        
    def load_player_data(self):
        """Load player data or create new if none exists"""
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
        if os.path.exists(self.save_file):
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
                messagebox.showerror("Error", f"Failed to load save data: {e}")
    
    def save_player_data(self):
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
            messagebox.showerror("Error", f"Failed to save data: {e}")
    
    def reset_daily(self):
        """Reset daily activities"""
        self.watered_today = False
        self.affirmation_done_today = False
        self.save_player_data()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Title label
        title_label = tk.Label(
            self.root, 
            text="MotivaPlant", 
            font=("Arial", 24, "bold"),
            bg="#eef7f6", 
            fg="#2a7d53"
        )
        title_label.pack(pady=20)
        
        # Plant frame
        plant_frame = tk.Frame(self.root, bg="#eef7f6")
        plant_frame.pack(pady=20)
        
        # Plant visual (simple text-based)
        self.plant_label = tk.Label(
            plant_frame,
            text=self.get_plant_visual(),
            font=("Courier", 14),
            bg="#eef7f6",
            fg="#306630",
            justify="left"
        )
        self.plant_label.pack()
        
        # Plant info
        info_text = f"Plant Level: {self.plant_level}\n"
        info_text += f"Growth: {int(self.plant_growth * 100)}%\n"
        info_text += f"Watered Today: {'Yes' if self.watered_today else 'No'}\n"
        info_text += f"Daily Affirmation: {'Completed' if self.affirmation_done_today else 'Not Completed'}"
        
        self.info_label = tk.Label(
            plant_frame,
            text=info_text,
            font=("Arial", 12),
            bg="#eef7f6",
            justify="left"
        )
        self.info_label.pack(pady=10)
        
        # Message display
        self.message_display = tk.Label(
            self.root,
            text=self.unlocked_messages[-1] if self.unlocked_messages else "",
            font=("Arial", 12, "italic"),
            bg="#f0f8ff",
            fg="#333",
            wraplength=600,
            pady=10
        )
        self.message_display.pack(fill="x", padx=20)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg="#eef7f6")
        button_frame.pack(pady=20)
        
        # Water button
        water_button = tk.Button(
            button_frame,
            text="Water Plant",
            font=("Arial", 12),
            command=self.water_plant,
            bg="#5bc0de",
            fg="white",
            padx=20,
            pady=10,
            state="normal" if not self.watered_today else "disabled"
        )
        water_button.grid(row=0, column=0, padx=10)
        
        # Affirmation button
        affirm_button = tk.Button(
            button_frame,
            text="Daily Affirmation",
            font=("Arial", 12),
            command=self.show_affirmation,
            bg="#9370db",
            fg="white",
            padx=20,
            pady=10,
            state="normal" if not self.affirmation_done_today else "disabled"
        )
        affirm_button.grid(row=0, column=1, padx=10)
        
        # Journal button
        journal_button = tk.Button(
            button_frame,
            text="Journal",
            font=("Arial", 12),
            command=self.show_journal,
            bg="#5cb85c",
            fg="white",
            padx=20,
            pady=10
        )
        journal_button.grid(row=0, column=2, padx=10)
        
        # Information about full version
        info_label = tk.Label(
            self.root,
            text="Note: This is a simplified version of MotivaPlant.\nFor the full graphical experience, please install pygame and run the main version.",
            font=("Arial", 10),
            bg="#eef7f6",
            fg="#666"
        )
        info_label.pack(side="bottom", pady=10)
    
    def get_plant_visual(self):
        """Return ASCII art representation of the plant based on level"""
        plant_visuals = [
            # Level 1
            """
      _
     / \\
    /___\\
    """,
            # Level 2
            """
      _
     / \\
    /___\\
     | |
    """,
            # Level 3
            """
      _
     / \\
    /___\\
     | |
     | |
    """,
            # Level 4
            """
      _
     / \\
    /___\\
     | |
     | |
    _|_|_
    """,
            # Level 5
            """
      _
     / \\
    /___\\
     | |
     |_|_
    /   \\
    """,
            # Level 6
            """
     \\_/
    _|_|_
     | |
     | |
    _|_|_
    """,
            # Level 7
            """
     \\_/
    _|_|_
    \\   /
     | |
    _|_|_
    """,
            # Level 8
            """
      *
     \\*/
    _|_|_
    \\   /
     | |
    _|_|_
    """,
            # Level 9
            """
      *
     \\*/
    _|*|_
    \\   /
     | |
    _|_|_
    """,
            # Level 10
            """
     \\*/
     /|\\
    /*|*\\
    \\   /
     | |
    _|_|_
    """
        ]
        
        # Calculate effective level including growth
        effective_level = min(10, int(self.plant_level - 1 + self.plant_growth))
        return plant_visuals[effective_level]
    
    def water_plant(self):
        """Handle watering the plant"""
        if not self.watered_today:
            self.watered_today = True
            self.plant_growth += 0.15  # Add 15% growth
            
            # Check for level up
            if self.plant_growth >= 1.0:
                self.level_up()
            
            self.save_player_data()
            self.update_display()
            messagebox.showinfo("Watered!", "You watered your plant! It looks happier now.")
    
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
            messagebox.showinfo("Level Up!", f"Your plant grew to level {self.plant_level}!")
    
    def update_display(self):
        """Update the plant visual and info display"""
        self.plant_label.config(text=self.get_plant_visual())
        
        info_text = f"Plant Level: {self.plant_level}\n"
        info_text += f"Growth: {int(self.plant_growth * 100)}%\n"
        info_text += f"Watered Today: {'Yes' if self.watered_today else 'No'}\n"
        info_text += f"Daily Affirmation: {'Completed' if self.affirmation_done_today else 'Not Completed'}"
        self.info_label.config(text=info_text)
        
        # Update message
        self.message_display.config(text=self.unlocked_messages[-1] if self.unlocked_messages else "")
        
        # Force the root window to update
        self.root.update_idletasks()
    
    def show_affirmation(self):
        """Show the affirmation dialog"""
        if self.affirmation_done_today:
            messagebox.showinfo("Already Done", "You've already completed your affirmation for today. Come back tomorrow!")
            return
            
        # Create a toplevel window for the affirmation exercise
        affirm_window = tk.Toplevel(self.root)
        affirm_window.title("Daily Affirmation")
        affirm_window.geometry("600x500")
        affirm_window.configure(bg="#f0e6fa")
        
        # Set up the affirmation exercise
        tk.Label(
            affirm_window, 
            text="Daily Affirmation", 
            font=("Arial", 18, "bold"),
            bg="#f0e6fa"
        ).pack(pady=20)
        
        # Randomly select an affirmation
        affirmations = [
            "I am capable of learning difficult concepts with time and practice.",
            "My worth is not defined by my grades or performance.",
            "I belong in computer science just as much as anyone else.",
            "Making mistakes is how I learn and grow stronger.",
            "I don't need to know everything right away - learning is a journey.",
            "I have unique perspectives and ideas that are valuable to my field.",
            "I can overcome challenges by breaking them into smaller steps.",
            "Asking for help shows wisdom, not weakness.",
            "I am resilient and can adapt to new challenges.",
            "Today I choose to focus on progress, not perfection."
        ]
        
        affirmation = random.choice(affirmations)
        
        instruction_text = "Repeat this affirmation to yourself three times:\n\n"
        
        tk.Label(
            affirm_window,
            text=instruction_text,
            font=("Arial", 12),
            bg="#f0e6fa",
            justify="left"
        ).pack(pady=10)
        
        affirm_text = tk.Label(
            affirm_window,
            text=affirmation,
            font=("Arial", 14, "italic"),
            bg="#e6d4f4",
            fg="#333",
            wraplength=500,
            padx=20,
            pady=20
        )
        affirm_text.pack(fill="x", padx=20)
        
        # Thought challenge
        challenges = [
            {
                "prompt": "When I don't understand a concept immediately, it means...",
                "options": [
                    "I'm not smart enough for this field.",
                    "This is a normal part of learning something complex."
                ],
                "correct": 1
            },
            {
                "prompt": "When I see others in my class who seem to understand everything...",
                "options": [
                    "They probably have moments of confusion too, I just don't see it.",
                    "They must be naturally smarter than me, so I'll never catch up."
                ],
                "correct": 0
            },
            {
                "prompt": "When I need to ask for help in class or office hours...",
                "options": [
                    "It shows I'm not cut out for computer science.",
                    "It shows I'm taking active steps to learn and grow."
                ],
                "correct": 1
            }
        ]
        
        challenge = random.choice(challenges)
        
        tk.Label(
            affirm_window,
            text="\nLet's challenge negative thoughts:\n",
            font=("Arial", 12),
            bg="#f0e6fa"
        ).pack(pady=10)
        
        tk.Label(
            affirm_window,
            text=challenge["prompt"],
            font=("Arial", 12),
            bg="#f0e6fa",
            wraplength=500
        ).pack(pady=5)
        
        # Variable to store the selected option
        selected_option = tk.IntVar()
        
        # Create radio buttons for the options
        for i, option in enumerate(challenge["options"]):
            tk.Radiobutton(
                affirm_window,
                text=option,
                variable=selected_option,
                value=i,
                font=("Arial", 11),
                bg="#f0e6fa",
                wraplength=500,
                justify="left",
                padx=20
            ).pack(anchor="w", padx=50, pady=5)
        
        # Button to complete the exercise
        def complete_affirmation():
            selected = selected_option.get()
            if selected == challenge["correct"]:
                messagebox.showinfo("Great Choice!", "That's a healthy perspective! Regular practice of positive self-talk helps build confidence and resilience over time.")
            else:
                messagebox.showinfo("Let's Reframe", "Try to replace negative thoughts with more balanced ones. It's natural to have these thoughts, but we can practice reframing them.")
            
            # Mark as completed
            self.affirmation_done_today = True
            self.plant_growth += 0.2  # Add 20% growth
            
            # Check for level up
            if self.plant_growth >= 1.0:
                self.level_up()
            
            self.save_player_data()
            self.update_display()
            
            # Close the window
            affirm_window.destroy()
        
        tk.Button(
            affirm_window,
            text="Complete",
            font=("Arial", 12),
            command=complete_affirmation,
            bg="#9370db",
            fg="white",
            padx=20,
            pady=10
        ).pack(pady=20)
    
    def show_journal(self):
        """Show the journaling interface"""
        # Create a toplevel window for journaling
        journal_window = tk.Toplevel(self.root)
        journal_window.title("Journal")
        journal_window.geometry("700x600")
        journal_window.configure(bg="#f8f9fa")
        
        # Set up the journal interface
        tk.Label(
            journal_window, 
            text="Your Journal", 
            font=("Arial", 18, "bold"),
            bg="#f8f9fa"
        ).pack(pady=20)
        
        # Display previous entries
        entries_frame = tk.Frame(journal_window, bg="#f8f9fa")
        entries_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            entries_frame,
            text="Previous Entries:",
            font=("Arial", 12, "bold"),
            bg="#f8f9fa",
            anchor="w"
        ).pack(fill="x")
        
        entries_text = scrolledtext.ScrolledText(
            entries_frame,
            width=80,
            height=10,
            font=("Arial", 10),
            wrap=tk.WORD
        )
        entries_text.pack(fill="both", expand=True, pady=5)
        
        # Display entries
        entries_text.config(state=tk.NORMAL)
        entries_text.delete(1.0, tk.END)
        
        for entry in self.journal_entries:
            entries_text.insert(tk.END, f"[{entry['date']}]\n{entry['text']}\n\n")
        
        entries_text.config(state=tk.DISABLED)
        
        # Journal prompts
        prompts = [
            "What made you feel proud today?",
            "What's one thing you learned recently that surprised you?",
            "What small win can you celebrate today?",
            "If your future self could give you advice, what would they say?",
            "What's a challenge that felt impossible but you overcame?",
            "What would you do in your field if you knew you couldn't fail?",
            "What's something nice someone said that you could tell yourself?",
            "What's a skill you're better at than you give yourself credit for?",
            "What small step could you take today toward a goal?",
            "What would you try if other people's opinions didn't matter?"
        ]
        
        current_prompt = random.choice(prompts)
        
        # New entry section
        entry_frame = tk.Frame(journal_window, bg="#f8f9fa")
        entry_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            entry_frame,
            text="Today's Prompt:",
            font=("Arial", 12, "bold"),
            bg="#f8f9fa",
            anchor="w"
        ).pack(fill="x")
        
        tk.Label(
            entry_frame,
            text=current_prompt,
            font=("Arial", 11, "italic"),
            bg="#f8f9fa",
            fg="#555",
            wraplength=650,
            anchor="w"
        ).pack(fill="x", pady=5)
        
        tk.Label(
            entry_frame,
            text="Your Entry:",
            font=("Arial", 12, "bold"),
            bg="#f8f9fa",
            anchor="w"
        ).pack(fill="x", pady=5)
        
        entry_text = scrolledtext.ScrolledText(
            entry_frame,
            width=80,
            height=8,
            font=("Arial", 11),
            wrap=tk.WORD
        )
        entry_text.pack(fill="both", expand=True, pady=5)
        
        # Buttons
        button_frame = tk.Frame(journal_window, bg="#f8f9fa")
        button_frame.pack(pady=10)
        
        def new_prompt():
            nonlocal current_prompt
            current_prompt = random.choice(prompts)
            for widget in entry_frame.winfo_children():
                if isinstance(widget, tk.Label) and widget.cget("font") == ("Arial", 11, "italic"):
                    widget.config(text=current_prompt)
        
        def save_entry():
            entry_content = entry_text.get(1.0, tk.END).strip()
            if entry_content:
                today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                self.journal_entries.append({
                    'date': today,
                    'text': entry_content
                })
                self.plant_growth += 0.1  # Add 10% growth for journaling
                
                # Check for level up
                if self.plant_growth >= 1.0:
                    self.level_up()
                
                self.save_player_data()
                self.update_display()
                
                # Update entries display
                entries_text.config(state=tk.NORMAL)
                entries_text.delete(1.0, tk.END)
                
                for entry in self.journal_entries:
                    entries_text.insert(tk.END, f"[{entry['date']}]\n{entry['text']}\n\n")
                
                entries_text.config(state=tk.DISABLED)
                
                # Clear entry text
                entry_text.delete(1.0, tk.END)
                
                messagebox.showinfo("Entry Saved", "Your journal entry has been saved!")
        
        tk.Button(
            button_frame,
            text="New Prompt",
            font=("Arial", 11),
            command=new_prompt,
            bg="#f0ad4e",
            fg="white",
            padx=10,
            pady=5
        ).grid(row=0, column=0, padx=10)
        
        tk.Button(
            button_frame,
            text="Save Entry",
            font=("Arial", 11),
            command=save_entry,
            bg="#5cb85c",
            fg="white",
            padx=10,
            pady=5
        ).grid(row=0, column=1, padx=10)
        
        tk.Button(
            button_frame,
            text="Close",
            font=("Arial", 11),
            command=journal_window.destroy,
            bg="#d9534f",
            fg="white",
            padx=10,
            pady=5
        ).grid(row=0, column=2, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleMotivaPlant(root)
    root.mainloop()