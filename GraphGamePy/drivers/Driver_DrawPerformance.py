#Draws the performance data gotten from Driver_PerformanceTest

import matplotlib.pyplot as plt

nodes1 = [4.88658, 6.4118, 8.830296, 15.49839, 16.093472, 251.26761]
nodes2 = [2.4547239999999997, 5.29112, 12.012574, 77.17876, 41.95992, 21.795093999999978]
nodes3 = [5.099608, 7.111701999999999, 11.112254, 13.911382, 120.51456400000001, 66.60274000000001]

nodes_avg = []
for i in range(0, len(nodes1)):
	nodes_avg.append(nodes1[i] + nodes2[i] + nodes3[i])
	nodes_avg[i] /= 3
print(nodes_avg)

plt.plot(list(range(5, 35, 5)), nodes_avg, color="black", linestyle="dashed")
plt.ylim(0, 400)
plt.ylabel("Seconds")
plt.xlabel("Number of Nodes")
plt.savefig('demo1.png', transparent=True)
plt.clf()

connect1 = [9.311761999999987, 9.840071999999964, 21.444457999999997, 7.894007999999985, 87.60535400000003, 258.70328399999994, 1084.992768]
connect2 = [9.844489999999979, 8.309091999999993, 16.989038000000022, 15.269335999999981, 110.43715199999997, 168.45679, 37.503916000000004]
connect3 = [11.545006, 9.200574000000017, 8.770616000000018, 69.456006, 9.499353999999983, 307.44777999999997, 18.706182000000013]

connect_avg = []
for i in range(0, len(connect1)):
	connect_avg.append(connect1[i] + connect2[i] + connect3[i])
	connect_avg[i] /= 3
print(connect_avg)

plt.plot([0.15, 0.20, 0.25, 0.3, 0.35, 0.4, 0.45], connect_avg, color="black")
plt.ylim(0, 400)
plt.ylabel("Seconds")
plt.xlabel("Connectedness")
plt.savefig('demo2.png', transparent=True)
plt.clf()

plt.plot([0.15, 0.20, 0.25, 0.3, 0.35, 0.4, 0.45], [50, 50, 50, 50, 50, 50, 50], color="black")
plt.ylim(0, 400)
plt.xlim(0.15, 0.45)
plt.ylabel("Seconds")
plt.xlabel("Connectedness")
plt.savefig('demo3.png', transparent=True)
plt.clf()