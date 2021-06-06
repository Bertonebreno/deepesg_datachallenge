import sys
import numpy as np
import pandas as pd
import time
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

        elif (action == 1):
            levels[-1] += 1
            if(len(levels) > 1):
                child_list[current_parent[-1]].append(i)
            else:
                is_root[i] = 1
        
        else:
            current_parent.append(i - 1)
            child_list[current_parent[-1]].append(i)
            levels.append(1)

        for j in range(len(levels)):
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
        
        temp = account_values[i]
        for j in range(len(child_list[i])):
            account_values[child_list[i][j]] = np.random.random()*temp
            temp -= account_values[child_list[i][j]]

        general_ledge[i] = temp

    general_ledge = pd.DataFrame({"account":chart_of_accounts, "value": general_ledge})

    return general_ledge, account_values




def testFunction(max_number_of_accounts):
    start_time = time.time()

    number_of_accounts = np.random.randint(1, max_number_of_accounts)
    random_chart, is_root, child = createChartOfAccounts(number_of_accounts)
    random_ledge, value = createGeneralLedge(random_chart, is_root, child)

    creation_time  = time.time() - start_time

    start_time = time.time()

    account_transactions = mainCode.getTotalTransaction(random_ledge)
    random_chart = pd.DataFrame(random_chart)
    new_value, chart = mainCode.getAccountValues(random_chart, account_transactions)

    calculation_time = time.time() - start_time

    answer = np.allclose(value, new_value)  # using np.allclose to avoid differences caused by floating point calculations

    return answer, creation_time, calculation_time




if __name__ == "__main__":
    try:
        number_of_times = int(sys.argv[1])
        max_number_of_accounts = int(sys.argv[2])
    except:
        print("Not enough arguments")

    solutions = []
    creation_time = 0
    calculation_time = 0
    for i in range(number_of_times):
        print(i)
        this_solution, this_creation_time, this_calculation_time = testFunction(max_number_of_accounts)
        solutions.append(this_solution)
        creation_time += this_creation_time
        calculation_time += this_calculation_time

    print(np.all(solutions), creation_time/number_of_times, calculation_time/number_of_times)