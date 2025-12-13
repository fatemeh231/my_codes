"""
@author: seyedeh fatemeh hosseininasab
fifth winner
"""
import matplotlib.pyplot as plt

fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# 1. Percentage of profitable trades
sizes = [34,66]
labels = ['win', 'loss']
colors = ['g', 'r']
axs[0, 0].pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", shadow=True)
axs[0, 0].set_title("Percentage of Winning Trades")

# 2. Number of trades per symbol
size_number= [28,30,29,19,24,33,29,28,21,29,17,20,20]
labels_symbols = ['mini nasdaq', 'mini s&p', "micro s&p", "full size gold", "micro dow", "micro nasdaq",
                  "micro crude", "full size crude", "mini dow", "micro gold", "micro ether", "micro bitcoin", "micro euro fx"]
axs[0, 1].pie(size_number, labels=labels_symbols, autopct="%1.1f%%", shadow=True)
axs[0, 1].set_title("Number of Trades per Symbol")

# 3. Percentage of profitable trades per symbol
size_number1= [36,33,38,21,38,36,38,32,33,28,41,45,25]
axs[1, 0].pie(size_number1, labels=labels_symbols, autopct="%1.1f%%", shadow=True)
axs[1, 0].set_title("Percentage of Profitable Trades per Symbol")

# 4. Percentage of buy and sell trades
size_per = [53,47]
labels_trade = ['buy', 'sell']
colors = ['g', 'r']
axs[1, 1].pie(size_per, labels=labels_trade, colors=colors, autopct="%1.1f%%", shadow=True)
axs[1, 1].set_title("Percentage of Buy vs Sell Trades")

plt.suptitle("Trade analysis overview for the fifth winner", fontsize=16)
plt.tight_layout()
plt.show()