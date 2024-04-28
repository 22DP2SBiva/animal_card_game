# For managing data: reading/writing
import csv
class File_Manager:
    def find_account(self, name, password):
        # Check if account in CSV file
        # File path for the CSV file
        file = 'accounts.csv'
        found = False
        with open(file, 'r') as file:
            reader = csv.reader(file)
            next(reader) # Skip header line
            # Search for account within CSV file
            for line in reader:
                if line[0] == name and line[1] == password:
                    found = True
            return found  
    def add_account(self, name, password):
        found_account = File_Manager.find_account(self, name, password)
        if found_account is False:
            # File path for the CSV file
            file = 'accounts.csv'
            account = [name, password]
            account = ','.join(account)
            # Open the file in append mode
            with open(file, 'a') as file:
                # Append data to the CSV file
                file.write("\n"+account)
            # Print a confirmation message
            print(f"CSV file '{file}' appended to successfully.")
        else:
            print("Account already exists.")
    def login(self, name, password):
        # Check if account in CSV file
        found_account = File_Manager.find_account(self, name, password)
        if found_account:
            print("Successfully logged in.")
    def change_options(self, name, password, max_card_count, new_card_count, background, music_volume, sfx_volume):
        # Guest user
        if name is "" and password is "":
            file = 'options.csv'
            account = [name, password, max_card_count, new_card_count, background, music_volume, sfx_volume]
            print(account)
            with open(file, 'r', newline='') as file:
                reader = csv.reader(file)
                data = list(reader)
            # Replace default values (always at index 1) with new values
            data[1] = account
            print(data)
            print(data[1])
            # Rewrite data back to the CSV file
            file = 'options.csv'
            with open(file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
            print(f"CSV file '{file}' written to successfully.")
        # Registered user
        else:
            file = 'options.csv'
            with open(file, 'r', newline='') as file:
                reader = csv.reader(file)
                data = list(reader)
                account = [name, password, max_card_count, new_card_count, background, music_volume, sfx_volume]
                # Find line where this account options data is stored
                for line in reader:
                    if line[0] == name and line[1] == password:
                        # Replace account options data with new values
                        data[data.index(line)] = account
            file = 'options.csv'
            with open(file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
            print(f"CSV file '{file}' written to successfully.")
