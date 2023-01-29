import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf


def total_return(prices, reference):
    shares = 0
    for i in range(len(prices)):
        shares += reference[i] / prices[i]
    return shares * prices[len(prices) - 1]


def dlr(val):
    return round(val * 100) / 100


def validate_int_input(firstString, errorString="Error, please enter an integer: "):
    validatedInput = 0
    tryLoop = True

    try:
        validatedInput = int(input(firstString))
    except ValueError:
        while tryLoop:
            tryLoop = False
            try:
                validatedInput = int(input(errorString))
            except ValueError:
                tryLoop = True
    return validatedInput


def validate_str_input(firstString, errorString="Error, please enter a string: "):
    validatedInput = ""
    tryLoop = True

    try:
        validatedInput = str(input(firstString))
    except ValueError:
        while tryLoop:
            tryLoop = False
            try:
                validatedInput = str(input(errorString))
            except ValueError:
                tryLoop = True
    return validatedInput


print("Welcome, this program simulates returns for DCA'ing into stocks\n")

# Defining ticker and historical range
backup_ticker = "vti"

try:
    userInput = input("Enter what ticker you would like to simulate returns for: ")
    stock = yf.Ticker(userInput)
except IndexError:
    userInput = input("Error, please enter a correctly formatted ticker (Ex: vti): ")
    stock = yf.Ticker(userInput)


userStartYear = validate_str_input("Enter the year you would like the backtest to begin: ")

start_date = userStartYear + "-2-13"
end_date = "2023-1-28"

# Initializing stock info
hist = stock.history(start=start_date, end=end_date)
print(f"Downloading information for {userInput}")
data = yf.download(userInput, start_date, end_date)
print("")

# This code throws an error if yfinance can't find the entered ticker
try:
    tester = hist["Open"][0]
except IndexError:
    print("\nCould not find specified ticker. Switching to default ticker 'VTI' ")
    stock = yf.Ticker("VTI")
    hist = stock.history(start=start_date, end=end_date)

# Variables
price_list = []
monthly_addition = validate_int_input("Enter how much you would invest each month: ")
current_shares = 0
portfolio_values = []

# Creating a clean price list
for i in range(len(hist["Open"])):
    price_list.append(dlr(hist["Open"][i]))


# Creating the portfolio values list
for i in range(len(price_list)):
    if i % 30 == 0:
        current_shares += monthly_addition/price_list[i]
    portfolio_values.append(current_shares * price_list[i])

# Calculating end value of investments
end_value = portfolio_values[ len(portfolio_values) - 1]

# Printing out results
print("Ending Portfolio Value: $" + str(dlr(end_value)))

# Adding the portfolio values data to the dataframe
data['Portfolio_Value'] = portfolio_values

df = pd.DataFrame(data)

df.plot(y="Portfolio_Value", kind="line")

plt.show()
