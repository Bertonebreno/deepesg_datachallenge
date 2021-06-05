import numpy as np
import pandas as pd

chart_of_accounts = pd.read_excel(r"input/chart_of_accounts.xlsx")
chart_of_accounts = chart_of_accounts.iloc[:,0]
chart_of_accounts_ar = chart_of_accounts.to_numpy()

number_of_accounts = len(chart_of_accounts.index)
account_values = np.zeros(number_of_accounts)

general_ledger = pd.read_excel(r"input/general_ledger.xlsx")


# print(chart_of_accounts)
print(general_ledger)
# print(account_values)

def updateAccountValues(current_account_values, general_ledger, chart_of_accounts_ar):
    for i in range(number_of_accounts):
        account_number = chart_of_accounts_ar[i]
        if (i + 1) == number_of_accounts:
            print("This is the last account!")
            account_transactions = general_ledger.loc[lambda df: df['account'] == account_number]
            account_transactions = account_transactions.iloc[:,1]
            account_transactions_ar = account_transactions.to_numpy()
            current_account_values[i] += np.sum(account_transactions_ar)
            return current_account_values
        else:
            next_account_number = chart_of_accounts_ar[i]
            if(account_number in next_account_number):
            
            else:

account_values = updateAccountValues(account_values, general_ledger, chart_of_accounts_ar)
print(account_values)