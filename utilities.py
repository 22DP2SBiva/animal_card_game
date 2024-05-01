# Various useful functions
class Utilities:
    def sort_by_highest(self, accounts):
        # Sort players by highest score
        sorted_accounts = []
        for user in accounts:
            if not sorted_accounts: # If list empty, add first score
                sorted_accounts.append([user[2], user[0]]) # Append score and name of user
            else:
                inserted = False
                for i, sorted_user in enumerate(sorted_accounts):
                    if int(user[2]) > int(sorted_user[0]):
                        print("user ", user[2], "is larger than ", sorted_user[0])
                        sorted_accounts.insert(i, [user[2], user[0]])
                        print("inserting into ", i)
                        inserted = True
                        break
                if not inserted:
                    sorted_accounts.append([user[2], user[0]])
        return sorted_accounts
    def sort_by_lowest(self, accounts):
        # Sort players by lowert score
        sorted_accounts = []
        for user in accounts:
            if not sorted_accounts: # If list empty, add first score
                sorted_accounts.append([user[2], user[0]]) # Append score and name of user
            else:
                inserted = False
                for i, sorted_user in enumerate(sorted_accounts):
                    if int(user[2]) < int(sorted_user[0]):
                        sorted_accounts.insert(i, [user[2], user[0]])
                        inserted = True
                        break
                if not inserted:
                    sorted_accounts.append([user[2], user[0]])
        return sorted_accounts