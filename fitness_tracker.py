import json
import os
import shlex


class FitnessTracker:
    def __init__(self, db_file='trainees.json'):
        self.db_file = db_file
        self.trainees = self.load_trainees()

    def load_trainees(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []

    def save_trainees(self):
        with open(self.db_file, 'w') as file:
            json.dump(self.trainees, file, indent=4)

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def main_menu(self):
        while True:
            self.clear_console()
            print("\nWelcome to FitnessTracker")
            print("Having trouble keeping track of your trainees? Add them to your list! You can even add goals to their profile!")
            print("1. Add a trainee")
            print("2. View existing trainees")
            print("> Type an option and hit enter")
            option = input("> ")

            if option == '1':
                self.add_trainee()
            elif option == '2':
                self.view_trainees()
            else:
                print("Invalid option. Please try again.")

    def add_trainee(self):
        self.clear_console()
        new_trainee = {}
        while True:
            print("\nAdd a Trainee")
            print(
                'Add their profile information! Use the following format: "Key" "Value", then hit enter.')
            print(
                "Made a mistake? That's ok! Just type UNDO then hit enter and the last entry will be removed.")
            print(
                "When you're done adding to their profile, type BACK to exit back to the main menu.")
            if new_trainee:
                print("\nCurrent Profile:")
                for key, value in new_trainee.items():
                    print(f"{key}: {value}")
            profile_info = input("> Add profile information: ")

            if profile_info.lower() == 'back':
                if new_trainee:
                    new_trainee['goals'] = []
                    self.trainees.append(new_trainee)
                    self.save_trainees()
                break
            elif profile_info.lower() == 'undo':
                if new_trainee:
                    last_key = list(new_trainee.keys())[-1]
                    new_trainee.pop(last_key)
                    print(f"Removed last entry: {last_key}")
                else:
                    print("No entries to remove.")
            else:
                try:
                    parsed_info = shlex.split(profile_info)
                    if len(parsed_info) == 2:
                        key, value = parsed_info
                        new_trainee[key.lower()] = value
                    else:
                        print(
                            "Invalid format. Please use the format: \"Key\" \"Value\".")
                except ValueError:
                    print("Invalid format. Please use the format: \"Key\" \"Value\".")

    def view_trainees(self):
        self.clear_console()
        while True:
            if not self.trainees:
                print("\nNo trainees available.")
                break

            print("\nExisting Trainees")
            for i, trainee in enumerate(self.trainees, start=1):
                print(f"{i}. {trainee.get('name', 'Unnamed')}")

            print(
                "> Enter the trainee's number to view their profile or type BACK to exit back to the main menu.")
            option = input("> ")

            if option.lower() == 'back':
                break
            elif option.isdigit() and 1 <= int(option) <= len(self.trainees):
                self.view_trainee_profile(int(option) - 1)
            else:
                print("Invalid option. Please try again.")

    def view_trainee_profile(self, index):
        self.clear_console()
        while True:
            trainee = self.trainees[index]
            print(f"\nTrainee's Profile")
            for key, value in trainee.items():
                if key != 'goals':
                    print(f"{key}: {value}")
            print("You can type EDIT to edit their profile, GOAL to edit their goals, or BACK to go back to the list of existing trainees.")
            print('To delete this trainee, type DELETE "their name".')
            option = input("> ")

            if option.lower() == 'back':
                self.save_trainees()
                break
            elif option.lower() == 'edit':
                self.edit_trainee_profile(index)
            elif option.lower() == 'goal':
                self.edit_trainee_goals(index)
            elif option.lower().startswith('delete'):
                try:
                    _, name = shlex.split(option)
                    if name == trainee.get('name'):
                        del self.trainees[index]
                        self.save_trainees()
                        print(f"Trainee {name} has been deleted.")
                        break
                    else:
                        print("The name provided does not match the current trainee.")
                except ValueError:
                    print('Invalid format. Please use the format: DELETE "their name".')
            else:
                print("Invalid option. Please try again.")

    def edit_trainee_profile(self, index):
        self.clear_console()
        change_history = []
        while True:
            trainee = self.trainees[index]
            print(f"\nEdit {trainee.get('name', 'Unnamed')}'s Profile")
            print('To update an existing field, add a new field, use the following format: "Key" "Value", then hit enter.')
            print("To remove a field, type DELETE then the key like \"Name\".")
            print(
                "Made a mistake? That's ok! Just type UNDO then hit enter and the last update will be reverted.")
            print(
                "When you're done adding to their profile, type BACK to exit the profile editor.")
            print(f"\nCurrent Profile:")
            for key, value in trainee.items():
                if key != 'goals':
                    print(f"{key}: {value}")
            option = input("> ")

            if option.lower() == 'back':
                self.save_trainees()
                break
            elif option.lower().startswith('delete'):
                _, key = option.split()
                if key in trainee:
                    change_history.append(('delete', key, trainee[key]))
                    trainee.pop(key)
                    print(f"Removed field: {key}")
                else:
                    print(f"No such field: {key}")
            elif option.lower() == 'undo':
                if change_history:
                    action, key, value = change_history.pop()
                    if action == 'update':
                        trainee[key] = value
                    elif action == 'delete':
                        trainee[key] = value
                    print(f"Undid the last change: {key} restored to {value}")
                else:
                    print("No actions to undo.")
            else:
                try:
                    parsed_info = shlex.split(option)
                    if len(parsed_info) == 2:
                        key, value = parsed_info
                        if key in trainee:
                            change_history.append(
                                ('update', key, trainee[key]))
                        trainee[key.lower()] = value
                        print(f"Updated {key}: {value}")
                    else:
                        print(
                            "Invalid format. Please use the format: \"Key\" \"Value\".")
                except ValueError:
                    print("Invalid format. Please use the format: \"Key\" \"Value\".")

    def edit_trainee_goals(self, index):
        self.clear_console()
        change_history = []
        while True:
            trainee = self.trainees[index]
            print(f"\nEdit {trainee.get('name', 'Unnamed')}'s Goals")
            print(
                'To add a new goal, use the following format: goal "new goal in quotes"')
            print("To remove a field, type DELETE then the goal number.")
            print(
                "Made a mistake? That's ok! Just type UNDO then hit enter and the last update will be reverted.")
            print(
                "When you're done adding to their goals, type BACK to exit the goal editor.")
            if trainee['goals']:
                for i, goal in enumerate(trainee['goals'], start=1):
                    print(f"{i}. {goal}")
            else:
                print("No goals added yet.")
            option = input("> ")

            if option.lower() == 'back':
                self.save_trainees()
                break
            elif option.lower().startswith('delete'):
                try:
                    _, goal_num = option.split()
                    goal_num = int(goal_num)
                    if 1 <= goal_num <= len(trainee['goals']):
                        change_history.append(
                            ('delete', goal_num, trainee['goals'][goal_num - 1]))
                        removed_goal = trainee['goals'].pop(goal_num - 1)
                        print(f"Removed goal: {removed_goal}")
                    else:
                        print("Invalid goal number.")
                except (ValueError, IndexError):
                    print("Invalid input. Please use the format: DELETE goal_number")
            elif option.lower() == 'undo':
                if change_history:
                    action, goal_num, value = change_history.pop()
                    if action == 'delete':
                        trainee['goals'].insert(goal_num - 1, value)
                    print(
                        f"Undid the last change: goal {goal_num} restored to {value}")
                else:
                    print("No actions to undo.")
            elif option.lower().startswith('goal'):
                try:
                    _, new_goal = shlex.split(option, maxsplit=1)
                    change_history.append(
                        ('update', len(trainee['goals']) + 1, new_goal))
                    trainee['goals'].append(new_goal)
                    print(f"Added goal: {new_goal}")
                except ValueError:
                    print(
                        "Invalid format. Please use the format: goal \"new goal in quotes\".")
            else:
                print(
                    "Invalid command. Please use the format: goal \"new goal in quotes\" or DELETE goal_number.")


if __name__ == "__main__":
    app = FitnessTracker()
    app.main_menu()
