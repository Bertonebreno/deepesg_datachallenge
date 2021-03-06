import sys
import numpy as np
import pandas as pd

def getTotalTransaction(general_ledger):
    # In this part we get the sum of all transactions an account has made
    general_ledger = general_ledger.set_index("account")
    account_transactions = general_ledger.groupby(level=0, axis=0).sum()
    return account_transactions

def getAccountValues(chart_of_accounts, account_transactions):
    chart_of_accounts = chart_of_accounts.iloc[:,0] 
    number_of_accounts = len(chart_of_accounts.index)

    chart_of_accounts_ar = chart_of_accounts.to_numpy().reshape(number_of_accounts)

    account_values = np.zeros(number_of_accounts)   #array we will use to store total value in an account

    parent_nodes = np.zeros(number_of_accounts) - 1 #array we will use to store the parent of a node in the
                                                    #account tree. The value -1 means it is a root node


    # We will go through all accounts, save its account value, and then check if they have any a parent account, 
    #if they have we will store this information
    for i in range(number_of_accounts): 
        account_number = chart_of_accounts_ar[i]

        try:
            account_values[i] += account_transactions.loc[account_number][0]                                           
        except:
            pass                                                                           

        if (parent_nodes[i] == -1 and i > 0): # Let's find its parent (if it has one)
            current_possible_parent = i - 1   # This will check if the previous account is the parent
            while True:
                if(chart_of_accounts_ar[int(current_possible_parent)] in account_number):  #Found a parent!
                    parent_nodes[i] = current_possible_parent
                    break
                elif(parent_nodes[int(current_possible_parent)] != -1):  # Keep looking for its parent
                    current_possible_parent = parent_nodes[int(current_possible_parent)] # This will check if the parent of the previous account is the parent of the current account
                                        
                else:   # It is a root (or parentless) node 
                    break



    # Now we will go through the account list in reverse order, summing the account_values
    #to its respective parents
    for i in range(number_of_accounts-1, -1, -1):

        if (parent_nodes[i] != -1):
            account_values[int(parent_nodes[i])] += account_values[i]

    chart_and_values = pd.DataFrame({"account": chart_of_accounts_ar, "total_transactions": account_values})
    return account_values, chart_and_values


if __name__ == '__main__':
    try:
        chart_of_accounts_path = sys.argv[1]
        chart_of_accounts = pd.read_excel(chart_of_accounts_path)
    except:
        print("Could not read the chart of accounts")
        sys.exit()

    try:
        general_ledger_path = sys.argv[2]
        general_ledger = pd.read_excel(general_ledger_path)
    except:
        print("Could not read the general ledger")
        sys.exit()

    try:
        output_path = sys.argv[3]
    except:
        print("Could not get to the output path")
        sys.exit()

    account_transactions = getTotalTransaction(general_ledger)
    account_values, chart_and_values = getAccountValues(chart_of_accounts, account_transactions)

    print(account_values)
    try:
        chart_and_values.to_excel(output_path)
    except:
        print(chart_and_values)
        print("Could not write the solution to the output path")