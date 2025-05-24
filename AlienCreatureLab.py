import json
import random
import os


#---------------------------Alien Creature Lab-------------------------
# Define the folder to store save files
SAVE_FOLDER = "saves"
os.makedirs(SAVE_FOLDER, exist_ok=True)  # Ensure the folder exists


# Save alien data to a file
def save_game(alien):
    filename = input("Enter a save file name (e.g., alien001): ").strip()
    if not filename.endswith(".json"):
        filename += ".json"
    filepath = os.path.join(SAVE_FOLDER, filename)

    data = {
        "name": alien.name,
        "health": alien.health,
        "happiness": alien.happiness,
        "hunger": alien.hunger,
        "mutation_level": alien.mutation_level,
        "stage": alien.stage,
        "final_form": alien.final_form,
        "diary": alien.diary
    }

    with open(filepath, 'w') as f:
        json.dump(data, f)
    print(f"💾 Game saved to {filepath}!")


# Load alien data from a selected save file
def load_game():
    files = [f for f in os.listdir(SAVE_FOLDER) if f.endswith('.json')]
    if not files:
        print("❌ No save files found.")
        return None

    print("\nAvailable save files:")
    for i, fname in enumerate(files):
        print(f"{i + 1}. {fname}")

    while True:
        choice = input("Enter file number or name to load: ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                filename = files[idx]
                break
        elif choice in files:
            filename = choice
            break
        else:
            print("Invalid choice. Try again.")

    filepath = os.path.join(SAVE_FOLDER, filename)

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        alien = AlienCreature(data['name'])
        alien.health = data['health']
        alien.happiness = data['happiness']
        alien.hunger = data['hunger']
        alien.mutation_level = data['mutation_level']
        alien.stage = data['stage']
        alien.final_form = data['final_form']
        alien.diary = data['diary']
        print(f"🔁 Game loaded from {filename}!")
        return alien
    except Exception as e:
        print(f"⚠️ Error loading file: {e}")
        return None


# Delete a selected save file
def delete_save():
    files = [f for f in os.listdir(SAVE_FOLDER) if f.endswith('.json')]
    if not files:
        print("❌ No save files to delete.")
        return

    print("\n🗑️  Available save files:")
    for i, fname in enumerate(files):
        print(f"{i + 1}. {fname}")

    choice = input("Enter the number of the file to delete: ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            filename = files[idx]
            filepath = os.path.join(SAVE_FOLDER, filename)
            confirm = input(f"Are you sure you want to delete {filename}? (y/n): ")
            if confirm.lower() == 'y':
                os.remove(filepath)
                print(f"✅ Deleted {filename}")
            else:
                print("❎ Deletion canceled.")
        else:
            print("Invalid file number.")
    else:
        print("Invalid input.")


# Alien creature class with lifecycle and stats
class AlienCreature:
    def __init__(self, name):
        self.name = name
        self.health = 80
        self.happiness = 50
        self.hunger = 50
        self.mutation_level = 0
        self.stage = 'baby'
        self.final_form = None
        self.diary = []

    # Feeding interaction
    def feed(self):
        self.hunger = max(0, self.hunger - 20)
        self.health = min(100, self.health + 10)
        self.happiness = min(100, self.happiness + 5)
        print(f"{self.name} enjoyed the meal! 🥣")
        self.log_event(f"{self.name} was fed. +10 Health, -20 Hunger")

    # Light interaction - chance to mutate
    def expose_to_light(self):
        print("Exposing to alien light rays... ☀️")
        if random.random() < 0.4:
            self.mutation_level += 1
            print(f"{self.name} is mutating! 🧬 Mutation Level: {self.mutation_level}")
            self.log_event(f"{self.name} mutated! Mutation level is now {self.mutation_level}")
        else:
            print("Nothing happened.")
            self.log_event(f"{self.name} was exposed to light but nothing happened.")

    # Sound interaction - increases happiness
    def play_sound(self):
        print("Playing cosmic frequencies... 🎵")
        self.happiness = min(100, self.happiness + 10)
        if random.random() < 0.2:
            self.mutation_level += 1
            print(f"{self.name} reacted strangely... more mutations!")
            self.log_event(f"{self.name} mutated from sound!")
        else:
            print("The creature looks happy.")
            self.log_event(f"{self.name} mutated from sound!")

    # Simulate the passing of a day and update status
    def next_day(self):
        self.hunger = min(100, self.hunger + 10)
        self.happiness = max(0, self.happiness - 5)
        self.health = max(0, self.health - self.hunger // 20)

        # Final Form passive abilities
        if self.stage == 'evolved':
            if self.final_form == 'PsiBrain':
                self.happiness = min(100, self.happiness + 5)
            elif self.final_form == 'BioBeast':
                self.health = min(100, self.health + 10)
            elif self.final_form == 'VoidGhost':
                self.hunger = max(0, self.hunger - 5)
                self.happiness = min(100, self.happiness + 3)

        # Evolution conditions
        if self.mutation_level >= 3 and self.stage == 'baby':
            self.stage = 'teen'
            self.log_event(f"{self.name} evolved into a TEEN form! 👾")
        elif self.mutation_level >= 6 and self.stage == 'teen':
            self.stage = 'evolved'
            self.final_form = random.choice(['PsiBrain', 'BioBeast', 'VoidGhost'])
            self.log_event(f"{self.name} mutated into FINAL FORM: {self.final_form}! 🔥")

    # Display alien's status
    def status(self):
        face = "👶" if self.stage == 'baby' else "👾" if self.stage == 'teen' else (
            "🧠✨" if self.final_form == 'PsiBrain' else
            "🐲🦠" if self.final_form == 'BioBeast' else
            "👻🌌" if self.final_form == 'VoidGhost' else "👽"
        )
        title = f" {self.name}'s Status {face} "
        border = "=" * len(title)

        print("\n" + border)
        print(title)
        print(border)
        print(f"  Stage          : {self.stage}")
        print(f"  Health         : {self.health}/100")
        print(f"  Happiness      : {self.happiness}/100")
        print(f"  Hunger         : {self.hunger}/100")
        print(f"  Mutation Level : {self.mutation_level}")
        print(f"  Final Form     : {self.final_form if self.final_form else 'N/A'}")
        print(border + "\n")

    # Log important events with timestamp
    def log_event(self, message):
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        entry = f"[{timestamp}] {message}"
        self.diary.append(entry)
        print(entry)

    # Print evolution history
    def view_diary(self):
        print("\n==== Evolution Diary ====")
        for entry in self.diary:
            print(entry)
        print("=========================\n")


# Main game loop
def main():
    print("Welcome to Alien Creature Lab! 👩‍🔬👽")
    choice = input("Do you want to load a saved alien? (y/n): ")
    alien = load_game() if choice.lower() == 'y' else None
    if not alien:
        name = input("Name your alien: ")
        alien = AlienCreature(name)

    while True:
        alien.status()
        print("1. Feed | 2. Light | 3. Sound | 4. Next Day")
        print("5. View Diary | 6. Save Game | 7. Delete Save | 8. Exit")
        choice = input("Choice: ")

        if choice == '1':
            alien.feed()
        elif choice == '2':
            alien.expose_to_light()
        elif choice == '3':
            alien.play_sound()
        elif choice == '4':
            alien.next_day()
        elif choice == '5':
            alien.view_diary()
        elif choice == '6':
            save_game(alien)
        elif choice == '7':
            delete_save()
        elif choice == '8':
            print("Bye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
