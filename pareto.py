from agent import Agent

def isParetoImprovment(agents:list[Agent], option1:int, option2:int) -> bool:
    """
    Option1 is called "Pareto Improvment" to option2 if it benefits 
    at least one person without making it worse for anyone else.
    >>> isParetoImprovment([Agent([1, 2, 3, 4, 5]), Agent([3, 1, 2, 5, 4] ), Agent([3, 5, 5, 1, 1] )], 1, 2)
    False
    >>> isParetoImprovment([Agent([1, 2, 3, 4, 5]), Agent([3, 1, 2, 5, 4] ), Agent([3, 5, 5, 1, 1] )], 2, 1)
    True
    """
    # return False if at least one agent loses on the option2
    for agent in agents:
        if agent.value(option1) < agent.value(option2):
            return False
            
    # return False if none of the agents gains anything
    for agent in agents:
        if agent.value(option1) > agent.value(option2):
            return True

    # return false because both options are the same (therefore, can't be an improvment)
    return False

def isParetoOptimal(agents:list[Agent], option:int, allOptions:list[int]) -> bool:
    """
    option is Pareto Optimal (aka Pareto Efficient) if none of the other 
    options (allOptions) are Pareto Improvment to it.
    >>> isParetoOptimal([Agent([1, 2, 3, 4, 5]), Agent([3, 1, 2, 5, 4] ), Agent([3, 5, 5, 1, 1] )], 1, [0, 2, 3, 4])
    False
    >>> isParetoOptimal([Agent([1, 2, 3, 4, 5]), Agent([3, 1, 2, 5, 4] ), Agent([3, 5, 5, 1, 1] )], 2, [0, 1, 3, 4])
    True
    """
    for otherOption in allOptions:
        if isParetoImprovment(agents=agents, option1=otherOption, option2=option):
            return False
    return True
def egalitarian(agents:list[Agent], allOptions:list[int]=[0,1,2,3,4]) -> int:
    """
    gets a list of agents and options, returns the option that is egalitarian.
    returns the option that maximizes the minimum value for an agent
    >>> egalitarian([Agent([1, 2, 3, 4, 5]), Agent([3, 1, 2, 5, 4]), Agent([3, 5, 5, 1, 1])])    
    2
    """
    z=0
    maxMin = -1
    for i in allOptions:
        currMin = 9999999
        for agent in agents:
            if agent.value(i) < currMin:
                currMin = agent.value(i)
        if currMin > maxMin:
            maxMin = currMin
            z = i

    return z


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)