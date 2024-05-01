import requests

# URL of the API endpoint
url = 'https://min-api.cryptocompare.com/data/price?fsym=USD&tsyms=EUR'

# Sending a GET request
response = requests.get(url)

# Checking if the request was successful (status code 200)
if response.status_code == 200:
    # Getting the JSON response
    data = response.json()
    # Process the JSON data as needed
    print(data)
else:
    print("Error:", response.status_code)
