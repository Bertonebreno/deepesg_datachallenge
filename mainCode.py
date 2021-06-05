import numpy as np
import pandas as pd

try:
    chart_of_accounts = pd.read_excel(r"input/chart_of_accounts.xlsx")
except:
    print("Could not read the chart of accounts")
chart_of_accounts = chart_of_accounts.iloc[:,0]
chart_of_accounts_ar = chart_of_accounts.to_numpy()

number_of_accounts = len(chart_of_accounts.index)
account_values = np.zeros(number_of_accounts)   #array we will use to store total transactions in an account

parent_nodes = np.zeros(number_of_accounts) - 1 #array we will use to store the parent of a node in the
                                                #account tree. The value -1 means it is a root node

try:
    general_ledger = pd.read_excel(r"input/general_ledger.xlsx")
except:
    print("Could not read the general ledger")


# We will go through all accounts, check if they have any child accounts, if they have we will 
#store this information, if not, we will save its account value
for i in range(number_of_accounts): 

    account_number = chart_of_accounts_ar[i]

    account_transactions = general_ledger.loc[lambda f: general_ledger['account'] == account_number]  # In this part we get the sum of all transactions an account has made.
    account_transactions = account_transactions.iloc[:,1]                                             #This can be changed to a relational database, as the only information
    account_transactions_ar = account_transactions.to_numpy()                                         #needed from the general ledger is the list of the sum of the transactions
    account_values[i] += np.sum(account_transactions_ar)                                              #the accounts were involved, a simple task that will result in a list with
                                                                                                      #the same size as the chart of accounts.

    if (parent_nodes[i] == -1 and i > 0): # Let's find for its parent (if it has one)
        current_possible_parent = i - 1   # This will check if the previous account is the parent
        while True:
            if(chart_of_accounts_ar[int(current_possible_parent)] in account_number):  #Found a parent!
                parent_nodes[i] = current_possible_parent
                break
            elif(parent_nodes[int(current_possible_parent)] != -1):  # Keep looking for its parent
                current_possible_parent = parent_nodes[int(current_possible_parent)] # This will check if the parent of the previous
                                                                                     #account is the parent of the current account
            else:   # It is a root (or parentless) node 
                break



# Now we will go through the account list in reverse order, summing the account_values
#to its respective parents
for i in range(number_of_accounts-1, -1, -1):

    if (parent_nodes[i] != -1):
        parent_index = int(parent_nodes[i])
        account_values[parent_index] += account_values[i]

data = pd.DataFrame({"account": chart_of_accounts_ar, "total_transactions": account_values})
data.to_excel('output/output.xlsx', index=False, sheet_name='new_sheet_name')
print(account_values)