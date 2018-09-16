import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import requests
import json
import numpy as np
from time import sleep

def get_graphData():
    #server_url = "http://127.0.0.1:5000"
    cserver_url = "http://23.96.30.98"
    result = requests.get(server_url + '/api/graphData')
    return result.json()

def animate(graphData):
    times = [0,1,2,3,4,5,6,7,8,9]
    players = [[0,1,2,3,4,5,6,7,8,9], [0,1,2,3,4,5,6,7,8,9], [0,1,2,3,4,5,6,7,8,9], [4,1,6,3,4,7,1,7,9,9]]
    player_ids = ["Player 1", "Player 2", "Player 3", "Player 4"]
    bottoms = [[0 for i in range(len(players[0]))]]

    N = len(times)
    ind = np.arange(N)
    width = 5
    bars = []

    print(graphData)
         #for player, coord_list in graphData:

    players = []
    coord_lists = []
    for (v,k) in graphData.items():
        players.append(v)
        coord_lists.append(k)

    for i in range(len(graphData)):
        player = players[i]
        coord_list = coord_lists[i]
        x = [float(thingy[0]) for thingy in coord_list]
        y = [thingy[1] for thingy in coord_list]
        plt.pause(0.3)
        if i > 0:
            bottoms.append([coord_lists[i-1][t][1] + bottoms[i-1][t] for t in range(len(coord_list[i-1]))])
        bars.append(plt.bar(x,y,width))


        #
        # for i in range(len(players)):
        #       if i == 0:
        #               plt.pause(0.3)
        #               bars.append(plt.bar(ind, players[i], width))
        #               plt.pause(0.3)
        #               continue
        #       else:
        #               #bottom is where this bar should start. We keep track of the sum to stack the bars correctly
        #               plt.pause(0.3)
        #               bottoms.append([players[i-1][t]+bottoms[i-1][t] for t in range(len(players[i]))])
        #               plt.pause(0.3)
        #               bars.append(plt.bar(ind, players[i], width, bottom = bottoms[i]))


    plt.title("Work Load Distribution by Player")
    plt.ylabel("Chunks completed")
    plt.xlabel("Time Since Start (seconds)")
    plt.legend(['Player1','Player2'])

    plt.show()
    plt.pause(0.4)

if __name__ == "__main__":
        #fig = plt.figure()
        #ax1 = fig.add_subplot(1,1,1)
        #ani = animation.FuncAnimation(fig, animate, interval = 1000)
    graphData = get_graphData()
    animate(graphData)
