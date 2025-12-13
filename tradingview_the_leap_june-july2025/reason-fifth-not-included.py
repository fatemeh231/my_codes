"""
@author:seyedeh fatemeh hosseininasab
"""
import matplotlib.pyplot as plt

n8=[90,86,80,96,34]
n9=[10,14,20,6,66]
labels = ['first', 'second', 'third', 'fourth', 'fifth']
plt.scatter(n8, n9)
plt.ylabel("lose percentage")
plt.xlabel("win percentage")
plt.title("win to lose ratio")
for i, label in enumerate(labels):
    plt.text(n8[i], n9[i], label, fontsize=11, ha='right')

plt.text(35,30, """"Note: The fifth data point is an outlier and will be \n
excluded from the overall analysis due to its significant\n 
difference from the other data points""", fontsize=10, color='blue')
plt.show()