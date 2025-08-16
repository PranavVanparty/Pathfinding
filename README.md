# Pathfinding

This repostitory currently contains the A star algorithm - used for generating the shortest path from one point to another - and a visuallization tool. You can take this and add your own algortithms to practice. 

# Installation

First clone the repo. Then do the following command in the terminal
```bash
pip install pygame
```
or 
```bash
pip3 install pygame
```
make sure to do this on the same python interpreter as the one the code is using.

# A* Algorithm
A star is simmilar to the Dijkstra's Algorithm but there is one key diffrence A Star takes into account Heuristics.
The following function is used:

F(n) = G(n) + H(n)

F is the final score that is given to the node. 
G is the distance from the start to the node.
H is the the distance from the node to the end position. I use the Manhattan Distance formula but you can also use the euclidian distance formula.

----
Preconditions:

* The start node is in the priority Queue

* The weights are all one

* All the F_scores, and G_scores are set to infinity except for the start

* Start F_socre is just the huristic score & G_score is 0
----

The algorithm starts with the start node and considers all of its neighbors. For each of its neighbors it it plugs in values into the formula and updates each of the F scores- which contains the following : F_score, where it came from, and the node. Then it puts all of these into the priority queue - which just allows you to pop the next best Node based on a criteria i.e, the F score. It pops the next best node and the cycle repeats. If a node is is considered twice and the current path that node is shorter than what was previosly then it updates the G_score of the node and recalucates its F_score then adds it to the queue. This cycle repeats until the best path is found and uses the came_from attribute to reconstruct the path.

 <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXNxZXp3N28xdXlxa2xjeDI2amtrN3c0YnJxOGoxNWJoZXFsYmQwMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/pp4LXHKCq1dK36KkWA/giphy.gif"/>



