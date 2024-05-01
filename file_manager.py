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
                account = ','.join(account)
                # Open the file in append mode
                with open(file, 'a') as file:
                    # Append data to the CSV file
                    file.write("\n"+account)
                # Print a confirmation message
                print(f"CSV file '{file}' appended to successfully.")
                return "ACCOUNT ADDED"
            else:
                print("Account already exists.")
                return "ACCOUNT ALREADY EXISTS"
        else:
            return "EMPTY TEXT"
    def login(self, name, password):
        # Check if account in CSV file
        found_account = File_Manager.find_account(self, name, password)
        if found_account:
            print("Successfully logged in.")
            return "LOGGED IN"
        else:
            return "NO ACCOUNT FOUND"
    def change_options(self, name, password, max_card_count, new_card_count, background, music_volume, sfx_volume):
        # Guest user
        if name is "" and password is "":
            print("Guest")
            file = 'options.csv'
            account = [name, password, max_card_count, new_card_count, background, music_volume, sfx_volume]
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
            print("Registered user")
            found_account = False
            file = 'options.csv'
            with open(file, 'r') as file:
                reader = csv.reader(file)
                data = list(reader)
                account = [name, password, max_card_count, new_card_count, background, music_volume, sfx_volume]
                file.seek(0) # Reset pointer position to start of file since data puts it at the end
                # Find line where this account options data is stored
                print("In read")
                for line in reader:
                    print(line)
                    if line[0] == name and line[1] == password:
                        # Replace account options data with new values
                        print("data at index", data[data.index(line)])
                        print("account", account)
                        data[data.index(line)] = account
                        found_account = True
            file = 'options.csv'
            if found_account:
                print("found account")
                with open(file, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(data)
            else:
                print("no account in options file")
                account = ','.join(account)
                with open(file, 'a', newline='') as file:
                    file.write(account)
            print(f"CSV file '{file}' written to successfully.")
    def get_options(self, name, password):
        # Return options list
        if name is "" and password is "":
            file = 'options.csv'
            with open(file, 'r', newline='') as file:
                reader = csv.reader(file)
                data = list(reader)
                return data
        else:
            print("Registeresd read")
            file = 'options.csv'
            with open(file, 'r', newline='') as file:
                reader = csv.reader(file)
                for line in reader:
                    print("line", line)
                    if line[0] == name and line[1] == password:
                        print(line)
                        return line
    def get_account_data(self, name, password):
        file = 'accounts.csv'
        with open(file, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader) # Skip header line
            data = list(reader)
            return data


