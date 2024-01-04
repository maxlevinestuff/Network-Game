#tests PyPlot

import matplotlib.pyplot as plt
plt.style.use('ggplot')

#x = ['Rational', 'Random', 'Greedy', 'Myopic', 'Rational', 'Random', 'Greedy', 'Myopic']
x_values = [10, 15, 20, 25]
results = [1.7339668273925781, 3.157149076461792, 3.3661611080169678, 4.166335105895996]

#x_pos = [i for i, _ in enumerate(x)]

#plt.plot(x_pos, run1, color='black')
plt.plot(x_values, results)
plt.xlabel("Total moves")
plt.ylabel("Runtime")
#plt.ylim(0.8, 1.01)
plt.title("Total moves affecting runtime")

#plt.xticks(x_pos, x)

plt.show()