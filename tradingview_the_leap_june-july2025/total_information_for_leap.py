import matplotlib.pyplot as plt

# Create the figure with 2x2 subplots
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# 1. Percentage of profitable trades
profit= [43, 57]
labels = ['profitable', 'unprofitable']
colors = ['g', 'r']
axs[0, 0].pie(profit, labels=labels, colors=colors, autopct="%1.1f%%", shadow=True)
axs[0, 0].set_title("Percentage of Winning Trades")

# 2. Number of trades per symbol
size_number= [782281, 320873, 112412, 272042, 53693, 118061, 88611, 117746, 107119, 99697, 109829, 143445, 50861]
labels_symbols = ['mini nasdaq', 'mini s&p', "micro s&p", "full size gold", "micro dow", "micro nasdaq",
                  "micro crude", "full size crude", "mini dow", "micro gold", "micro ether", "micro bitcoin", "micro euro fx"]
axs[0, 1].pie(size_number, labels=labels_symbols, autopct="%1.1f%%", shadow=True)
axs[0, 1].set_title("Number of Trades per Symbol")

# 3. Invested funds for trades per symbol
size_number1= [353.1,100.4,5.5,95.1,2.3,5.4,3.6,8.4,23.9,5.6,2.9,5.6,2.7]
axs[1, 0].pie(size_number1, labels=labels_symbols, autopct="%1.1f%%", shadow=True)
axs[1, 0].set_title("Invested Funds for Trades per Symbol")

# 4. Replace with styled message
axs[1, 1].axis('off')  # hide the axes

# Draw a rectangle as background
rect = plt.Rectangle((0, 0), 1, 1, color='lightyellow', alpha=0.8)
axs[1, 1].add_patch(rect)

# Add the message text
message = ("number of traders:54,870.\n"
           "total number of trades:2,376,670\n")
axs[1, 1].text(0.5, 0.5, message, ha='center', va='center', fontsize=25, wrap=True)

# Add overall title
plt.suptitle("Trade analysis overview of whole traders", fontsize=20)

# Layout adjustment
plt.tight_layout()
plt.show()