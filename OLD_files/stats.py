import matplotlib.pyplot as plt
import numpy as np 


l3_misses_empty = []
with open('without_att.txt', 'r') as file:
    for line in file:
        if 'l3_misses' in line:
            l3_misses_empty.append(int(line.split()[0]))
l3_misses_attack = []
with open('att_effect.txt', 'r') as file:
    for line in file:
        if 'l3_misses' in line:
            l3_misses_attack.append(int(line.split()[0]))

l3_misses_attack_LLC = []
with open('LLC_effect.txt', 'r') as file:
    for line in file:
        if 'l3_misses' in line:
            l3_misses_attack_LLC.append(int(line.split()[0]))

iterations = np.arange(len(l3_misses_attack))
plt.bar([1,1.5,2], l3_misses_empty, color ='maroon',
        width = 0.4, label='Normal Behaviour')
plt.bar([4,4.5,5], l3_misses_attack, width = 0.4, label="Atomic locking")
plt.bar([7,7.5,8], l3_misses_attack_LLC, width = 0.4, label="LLC cleansing")


plt.legend()

x_ticks = np.concatenate(([1, 1.5, 2], [4, 4.5, 5], [7,7.5,8]))
x_tick_labels = ["T1", "T2", "T3", "T1", "T2", "T3", "T1", "T2", "T3"]
plt.xticks(x_ticks, x_tick_labels)

plt.ylabel('L3 Misses')
plt.title('L3 Misses Statistics')
plt.show()
