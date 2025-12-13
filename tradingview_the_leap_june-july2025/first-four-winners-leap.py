"""
@author: seyedeh fatemeh hosseininasab
first four winners in depth information
"""
import matplotlib.pyplot as plt
import numpy as np

# Your data lists
size_number1= [14, 13, 10, 8, 8, 8, 8, 8, 7, 7, 7, 5, 3]
size_number1_prime= [100, 100, 90, 88, 88, 100, 100, 100, 100, 71, 86, 40, 33]
size_number2= [11,8,1,6,2,0,5,5,2,0,4,11,1]
size_number2_prime= [91,100,100,83,100,0,80,60,100,0,75,100,0]
size_number3= [5, 5, 5, 2, 5, 6, 6, 4, 6, 5, 6, 5, 5]
size_number3_prime= [100, 100, 100, 50, 100, 83, 67, 50, 67, 100, 83, 80, 40]
size_number4= [19,4,13,15,13,13,8,6,8,14,11,10,2]
size_number4_prime= [92,100,92,100,100,92,100,100,88,93,73,100,50]

# Your labels for each segment
labels_symbols = ['mini nasdaq', 'mini s&p', "micro s&p", "full size gold", "micro dow", "micro nasdaq",
                  "micro crude", "full size crude", "mini dow", "micro gold", "micro ether", "micro bitcoin", "micro euro fx"]

# Calculate the total sizes
whole_size = [size_number1[i] + size_number2[i] + size_number3[i] + size_number4[i] for i in range(len(size_number1))]
whole_size_prime = [size_number1_prime[i] + size_number2_prime[i] + size_number3_prime[i] + size_number4_prime[i] for i in range(len(size_number1_prime))]

# Create figure with 2 subplots side by side
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Pie chart for whole_size
axs[0].pie(whole_size, labels=labels_symbols, autopct='%1.1f%%')
axs[0].set_title('Sum of sizes (Whole Size)')

# Pie chart for whole_size_prime
axs[1].pie(whole_size_prime, labels=labels_symbols, autopct='%1.1f%%')
axs[1].set_title('Sum of sizes (Whole Size Prime)')

plt.suptitle("the whole information of the first four winners of leap",fontsize=20)
plt.tight_layout()
plt.show()