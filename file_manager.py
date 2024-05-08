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
        if name is not "" and password is not "":
            if found_account is False:
                # File path for the CSV file
                file = 'accounts.csv'
                account = [name, password, "0"]
                # Open the file in append mode
                with open(file, 'a', newline='') as file:
                    # Append data to the CSV file
                    writer = csv.writer(file)
                    writer.writerow(account)
                # Print a confirmation message
                return "ACCOUNT ADDED"
            else:
                return "ACCOUNT ALREADY EXISTS"
        else:
            return "EMPTY TEXT"
    def add_account_with_score(self, name, password, score):
        found_account = False
        if name is not "" and password is not "":
            file = 'accounts.csv'
            with open(file, 'r') as file:
                reader = csv.reader(file)
                data = list(reader)
                account = [name, password, str(score)]
                file.seek(0) # Reset pointer position to start of file since data puts it at the end
                # Find line where this account options data is stored
                for line in reader:
                    if line[0] == name and line[1] == password:
                        # Replace account options data with new values
                        data[data.index(line)] = account
                        found_account = True
            file = 'accounts.csv'
            if found_account:
                with open(file, 'w', newline='\n') as file:
                    writer = csv.writer(file)
                    writer.writerows(data)
    def login(self, name, password):
        # Check if account in CSV file
        found_account = File_Manager.find_account(self, name, password)
        if found_account:
            return "LOGGED IN"
        else:
            return "NO ACCOUNT FOUND"
    def change_options(self, name, password, max_card_count, new_card_count, background, music_volume, sfx_volume):
        # Guest user
        if name is "" and password is "":
            file = 'options.csv'
            account = [name, password, max_card_count, new_card_count, background, music_volume, sfx_volume]
            with open(file, 'r', newline='') as file:
                reader = csv.reader(file)
                data = list(reader)
            # Replace default values (always at index 1) with new values
            data[1] = account
            # Rewrite data back to the CSV file
            file = 'options.csv'
            with open(file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
        # Registered user
        else:
            found_account = False
            file = 'options.csv'
            with open(file, 'r') as file:
                reader = csv.reader(file)
                data = list(reader)
                account = [name, password, max_card_count, new_card_count, background, music_volume, sfx_volume]
                file.seek(0) # Reset pointer position to start of file since data puts it at the end
                # Find line where this account options data is stored
                for line in reader:
                    if line[0] == name and line[1] == password:
                        # Replace account options data with new values
                        data[data.index(line)] = account
                        found_account = True
            file = 'options.csv'
            if found_account:
                with open(file, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(data)
            else:
                account = ','.join(account)
                with open(file, 'a', newline='') as file:
                    file.write(account)
    def get_options(self, name, password):
        # Return options list
        if name is "" and password is "":
            file = 'options.csv'
            with open(file, 'r', newline='') as file:
                reader = csv.reader(file)
                data = list(reader)
                return data
        else:
            file = 'options.csv'
            with open(file, 'r', newline='') as file:
                reader = csv.reader(file)
                for line in reader:
                    if line[0] == name and line[1] == password:
                        return line
    def get_account_data(self, name, password):
        file = 'accounts.csv'
        with open(file, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader) # Skip header line
            data = list(reader)
            return data


