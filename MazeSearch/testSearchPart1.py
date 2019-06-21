import SearchBFSDFS
import SearchAstarGreedy
import StateSpace

print("Medium : DFS");
sp1 = StateSpace.StateSpace("MediumMaze.txt")
S1 = SearchBFSDFS.SearchBFSDFS(sp1)
S1.BFS_DFS(True)
S1.results()


print("Medium: BFS")
sp2 = StateSpace.StateSpace("MediumMaze.txt")
S2 = SearchBFSDFS.SearchBFSDFS(sp2)
S2.BFS_DFS()
S2.results()

print("Medium : SearchGreedy")
sp3 = StateSpace.StateSpace("MediumMaze.txt")
S3 = SearchAstarGreedy.SearchAstarGreedy(sp3)
S3.Greedy_Astar()
S3.results()

print("Medium : SearchAstar")
sp4 = StateSpace.StateSpace("MediumMaze.txt")
S4 = SearchAstarGreedy.SearchAstarGreedy(sp4)
S4.Greedy_Astar(True)
S4.results()


print("Big: DFS");
sp5 = StateSpace.StateSpace("BigMaze.txt")
S1 = SearchBFSDFS.SearchBFSDFS(sp5)
S1.BFS_DFS(True)
S1.results()

print("Big: BFS")
sp6 = StateSpace.StateSpace("BigMaze.txt")
S2 = SearchBFSDFS.SearchBFSDFS(sp6)
S2.BFS_DFS()
S2.results()

print("Big: SearchGreedy")
sp7 = StateSpace.StateSpace("BigMaze.txt")
S3 = SearchAstarGreedy.SearchAstarGreedy(sp7)
S3.Greedy_Astar()
S3.results()

print("Big: SearchAstar")
sp8 = StateSpace.StateSpace("BigMaze.txt")
S4 = SearchAstarGreedy.SearchAstarGreedy(sp8)
S4.Greedy_Astar(True)
S4.results()

print("Open: DFS");
sp9 = StateSpace.StateSpace("OpenMaze.txt")
S1 = SearchBFSDFS.SearchBFSDFS(sp9)
S1.BFS_DFS(True)
S1.results()

print("Open: BFS")
sp10 = StateSpace.StateSpace("OpenMaze.txt")
S2 = SearchBFSDFS.SearchBFSDFS(sp10)
S2.BFS_DFS()
S2.results()

print("Open: SearchGreedy")
sp11 = StateSpace.StateSpace("OpenMaze.txt")
S3 = SearchAstarGreedy.SearchAstarGreedy(sp11)
S3.Greedy_Astar()
S3.results()

print("Open :SearchAstar")
sp12 = StateSpace.StateSpace("OpenMaze.txt")
S4 = SearchAstarGreedy.SearchAstarGreedy(sp12)
S4.Greedy_Astar(True)
S4.results()
