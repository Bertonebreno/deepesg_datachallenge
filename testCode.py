import sys
import numpy as np
import pandas as pd
import mainCode

# In this testCode we will generate 

def createChartOfAccounts(number_of_accounts):
    chart_of_accounts = []
    child_list = []
    for i in range(number_of_accounts):
        chart_of_accounts.append("")
        child_list.append([])
    is_root = np.zeros(number_of_accounts, dtype=bool)

    chart_of_accounts[0] = "1"
    is_root[0] = 1
    current_parent = [0]
    levels = [1]    # The level indicates how many children a node has    


    for i in range(1, number_of_accounts):
        action = np.random.randint(0, 3) # 0 -> goes back a level // 1 -> keeps the level // 2 -> increases the level
        
        if (action == 0):
            if (len(current_parent) == 1):     # The current parent is a root, the next parent is also a root
                is_root[i] = 1
                current_parent[-1] = i
            elif (len(current_parent) == 2):   # The current parent is not a root, but the next one is
                is_root[i] = 1
                current_parent.pop()
            else:                              # Neither the current nor the next parent are root nodes
                current_parent.pop()
                child_list[current_parent[-1]].append(i)

            if (len(levels) > 1):
                levels.pop()
            levels[-1] += 1

        elif (action == 1):     # Keeps the level
            levels[-1] += 1
            if(len(levels) > 1):     
                child_list[current_parent[-1]].append(i)    # It isn't a root node
            else:
                is_root[i] = 1      # It is a root node
        
        else:     # Increases the level
            current_parent.append(i - 1)
            child_list[current_parent[-1]].append(i)
            levels.append(1)

        for j in range(len(levels)):    # Builds the string that is the account_number
            if (j == 0):
                chart_of_accounts[i] = str(levels[j])    
            else:
                chart_of_accounts[i] = chart_of_accounts[i] +"."+str(levels[j])
    
    return chart_of_accounts, is_root, child_list


def createGeneralLedge(chart_of_accounts, is_root, child_list):
    account_values = np.zeros(len(chart_of_accounts))
    general_ledge = np.zeros(len(chart_of_accounts))
    for i in range(len(chart_of_accounts)):
        if (is_root[i]):  # If it is a root node, we will add some value into it
            account_values[i] = np.random.rand()*1e10 # Random number between 0 and 10^10
        
        temporary_value = account_values[i]
        for j in range(len(child_list[i])):
            account_values[child_list[i][j]] = np.random.random()*temporary_value
            temporary_value -= account_values[child_list[i][j]]

        general_ledge[i] = temporary_value

    general_ledge = pd.DataFrame({"account":chart_of_accounts, "value": general_ledge})

    return general_ledge, account_values




def testFunction(max_number_of_accounts):

    number_of_accounts = np.random.randint(1, max_number_of_accounts)
    random_chart, is_root, child = createChartOfAccounts(number_of_accounts)
    random_ledge, value = createGeneralLedge(random_chart, is_root, child)

    account_transactions = mainCode.getTotalTransaction(random_ledge)
    random_chart = pd.DataFrame(random_chart)
    new_value, chart = mainCode.getAccountValues(random_chart, account_transactions)

    answer = np.allclose(value, new_value)  # using np.allclose to avoid differences caused by floating point calculations

    return answer



if __name__ == "__main__":
    try:
        number_of_times = int(sys.argv[1])
        max_number_of_accounts = int(sys.argv[2])
    except:
        print("This code needs two integers as inputs: times to test and maximum number of accounts")
        sys.exit()

    solutions = []
    for i in range(number_of_times):
        print(i)
        this_solution = testFunction(max_number_of_accounts)
        solutions.append(this_solution)

    print(solutions)
    if np.all(solutions):
        print("All tests have succeded!")
