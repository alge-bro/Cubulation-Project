#from sage.all import *
from itertools import chain, combinations

'''
accept input size of S and accept input of complex X
take input and develop set from it, i.e. input = 4 then set = {1,2,3,4}
take new set and create power set
go through X and check if it is a valid simplex complex, starting from size 2 and moving up
each time there is a missing set, store it in a secondary set and append at the end to make a valid complex
check that X' is flag
'''


class simplexAlgorithm:


    def __init__(self, inputSet, inputSize=None,vertexSet=None):
        self.inputSet = set(frozenset(s) for s in inputSet)
        self.inputSize = inputSize
        self.setFromSize = set()
        self.powerSet = set()
        self.returnSet = set()
        self.vertexSet = set(vertexSet) if vertexSet is not None else None

    def developSetFromSize(self):
        self.setFromSize.clear()
        if self.vertexSet is not None:
            return set(self.vertexSet)
        if self.inputSize is not None:
            return set(range(1, int(self.inputSize)+1))

        vertex = set()
        for simplex in self.inputSet:
            for vert in simplex:
                vertex.add(vert)

        return vertex

    def createPowerSet(self, s):
        s = sorted(s)
        return set(map(frozenset, chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))))

    def sizeOfSubset(self, x):
        return len(x)

    def checkIfValidComplex(self):
        sortedSet = sorted(self.inputSet, key=self.sizeOfSubset, reverse=True)
        currentlyChanged = True
        while currentlyChanged:
            currentlyChanged = False
            whatToAdd = set()
            for subsets in sortedSet:
                currentPowerSet = self.createPowerSet(subsets)
                currentPowerSet.discard(frozenset())
                tempSet = currentPowerSet - self.inputSet
                if len(tempSet) != 0:
                    print("Added ", list(tempSet), " to complex")
                    whatToAdd.update(tempSet)
                    currentlyChanged = True
        self.inputSet.update(whatToAdd)

        return self.inputSet

    '''
    New code from Dr.Mangahas notes
    '''
    def currentBuildAdjacency(self, vertices, edges):
        adjacentSet = {v: set() for v in vertices}

        for edge in edges:
            edgeList = list(edge)
            if len(edgeList) == 2:
                u = edgeList[0]
                v = edgeList[1]
                adjacentSet[u].add(v)
                adjacentSet[v].add(u)

        return adjacentSet

    '''
    Algorithm utilizing Bron-Kerbosch algorithm, universal fast/efficient 
    algorithm for finding maximal cliques (thanks Bron-Kerbosch)
    pesudocode for reference:
    algorithm BronKerbosch2(R, P, X) is
    if P and X are both empty then
        report R as a maximal clique
    choose a pivot vertex u in P ⋃ X
    for each vertex v in P \ N(u) do
        BronKerbosch2(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
        P := P \ {v}
        X := X ⋃ {v}
    '''
    def bronKerboschAlgorithm(self, R, P, X, adjacent, cliques):
        if not P and not X:
            if len(R) >= 2:
                cliques.append(frozenset(R))
            return

        candidatesForPivot = P | X

        def pivotRank(v):
            neighborsOfV = adjacent[v] & P
            return len(neighborsOfV)

        pivot = max(candidatesForPivot, key=pivotRank)

        verticesToLoopOver = list(P-adjacent[pivot])

        for v in verticesToLoopOver:
            newR = R | {v}
            newP = P & adjacent[v]
            newX = X & adjacent[v]
            self.bronKerboschAlgorithm(newR, newP, newX, adjacent, cliques)
            P = P - {v}
            X = X | {v}



    '''
    "Take the input of the simplicial complex, and extract its graph. 
    Find all maximal cliques of the graph. Each maximal clique defines a 
    simplex. For each simplex, ask whether it is in the complex.
     Any time the answer is no corresponds to a missing simplex"
    '''

    def checkIfComplexIsFlag(self):
        self.returnSet.clear()
        S = self.developSetFromSize()

        # only use edges actually present
        edges = set()
        for simplex in self.inputSet:
            if len(simplex) == 2:
                edges.add(simplex)

        adjacent = self.currentBuildAdjacency(S, edges)


        '''
        New part of utilizing cliques and the bron-Kerbosch algorithm
        '''
        cliques = []
        startingR = frozenset()
        startingP = set(S)
        startingX = set()

        self.bronKerboschAlgorithm(startingR, startingP, startingX, adjacent, cliques)

        for clique in cliques:
            cliqueAsFrozenSet = frozenset(clique)
            cliqueInComplex = cliqueAsFrozenSet in self.inputSet
            if not cliqueInComplex:
                self.inputSet.add(cliqueAsFrozenSet)
                self.returnSet.add(cliqueAsFrozenSet)
                print(f"MORE WORK NEEDED! {sorted(cliqueAsFrozenSet)} was not found, now added!")

        if not self.returnSet:
            print("COMPLEX IS FLAG")

        return self.returnSet









'''
Replaced big part of algorithm
no longer call develop set from size, saves time
no long creating long chains of JUST triples, focus on cliques instead
'''
