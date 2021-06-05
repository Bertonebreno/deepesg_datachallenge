import numpy as np
import pandas as pd

chart_of_accounts = pd.read_excel(r"input/chart_of_accounts.xlsx")
chart_of_accounts = chart_of_accounts.iloc[:,0]
chart_of_accounts_ar = chart_of_accounts.to_numpy()

number_of_accounts = len(chart_of_accounts.index)
account_values = np.zeros(number_of_accounts)
parent_nodes = np.zeros(number_of_accounts) - 1 #list we will use to store the parent of a node in the
                                                #account tree. The value -1 means it is a root node


general_ledger = pd.read_excel(r"input/general_ledger.xlsx")



#We will go through all accounts, check if they have any child accounts, if they have we will 
#store this information, if not, we will save its account value
for i in range(number_of_accounts): 
    account_number = chart_of_accounts_ar[i]

    if (parent_nodes[i] == -1 and i > 0): #let's find for its parent (if it has one)
        current_possible_parent = i - 1
        while True:
            if(chart_of_accounts_ar[int(current_possible_parent)] in account_number):  #Found a parent!
                parent_nodes[i] = current_possible_parent
                break
            elif(parent_nodes[int(current_possible_parent)] != -1):  #Keep looking for its parent
                current_possible_parent = parent_nodes[int(current_possible_parent)]
            else:   #It is a root node
                break

    if (i + 1) == number_of_accounts: #last account in the chart of accounts
        account_transactions = general_ledger.loc[lambda df: df['account'] == account_number]
        account_transactions = account_transactions.iloc[:,1]
        account_transactions_ar = account_transactions.to_numpy()
        account_values[i] += np.sum(account_transactions_ar)
    
    else:
        next_account_number = chart_of_accounts_ar[i + 1]

        if(account_number in next_account_number): #get child node
            parent_nodes[i+1] = i

        else: #end node

            account_transactions = general_ledger.loc[lambda df: df['account'] == account_number]
            account_transactions = account_transactions.iloc[:,1]
            account_transactions_ar = account_transactions.to_numpy()
            account_values[i] += np.sum(account_transactions_ar)


#Now we will go through the account list in reverse order, summing the childless account_values
#to its respective parents
for i in range(number_of_accounts-1, -1, -1):

    if (parent_nodes[i] != -1):
        parent_index = int(parent_nodes[i])
        account_values[parent_index] += account_values[i]



print(account_values)