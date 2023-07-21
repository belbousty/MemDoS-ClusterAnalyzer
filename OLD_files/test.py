import matplotlib.pyplot as plt
import numpy as np

# Data for the three bars
bar1_height = 10
bar2_height = 15
bar3_height = 20

# X-axis values for the bars
x = np.array([1, 2, 4])

# Plot the bars
plt.bar(x[:2], [bar1_height, bar2_height], color='maroon', width=0.4)
plt.bar(x[2], bar3_height, color='blue', width=0.4)

# Set the labels and title
plt.xlabel('Bars')
plt.ylabel('Height')
plt.title('Bar Plot')

# Set the x-axis tick labels
plt.xticks(x, ['Bar 1', 'Bar 2', 'Bar 3'])

# Show the plot
plt.show()
