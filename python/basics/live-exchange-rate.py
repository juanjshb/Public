import requests
import json
import random

currencyFrom = input("Enter the currency you own: ").upper()
currencyTo = input("Enter the currency you want: ").upper()

# URL of the API endpoint
url = 'https://min-api.cryptocompare.com/data/price?fsym={0}&tsyms={1}'.format(currencyFrom, currencyTo)

# Sending a GET request
response = requests.get(url)

# Checking if the request was successful (status code 200)
if response.status_code == 200:
    # Getting the JSON response
    data = response.json()
    # Process the JSON data as needed
    print("The current exchange rate for 1 {0} is {1} {2}".format(currencyFrom, data[currencyTo], currencyTo))
    condition = input("Would you like to make a reservation? [Y/N]")
    if condition.upper() == "Y":
           ammountFrom = input("Enter the amount of money you have: ")
           ammountTo = float(ammountFrom) * float(data[currencyTo])
           print("The current exchange rate for {0} {1} is {2} {3}".format(ammountFrom, currencyFrom, ammountTo, currencyTo))
           validation = input("Are you sure you want to make a reservation? [Y/N]")
           if validation.upper() == "Y":
                print("Your reservation number is: {0}".format(random.randint(0, 1000000)))
           elif validation.upper() == "N":
                print("Have a nice day!")
           else:
                print("This option is not available")
    elif condition.upper() == "N":
        # code block to execute if another_condition is True
         print("Have a nice day!")
    else:
         print("This option is not available")
    
else:
     print("Error:", response.status_code)
