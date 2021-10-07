import csv
import os

def is_int(str):
    '''
    Returns whether the string input is an integer.
    '''
    try:
        a = float(str)
        b = int(str)
    except (TypeError, ValueError):
        return False
    else:
        return a == b

#Checking integrity of transactions.
def check_transactions(customers, transactions):
    #Integrity checking for transactions
    print("Checking transactions...")
    index = 0
    for t in transactions:
        print(str(round(100 * (index / len(transactions))))+"% remaining")
        is_in = False
        for cust in customers:
            if t[1] == cust[0]:
                is_in = True
                break
        if not is_in:
            print("Error: Mismatched Transaction, removing transaction history")
            transactions.remove(t)
        index += 1
    print("Done!")

def run(customers, transactions, f1, f2, f3):
    # First creates the log.
    f = open(os.path.join('.', 'log.txt'), 'w')
    f.write('Creating log file. \n')
    #f.close()

    #Program logic.
    checksum = 1
    print("Parsing through transactions...")
    for t in transactions:
        cid = t[1]
        
        #Check for matching customer ID.
        for c in customers:
            if c[0] == cid:
                target = c
                
        if t[2] == 'Inquiry':
            message = f1(target[0], target[1], target[2], target[3])
            print(message)
            f.write(message + "\n")
            checksum += 6 + int(target[0])
            
            
        if t[2] == 'Purchase':
            print("Purchase for Customer " + str(cid) + " for amount of $" + str(float(t[3])))
            flag, bal = f2(float(target[3]), float(target[4]), float(t[3]))
            if flag:
                #new_bal = new_purchase(float(target[3]), float(target[4]), float(t[3]))
                print(str(target[1]) + " " + str(target[2]) + 
                     " your account " + str(target[0]) + " had a previous balance of $" + str(target[3]) + 
                     " and after your successful purchase of $" + str(t[3]) + " you have a balance of $" + str(bal))
                f.write(str(target[1]) + " " + str(target[2]) + 
                     " your account " + str(target[0]) + " had a previous balance of $" + str(target[3]) + 
                     " and after your successful purchase of $" + str(t[3]) + " you have a balance of $" + str(bal) + "\n")
                target[3] = bal
                checksum += 7 + int(bal) + int(target[0])
            else:
                print(str(target[1]) + " " + str(target[2]) + 
                     " your account " + str(target[0]) + " had a previous balance of $" + str(target[3]) + 
                     " a credit limit of $" + str(target[4]) + " and your attempted purchase of $" + str(t[3]) + 
                                                 " was declined.")
                f.write(str(target[1]) + " " + str(target[2]) + 
                     " your account " + str(target[0]) + " had a previous balance of $" + str(target[3]) + 
                     " a credit limit of $" + str(target[4]) + " and your attempted purchase of $" + str(t[3]) + 
                                                 " was declined. \n")
                checksum += 8 + int(t[3]) + int(target[0])
            
        if t[2] == 'Refund':
            new_bal = f3(float(target[3]), float(t[3]))
            print(str(target[1]) + " " + str(target[2]) + 
                 " your account " + str(target[0]) + " had a previous balance of $" + str(target[3]) +
                 " and after your refund of $" + str(t[3]) + " you now have a balance of $" + str(new_bal))
            f.write(str(target[1]) + " " + str(target[2]) + 
                 " your account " + str(target[0]) + " had a previous balance of $" + str(target[3]) +
                 " and after your refund of $" + str(t[3]) + " you now have a balance of $" + str(new_bal) + "\n")
            target[3] = new_bal
            checksum += 9 + int(new_bal) + int(target[0])
    
    checksum = checksum % 10000
    print("Your hash is " + str(checksum))
    f.write("Your hash is " + str(checksum))
    f.close()