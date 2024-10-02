import tkinter as tk
import random
import json
import os
import winsound


class AdventureGame:
    def __init__(self, master):
        self.master = master
        master.title("Adventure of John Doe")
        master.geometry("600x600")
        master.config(bg="#2c3e50")

        # Game variables
        self.inventory = []
        self.quest_item = None
        self.health = 100

        # Title Label
        self.title_label = tk.Label(master, text="Adventure of John Doe", bg="#2c3e50", fg="#e67e22",
                                    font=("Arial", 24, "bold"))
        self.title_label.pack(pady=10)

        # History Display
        self.history = tk.Text(master, height=10, width=70, state='disabled', bg="#34495e", fg="white",
                               font=("Arial", 12), wrap=tk.WORD)
        self.history.pack(pady=10)

        # Game Status Frame
        self.status_frame = tk.Frame(master, bg="#34495e")
        self.status_frame.pack(pady=10, padx=10, fill=tk.X)

        self.inventory_label = tk.Label(self.status_frame, text="Inventory: []", bg="#34495e", fg="white",
                                        font=("Arial", 12))
        self.inventory_label.pack(side=tk.LEFT, padx=5)

        self.health_label = tk.Label(self.status_frame, text="Health: 100", bg="#34495e", fg="white",
                                     font=("Arial", 12))
        self.health_label.pack(side=tk.LEFT, padx=5)

        # Button Frame
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        # Load game if it exists
        self.load_game()

        # Save Button
        self.save_button = tk.Button(master, text="Save Game", command=self.save_game, bg="#2980b9", fg="white",
                                     font=("Arial", 12))
        self.save_button.pack(pady=5)

    def append_to_history(self, message):
        self.history.config(state='normal')
        self.history.insert(tk.END, message + "\n")
        self.history.config(state='disabled')
        self.history.see(tk.END)

    def update_inventory_display(self):
        self.inventory_label.config(text=f"Inventory: {self.inventory if self.inventory else '[]'}")

    def play_sound(self, sound):
        if os.path.exists(sound):
            winsound.PlaySound(sound, winsound.SND_FILENAME)

    def clear_choice_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    def add_choice_button(self, text, command):
        button = tk.Button(self.button_frame, text=text, command=command, bg="#27ae60", fg="white", font=("Arial", 12))
        button.pack(pady=2, fill=tk.X)
        button.bind("<Enter>", lambda e: button.config(bg="#2ecc71"))
        button.bind("<Leave>", lambda e: button.config(bg="#27ae60"))

    def start_game(self):
        self.inventory.clear()  # Clear inventory for a new game
        self.health = 100  # Reset health
        self.quest_item = random.choice(["a golden key", "a lost artifact"])
        self.append_to_history("You find yourself in a dark and eerie forest.")
        self.append_to_history("Your goal is to find a way out.")
        self.append_to_history(f"Current Quest: Find {self.quest_item}.")
        self.append_to_history("You can either go left towards a faint light or right towards a strange sound.")

        self.update_health_display()
        self.add_choice_button("Go Left", self.left_path)
        self.add_choice_button("Go Right", self.right_path)

    def update_health_display(self):
        self.health_label.config(text=f"Health: {self.health}")

    def left_path(self):
        self.clear_choice_buttons()
        self.append_to_history("You walk towards the faint light...")
        self.append_to_history("As you get closer, you see a glowing portal!")
        self.append_to_history("Do you want to enter the portal or turn back?")
        self.add_choice_button("Enter the Portal", self.magical_land)
        self.add_choice_button("Turn Back", self.start_game)

    def magical_land(self):
        self.clear_choice_buttons()
        self.append_to_history("You enter the portal and find yourself in a magical land!")
        self.append_to_history("You can explore, look for a way out, or use an item (if you have any).")
        self.add_choice_button("Explore", self.find_item)
        self.add_choice_button("Look for a Way Out", self.check_quest_completion)
        self.add_choice_button("View Inventory", self.view_inventory)

    def find_item(self):
        self.clear_choice_buttons()
        items = ["a magical sword", "a healing potion", "a mysterious key", "a golden key", "a lost artifact"]
        found_item = random.choice(items)
        self.inventory.append(found_item)
        self.play_sound("item_found.wav")  # Sound for finding an item
        self.append_to_history(f"You found {found_item}!")
        self.update_inventory_display()
        self.add_choice_button("Keep Exploring", self.find_item)
        self.add_choice_button("Return", self.magical_land)

    def right_path(self):
        self.clear_choice_buttons()
        self.append_to_history("You follow the strange sound...")
        encounter = random.choice(["a friendly creature", "a hostile creature"])

        if encounter == "a friendly creature":
            self.friendly_creature()
        else:
            self.hostile_creature()

    def friendly_creature(self):
        self.clear_choice_buttons()
        self.append_to_history("You come across a friendly creature!")
        self.append_to_history("It offers to help you find a way out of the forest.")

        if "a magical sword" in self.inventory:
            self.append_to_history("With your magical sword, you can defeat any obstacles.")
            self.check_quest_completion()
        else:
            self.append_to_history("Unfortunately, you don't have the tools to navigate through.")
            self.append_to_history("Game Over!")
            self.add_choice_button("Restart Game", self.start_game)

    def hostile_creature(self):
        self.clear_choice_buttons()
        self.append_to_history("You encounter a hostile creature!")
        self.append_to_history("It looks ready to attack.")
        self.add_choice_button("Fight", self.fight_creature)
        self.add_choice_button("Run", self.run_from_creature)

    def fight_creature(self):
        self.clear_choice_buttons()
        if "a magical sword" in self.inventory:
            self.append_to_history("You bravely fight and defeat the creature with your sword!")
            self.check_quest_completion()
        else:
            self.append_to_history("You try to fight but don't have the means to defend yourself.")
            self.append_to_history("Game Over!")
            self.add_choice_button("Restart Game", self.start_game)

    def run_from_creature(self):
        self.clear_choice_buttons()
        self.append_to_history("You run as fast as you can...")
        self.health -= 20  # Lose health when running
        self.update_health_display()

        if self.health <= 0:
            self.append_to_history("You were too injured to escape. Game Over!")
            self.add_choice_button("Restart Game", self.start_game)
        else:
            self.append_to_history("But you trip and fall, and the creature catches up to you.")
            self.append_to_history("You barely escape, but you lost some health.")
            self.add_choice_button("Continue", self.magical_land)

    def check_quest_completion(self):
        self.clear_choice_buttons()
        if self.quest_item in self.inventory:
            self.append_to_history(f"You found the {self.quest_item}!")
            self.append_to_history("Congratulations, you've completed your quest!")
            self.add_choice_button("Restart Game", self.start_game)
        else:
            self.append_to_history("You still need to find the quest item.")
            self.add_choice_button("Explore More", self.magical_land)
            self.add_choice_button("Check Inventory", self.view_inventory)

    def view_inventory(self):
        self.clear_choice_buttons()
        if self.inventory:
            items = ", ".join(self.inventory)
            self.append_to_history(f"Your inventory: {items}.")
        else:
            self.append_to_history("Your inventory is empty.")
        self.add_choice_button("Continue", self.magical_land)

    def save_game(self):
        save_data = {
            'inventory': self.inventory,
            'quest_item': self.quest_item,
            'health': self.health
        }
        with open('save_game.json', 'w') as f:
            json.dump(save_data, f)
        self.append_to_history("Game saved!")

    def load_game(self):
        if os.path.exists('save_game.json'):
            with open('save_game.json', 'r') as f:
                save_data = json.load(f)
                self.inventory = save_data.get('inventory', [])
                self.quest_item = save_data.get('quest_item', None)
                self.health = save_data.get('health', 100)  # Default to 100 if not found
                self.update_health_display()
                self.append_to_history("Game loaded!")
                self.start_game()  # Restart the game to reset the context
        else:
            self.start_game()  # If no save exists, start a new game


if __name__ == "__main__":
    root = tk.Tk()
    game = AdventureGame(root)
    root.mainloop()
