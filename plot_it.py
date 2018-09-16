import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from time import sleep

def animate():
	times = [0,1,2,3,4,5,6,7,8,9]
	players = [[0,1,2,3,4,5,6,7,8,9], [0,1,2,3,4,5,6,7,8,9], [0,1,2,3,4,5,6,7,8,9], [4,1,6,3,4,7,1,7,9,9]]
	player_ids = ["Player 1", "Player 2", "Player 3", "Player 4"]
	bottoms = [[0 for i in range(len(players[0]))]]

	N = len(times)
	ind = np.arange(N)
	width = 0.35
	bars = []

	for i in range(len(players)):
		if i == 0:
			plt.pause(0.3)
			bars.append(plt.bar(ind, players[i], width))
			plt.pause(0.3)
			continue
		else:
			#bottom is where this bar should start. We keep track of the sum to stack the bars correctly
			plt.pause(0.3)
			bottoms.append([players[i-1][t]+bottoms[i-1][t] for t in range(len(players[i]))])
			plt.pause(0.3)
			bars.append(plt.bar(ind, players[i], width, bottom = bottoms[i]))


	plt.title("Work Load Distribution by Player")
	plt.yticks(np.arange(0, 101, 10))
	plt.ylabel("Percent Completed (%)")
	plt.xticks(ind, times)
	plt.xlabel("Time Since Start (seconds)")

	plt.legend(tuple(bars), tuple(player_ids))
	plt.show()
	plt.pause(0.4)

if __name__ == "__main__":
	#fig = plt.figure()
	#ax1 = fig.add_subplot(1,1,1)
	#ani = animation.FuncAnimation(fig, animate, interval = 1000)
	animate()
