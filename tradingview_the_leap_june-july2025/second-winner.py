"""
@author: seyedeh fatemeh hosseininasab
second winner
"""
import matplotlib.pyplot as plt
fig,axs=plt.subplots(2,2,figsize=(15, 10))

#Percentage of profitable trades
sizes=[86,14]
labels=['win','loss']
colors=['g','r']
axs[0,0].pie(sizes,labels=labels,colors=colors,autopct="%1.1f%%",shadow=True)
axs[0,0].set_title("Percentage of Winning Trades")

#Number of trades per symbol
size_number=[11,8,1,6,2,5,5,2,4,11,1]
labels_symbols=['mini nasdaq', 'mini s&p', "micro s&p", "full size gold", "micro dow",
                 "micro crude", "full size crude", "mini dow", "micro ether", "micro bitcoin", "micro euro fx"]
axs[0,1].pie(size_number,labels=labels_symbols,autopct="%1.1f%%",shadow=True)
axs[0,1].set_title("Number of Trades per Symbol")

#Percentage of profitable trades per symbol
size_number1= [91,100,100,83,100,80,60,100,75,100,0]
axs[1,0].pie(size_number1, labels=labels_symbols, autopct="%1.1f%%", shadow=True)
axs[1,0].set_title("Percentage of Profitable Trades per Symbol")

# 4. Percentage of buy and sell trades
size_per=[53,47]
labels_trade = ['buy', 'sell']
colors = ['g', 'r']
axs[1, 1].pie(size_per, labels=labels_trade, colors=colors, autopct="%1.1f%%", shadow=True)
axs[1, 1].set_title("Percentage of Buy vs Sell Trades")

plt.suptitle("Trade analysis overview for the second winner", fontsize=16)
plt.tight_layout()
plt.show()