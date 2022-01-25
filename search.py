import random
from datetime import datetime
import bisect
import heapq

class Search:

    def __init__(self, graph):
        self.graph = graph
        random.seed(datetime.now())

    def greedy_search(self, start, target):
        queue = [start]
        visited = []
        while(len(queue) > 0):
            current_node = queue.pop(0)
            if current_node != target:
                if current_node not in visited:
                    visited.append(current_node)
                    for next_node in current_node.get_neighbours():
                        if next_node not in visited:
                            next_node.set_parent(current_node)
                            gscore = next_node.manhattan_distance(target)
                            next_node.score = gscore
                            bisect.insort(queue, next_node)
            else:
                break            
        print("The number of visited nodes is: {}".format(len(visited)))

    """
        this algorithm is based on dijkstra's greedy algorithm 
        for finding the shortest path to all nodes.

        this is how it works:
            1. we create a minimum heap, This means that we have a very fast way
            of getting the minimum element. We determine the minimum element as the element
            with the shortest distance from the current_node

            2. we then that smallest node as the target, and remove that node from the list off
            targets

            3. we traverse to that node using the greedy_algorithm

            4. we then set the target as the current_node

            5. we do this over and over untill there are no more nodes
            
    """
    def dijkstra(self):
        #this queue wil contain all the targets of the supermarket in ASCENDING order(smallest in front)
        priorityQueue = []
        current_node = self.graph.start

        while(self.graph.targets):
            for item in self.graph.targets:
                heapq.heappush(priorityQueue,(current_node.manhattan_distance(item), item))
            target = heapq.heappop(priorityQueue)
            self.graph.targets.remove(target[1])

            #move to the target
            self.greedy_search(current_node, target[1])
            current_node = target[1]

        #move to the exit
        self.greedy_search(current_node, self.graph.exit)

    #broken
    def highlight_path(self):
        current_node = self.graph.exit.parent

        while current_node is not None and current_node != self.graph.start:
            current_node.set_color((248, 220, 50))
            current_node = current_node.parent

        print(self.graph.start)
        print("Path length is: {}".format(self.graph.target.distance))














