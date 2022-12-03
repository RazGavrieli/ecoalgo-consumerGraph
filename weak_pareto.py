import networkx as nx
import logging
import pareto as par
import copy
e = 0.01
def find_weak_pareto_improvment(allocation: list[list[float]],valuations: list[list[float]],cycle: list = None):
    print_io(allocation, valuations, cycle)
    A, B, consumerGraph = create_consumerGraph(allocation)
    changeGraph = create_changeGraph(allocation, valuations, A)

    print_graphs_sbs(consumerGraph, changeGraph, A)
    # calculate the product of the given circle (both directions)
    prodOfFirstCircle = 1
    prodOfSecondCircle = 1
    for index in range(0,len(cycle)-2, 2):
        prodOfFirstCircle *= valuations[cycle[index]][cycle[index+1]]/valuations[cycle[index+2]][cycle[index+1]]
        prodOfSecondCircle *= valuations[cycle[len(cycle)-1-index]][cycle[len(cycle)-2-index]]/valuations[cycle[len(cycle)-3-index]][cycle[len(cycle)-2-index]]

    # check the product of the cycles and define parameters for the next algorithm
    if prodOfFirstCircle == 1 and prodOfSecondCircle == 1:
        print("can have weak pareto improvment as both prods are 1")
    if prodOfFirstCircle <= 1:
        rangeList = range(0,len(cycle)-2, 2)
        agentBjump = 2
        currItemJump = 1
    elif prodOfSecondCircle <= 1:
        rangeList = range(len(cycle)-1, 0, -2)
        agentBjump = -2
        currItemJump = -1
    if prodOfFirstCircle > 1 and prodOfSecondCircle > 1:
        print("could not find any improvment for minimal sharing")
        return

    # the algorithm changes the allocations to remove one edge from the graph 
    newAllocations = copy.deepcopy(allocation)
    flag = True
    while flag:
        rollingProd = 1
        for index in rangeList:
            agentA = cycle[index]
            agentB = cycle[index+agentBjump]
            currItem = cycle[index+currItemJump]

            currR = valuations[agentA][currItem]/valuations[agentB][currItem]
            
            if newAllocations[agentA][currItem] - e/rollingProd < 0:
                jump = newAllocations[agentA][currItem]
                newAllocations[agentB][currItem] += jump
                newAllocations[agentA][currItem] = 0
                flag = False
                break
            newAllocations[agentA][currItem] -= e/rollingProd
            newAllocations[agentB][currItem] += e/rollingProd
            rollingProd *= currR


    A, _, improvedConsumerGraph = create_consumerGraph(newAllocations)
    improvedChangeGraph = create_changeGraph(newAllocations, valuations, A)    
    print_io(newAllocations)
    print("new number of edges:" ,improvedConsumerGraph.number_of_edges(),"old number of edges:", consumerGraph.number_of_edges())
    print_graphs_sbs(improvedConsumerGraph, improvedChangeGraph, A)
    return newAllocations
    

def print_io(
allocation: list[list[float]] = None,
valuations: list[list[float]] = None,
cycle: list = None
):
    for i in allocation:
        for j in i:
            print(j, end="\t")
        print()
    print()
    # for i in valuations:
    #     for j in i:
    #         print(j, end=" ")
    #     print()
    print(cycle)

def print_graphs_sbs(g1, g2, A):
    import matplotlib.pyplot as plt

    pos1 = nx.bipartite_layout(g1, A)
    pos2 = nx.circular_layout(g2)
    for k,v in pos2.items():
    # Shift the x values of every node by 10 to the right
        v[0]+=4
    nx.draw_networkx(g1, pos=pos1)
    nx.draw_networkx(g2, pos=pos2)
    
    edge_labels = nx.get_edge_attributes(g2, "weight")
    nx.draw_networkx_edge_labels(g2, pos=pos2,edge_labels=edge_labels, label_pos=0.2)
    plt.show()

def create_consumerGraph(allocation: list[list[float]]):
    consumerGraph = nx.Graph()
    A = []
    B = []
    for index, _agent in enumerate(allocation):
        consumerGraph.add_node(("agent", index), bipartite=1)
        A.append(("agent", index))
    for index, _itemAllocatedToPlayer in enumerate(allocation[0]):
        consumerGraph.add_node(("item", index), bipartite=0)
        B.append(("item", index))

    for indexOfAgent, allocationToAgent in enumerate(allocation):
        for indexOfIem, allocatonValue in enumerate(allocationToAgent):
            if allocatonValue > 0:
                consumerGraph.add_edge(("agent", indexOfAgent), ("item", indexOfIem))
    return A, B, consumerGraph

def create_changeGraph(allocation: list[list[float]],valuations: list[list[float]], A: list):
    changeGraph = nx.DiGraph()
    for i in A:
        changeGraph.add_node(i) 
               
    for _i, i in A:
        for _j, j in A:
            if i==j:
                continue
            r = []
            iValues = valuations[i]
            jValues = valuations[j]
            for index in range(len(valuations[0])):
                if allocation[i][index] == 0:
                    continue
                r.append(iValues[index]/jValues[index])
            weightOfNewEdge = min(r)
            changeGraph.add_edge((_i,i), (_j,j), weight=("{:.3f}".format(weightOfNewEdge),str(r.index(weightOfNewEdge))))

    return changeGraph

if __name__ == "__main__":
    # allocations = [
    # [0, 1, 0.2, 0.25],
    # [1, 0, 0.25, 0.25], 
    # [0, 0, 0.55, 0.5]
    # ]
    # valuations = [
    # [20, 50, 20, 10],
    # [50, 18, 22, 10],
    # [15,15,55, 15]
    # ]
    # cycle = [0, 2, 1, 3, 2, 2, 0]
    allocations = [
    [0.9, 0.1, 0],
    [0.05, 0.9, 0.1] , 
    [0.05, 0, 0.9]
     ]
    valuations = [
    [3, 1, 6],
    [6, 3, 1],
    [1, 6, 3]
    ]
    cycle = [0, 0, 1, 2, 2, 0, 0]
    newAllo = find_weak_pareto_improvment(allocation=allocations, valuations=valuations, cycle=cycle)

    agents = []
    for i in range(len(newAllo)):
        listOfOptions = [0, 0]
        for j in range(len(newAllo[i])):
            listOfOptions[0] += newAllo[i][j]*valuations[i][j]
            listOfOptions[1] += allocations[i][j]*valuations[i][j]
            
        agents.append(par.Agent(listOfOptions))
    print("is newAllocation pareto improvment for old:",par.isParetoImprovment(agents, 0, 1))
    print("is old allocation pareto improvemnt for new:",par.isParetoImprovment(agents, 1, 0))
    print(agents)

    # cycle = [0, 1, 1, 0, 0]
    # newNewAllo = find_weak_pareto_improvment(allocation=newAllo, valuations=valuations, cycle=cycle)

    # agents = []
    # for i in range(len(newNewAllo)):
    #     listOfOptions = [0, 0]
    #     for j in range(len(newNewAllo[i])):
    #         listOfOptions[0] += newNewAllo[i][j]*valuations[i][j]
    #         listOfOptions[1] += newAllo[i][j]*valuations[i][j]
            
    #     agents.append(par.Agent(listOfOptions))
    # print("is newAllocation pareto improvment for old:",par.isParetoImprovment(agents, 0, 1))
    # print("is old allocation pareto improvemnt for new:",par.isParetoImprovment(agents, 1, 0))
    # print(agents)

