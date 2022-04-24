import datetime
from db import SalesDb

# Global
db = SalesDb('Sales.db')
saleItem = {
    "id": 0,
    "SaleDate": '',
    "SellerId": 0,
    "CustomerName": '',
    "SaleItemName": '',
    "SaleValue": 0.0                                
}

print('Welcome to Nando\'s Sales Manager!\n')

#Validations
def ValidateDate(date_text):
    try:
        date_text = datetime.datetime.strptime(date_text, "%m/%d/%Y").strftime("%Y-%m-%d")
        return date_text
    except ValueError:
        return False
    
def DateFormatDB(dbDate):
    try:
        dbDate = datetime.datetime.strptime(dbDate, "%Y-%m-%d").strftime("%m/%d/%Y")
        return dbDate
    except ValueError:
        return dbDate
    
def ValidadePrice(price_text):
    if ((len(price_text.rsplit('.')[-1]) == 2) or (price_text.replace('.','',2).isdigit())):
        return True
    else:
        return False

def InputValidation(inp):
    match inp.lower():
        case '1':
            return True
        case '2':
            return True
        case '3':
            return True
        case '4':
            return True
        case 'q':
            return True
        case _:
            return False

# Main methods
def InsertEditSale(sale, editSale: bool):
    sellers = db.GetSellers()
    userInput = ''
    
    sellerId = -1    
    newSale = list(sale)

    while True:
        # Set SaleDate
        while True:
            userInput = input('\n- Type the date of the sale in the format mm/dd/yyyy, or (Q) to return\n')
            if(ValidateDate(userInput) == False):
                print('\n- Invalid date')
                continue
            else:
                newSale[1] = userInput
                break
        if(userInput.lower() == 'q'):
            break

        # Select Seller
        while True:
            print()
            for val in sellers:
                print(f'({val[0]}) {val[1]}')

            userInput = input('\n- Type the number of the seller, or (Q) to return\n')
            if(userInput.isnumeric() and int(userInput) <= len(sellers) and int(userInput) > 0):
                sellerId = int(userInput)
                print(f'\n({sellers[sellerId-1][0]}) {sellers[sellerId-1][1]}\n')
                userInput = input('Confirm seller?\n    (Y) Yes    (N) No\n')
                if(userInput.lower() == 'n'):
                    print('No')
                    continue
                elif(userInput.lower() == 'y'):
                    newSale[2] = sellers[sellerId-1][1]
                    print('Yes')
                    break
                else:
                    print('\n- Invalid option')
            elif(userInput.lower() == 'q'):
                break
            else:
                print('\n- Invalid option')
                continue
        if(userInput.lower() == 'q'):
            break

        # Set CustomerName
        while True:
            userInput = input('\n- Type the name of the customer, or (Q) to return\n')
            if(userInput.lower() == 'q'):
                break
            elif(not userInput == '' and not userInput.isspace() and (all(x.isalpha() or x.isspace() for x in userInput))):
                newSale[3] = userInput
                break
            else:
                print('\n- Invalid name')
        if(userInput.lower() == 'q'):
            break

        # Set SaleItemName
        while True:
            userInput = input('\n- Type the item sold, or (Q) to return\n')
            if(userInput.lower() == 'q'):
                break
            elif(not userInput == '' and not userInput.isspace() and (all(x.isalpha() or x.isspace() for x in userInput))):
                newSale[4] = userInput.lower()
                break
            else:
                print('\n- Invalid name')
        if(userInput.lower() == 'q'):
            break

        # Set SaleValue
        while True:
            userInput = input('\n- Type the price of the item with two decimals in the format: $00.00, or (Q) to return\n$')
            if(userInput.lower() == 'q'):
                break
            elif(ValidadePrice(userInput)):
                newSale[5] = float(userInput)
                break
            else:
                print('\n- Invalid price')
                continue
        if(userInput.lower() == 'q'):
            break
        
        while True:
            # Confirm informations
            print(f'\n{newSale[1]} - Seller: {newSale[2]}, Customer: {newSale[3]}, Item: {newSale[4]} - ${newSale[5]}\n')
            userInput = input('Confirm data?\n    (Y) Yes, finish    (N) No, rewrite data\n')
            if(userInput.lower() == 'y'):
                if(editSale == False):
                    db.InsertSale(ValidateDate(newSale[1]), sellerId, newSale[3], newSale[4], newSale[5])
                    print('\n- Sale inserted!\n')
                    userInput = 'q'
                    break
                elif(editSale == True):
                    db.UpdateSale(newSale[0], ValidateDate(newSale[1]), sellerId, newSale[3], newSale[4], newSale[5])
                    print('\n- Sale updated!\n')
                    userInput = 'q'
                    break
            elif(userInput.lower() == 'n'):
                continue
            else:
                print('\n- Type a valid option')
        if(userInput.lower() == 'q'):
            break    
    
def SelectSale(sales):
    while True:
        saleIndex = 1
        for val in sales:
            print(f'({saleIndex}) {DateFormatDB(val[1])} - Seller: {val[2]}, Customer: {val[3]}, Item: {val[4]} - ${val[5]}')
            saleIndex += 1
    
        userInput = input('\n- Type the sale number, or (Q) to return\n')
        if(userInput.isnumeric()):
            if(int(userInput) <= len(sales)):
                return userInput
        elif(userInput.lower() == 'q'):
            return 'q'
        print('\n- Type a valid option')

def RemoveSale(sale):
    while True:
        print(f'{DateFormatDB(sale[1])} - Seller: {sale[2]}, Customer: {sale[3]}, Item: {sale[4]} - ${sale[5]}')
        userInput = input('\nRemove this sale?\n    (Y) Yes    (N) No\n')
        if(userInput.lower() == 'y'):
            print('\nYes\n')
            db.RemoveSale(sale[0])
            print('\nSale removed!\n')
            break
        elif(userInput.lower() == 'n'):
            print('\nNo\n')
            break
        else:
            print('\n- Invalid option\n')

# Sale List
def ShowAllSales():
    sales = db.GetAllSales()
    rank = 1
    for val in sales:
        print(f'({rank}) {DateFormatDB(val[1])} - Seller: {val[2]}, Customer: {val[3]}, Item: {val[4]} - ${val[5]}')
        rank += 1
    print()
    while True:
        userInput = input('    (1) Insert sale (2) Edit sale (3) Remove sale (4) Show seller ranking (Q) Return to main options\n\n')
        if InputValidation(userInput):
            break
        print('- Select a valid option')
        continue

    match userInput.lower():
        case '1':
            print('\n- Insert sale:\n')
            InsertEditSale(saleItem.keys(), False)
        case '2':
            print('\n- Edit sale:\n')
            userInput = SelectSale(sales)
            if (userInput.lower() == 'q'):
                return
            InsertEditSale(sales[int(userInput)-1], True)            
        case '3':
            print('\n- Remove sale:\n')
            userInput = SelectSale(sales)
            if (userInput.lower() == 'q'):
                return
            RemoveSale(sales[int(userInput)-1]) 
        case '4':
            print('\n- Sellers ranking:\n')
            ShowSellerRanking()
        case 'q':
            print('\nReturn\n')
            return
        case _:
            print('\n- Invalid option\n')
            return
        
def ShowSellerRanking():
    rank = 1
    for val in db.GetMainSales():
        print(f'({rank}) {val[0]}, Total sold: ${val[1]}')
        rank += 1
    print()

def SelectOption():
    userInput = ''
    print('\n- Select an option:')
    while True:
        userInput = input('    (1) Show seller ranking (2) Insert sale (3) Show Sales history (4) Show Credits (Q) Quit application\n')
        if InputValidation(userInput):
            break
        print('\n- Select a valid option')
        continue
    
    match userInput.lower():
        case '1':
            print('\n- Sellers ranking:\n')
            ShowSellerRanking()
        case '2':
            print('\n- Insert sale:\n')
            InsertEditSale(saleItem.values(), False)
        case '3':
            print('\n- Sales history:\n')
            ShowAllSales()
        case '4':
            print('\n- Created by Fernando Lopes as a business case, on April/2022\n\nPress Enter to continue\n')
            input()
        case 'q':
            print('\nQuit!\n')
            return userInput.lower()
         
# Main loop  
while True:
    userInput = SelectOption()
    if userInput == 'q':
        print('Thank you for using Nando\'s Sales Manager!')
        input()
        break