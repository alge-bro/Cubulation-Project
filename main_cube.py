from sage.all import *
from simplex_program.simplex_algorithm import simplexAlgorithm
from cubulation_program.cubulation_algorithm import cubulationAlgorithm
from itertools import chain, combinations



'''
Test for simplex algorithm


testSet = frozenset([frozenset({6,1}),frozenset({2,6}),frozenset({5,2}),frozenset({1,5}),frozenset({6,3}),frozenset({4,6}),frozenset({5,8}),frozenset({7,5}),frozenset({2,7}),frozenset({8,2}),frozenset({1,4}),frozenset({3,1})])
size = 7
testObj1 = simplexAlgorithm(testSet,size)
testObj1.checkIfValidComplex()
testObj1.checkIfComplexIsFlag()
'''

'''
Should initialize as such:
cube = [
    {(6,1),(2,6),(5,2),(1,5)}
    {(6,3),(4,6),(5,8),(7,5)}
    {(3,1),(2,7),(8,2),(1,4)}
]

square faces = [
    {(1,2),(3,4),(1,2),(3,4)}
    {(1,2),(5,6),(1,2),(5,6)}
'''

class cubulationAlgorithm:

    simplexSet = set()
    foundEdges = set()
    needToAdd = set()
    currentSet = set()
    currentSubsets = set()
    currentSquareFaces = set()
    specificEdge = set()

    def __init__(self,squareComplex,squareComplexAsSet,cubeComplexFaces,size):
        self.squareComplexAsSet = set(frozenset(a) for a in squareComplexAsSet)
        self.squareComplex = set(frozenset(s) for s in squareComplex)
        self.cubeComplexFaces = set(frozenset(s) for s in cubeComplexFaces)
        self.size = size
        self.simplexSet = set()

    def createPowerSet(self, s):
        s = sorted(s)
        return set(map(frozenset, chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))))

    '''
    written as a helper, when going up dimension size will become relevant, as of now fixed at 2
    '''
    def edgesFromSimplex(self,simplexSet,dimSize):
        pSetSimplex = self.createPowerSet(self.simplexSet)
        for subset in pSetSimplex:
            if(subset.len() == dimSize ):
                self.foundEdges.add(subset)
        return self.foundEdges

    def checkSubsetOf(self, squareComplex, currentSet):
        for subsets in self.squareComplex:
            if currentSet.issubset(subsets):
                return subsets
        print("nothing")


    def mainAlgorithm(self,squareComplex,squareComplexAsSet):
        simplexObj = simplexAlgorithm(squareComplexAsSet, self.size)
        needToAdd = simplexObj.checkIfComplexIsFlag()
        for subset in self.needToAdd:
            currentSet = subset
            pSetCurrentSet = self.createPowerSet(currentSet)
            currentSubsets = self.edgesFromSimplex(pSetCurrentSet, 2)
            for set in currentSubsets:
                for squares in self.squareComplexAsSet:
                    if set.issubset(squares):
                        self.specificEdge.add(set)







