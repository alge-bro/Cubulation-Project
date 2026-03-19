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
    def __init__(self,squareComplex,squareComplexAsSet,cubeComplexFaces,size):
        self.squareComplexAsSet = set(frozenset(a) for a in squareComplexAsSet)
        self.squareComplex = set(frozenset(s) for s in squareComplex)
        self.cubeComplexFaces = set(frozenset(s) for s in cubeComplexFaces)
        self.size = size

        self.simplexSet = set()
        self.foundEdges = set()
        self.needToAdd = set()
        self.currentSet = set()
        self.currentSubsets = set()
        self.currentSquareFaces = set()
        self.specificEdge = set()

        self.squareCycles = []
        self.edgeToSquare = {}
        self.cubes = []

    def addSquare(self, squareCycle):
        squareCycle = tuple(frozenset(x) for x in squareCycle)

        if len(squareCycle) != 4:
            print("attempted to add non square face, try again!", squareCycle)
            return

        if squareCycle not in self.squareCycles:
            self.squareCycles.append(squareCycle)

        self.squareComplexAsSet.add(frozenset(squareCycle))
        self.squareComplex.add(frozenset(squareCycle))

    def initializeSquareCycles(self, squareCycleList):
        for square in squareCycleList:
            self.addSquare(square)

    def buildEdgeToSquareMap(self):
        self.edgeToSquare = {}

        for square in self.squareCycles:
            for edge in square:
                if edge not in self.edgeToSquare:
                    self.edgeToSquare[edge] = []
                self.edgeToSquare[edge].append(square)

    def squareIndexOfEdge(self, square, edge):
        edge = frozenset(edge)
        for i,e in enumerate(square):
            if e == edge:
                return i
        return None

    def adjacentEdgesInSquare(self, square, edge):
        i = self.squareIndexOfEdge(square, edge)
        if i is None:
            return None
        return (square[(i-1) % 4], square[(i+1) % 4])

    def oppositeEdgeInSquare(self, square, edge):
        i = self.squareIndexOfEdge(square, edge)
        if i is None:
            return None
        return square[(i+2) % 4]


    def linkComplexFromSquares(self):
        self.simplexSet = set()
        for square in self.squareComplexAsSet:
            for x in square:
                x = frozenset(x)
                self.simplexSet.add(x)
                for y in x:
                    self.simplexSet.add(frozenset({y}))

        return self.simplexSet

    def freshVertexLabel(self):
        self.size += 1
        return self.size

    def freshGeneratorPair(self):
        a = self.freshVertexLabel()
        b = self.freshVertexLabel()
        return frozenset({a,b})


    def createPowerSet(self, s):
        s = sorted(s)
        return set(map(frozenset, chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))))

    '''
    written as a helper, when going up dimension size will become relevant, as of now fixed at 2
    '''

    def edgesFromSimplex(self, simplexSet, dimSize):
        found = set()
        for simplex in simplexSet:
            for subset in combinations(simplex, dimSize):
                found.add(frozenset(subset))
        return found

    def checkSubsetOf(self, squareComplex, currentSet):
        for subsets in squareComplex:
            if currentSet.issubset(subsets):
                return subsets
        print("nothing")

    def simplicialConditionAdd(self,simplex):
        simplex = frozenset(simplex)
        powerSet = self.createPowerSet(simplex)
        powerSet.discard(frozenset())
        self.simplexSet.update(powerSet)
        return powerSet

    def edgesOfCorner(self,corner):
        corner = sorted(list(corner))
        return {frozenset(x) for x in combinations(corner, 2)}

    def maxVertexLabel(self):
        m = 0
        for s in self.simplexSet:
            for x in s:
                if isinstance(x, int):
                    if x > m:
                        m = x
        if m == 0:
            return self.size
        return m

    def squaresContainingEdge(self,edge):
        edge = frozenset(edge)
        temporary = []
        for square in self.squareCycles:
            if edge in square:
                temporary.append(square)
        return temporary

    def chooseSquareForEdge(self,edge):
        touches = self.squaresContainingEdge(edge)
        if(len(touches)==0):
            return None
        return touches[0]

    def newCubeRecord(self, seedCorner):
        return {
            "seed": frozenset(seedCorner),
            "corners": set(),
            "square faces": set(),
            "missing edges": set(),
            "new labels": set()
        }

    def makeSquareFromEdge(self, edge, oppositeEdge):
        edge = tuple(edge)
        oppositeEdge = tuple(oppositeEdge)

        a, b = edge
        c, d = oppositeEdge

        return (
            frozenset({a, b}),
            frozenset({b, d}),
            frozenset({c, d}),
            frozenset({a, c})

        )

    def inferCornersFromSeed(self, corner):
        corner = frozenset(corner)
        found = set()
        for edge in self.edgesOfCorner(corner):
            squares = self.edgeToSquare.get(edge, [])
            if not squares:
                continue
            square = squares[0]
            opp = self.oppositeEdgeInSquare(square, edge)
            if opp is None:
                continue
            candidate = edge.union(opp)

            if len(candidate) == 3:
                found.add(frozenset(candidate))

        return found


    def addCubeFromCorner(self,corner):
        corner = frozenset(corner)
        cube = self.newCubeRecord(corner)

        self.simplicialConditionAdd(corner)
        cube["corners"].add(corner)
        self.cubeComplexFaces.add(corner)

        cornerEdges = self.edgesOfCorner(corner)

        for edge in cornerEdges:
            squares = self.edgeToSquare.get(edge, [])
            square = squares[0] if squares else None
            if square is not None:
                cube["square faces"].add(frozenset(square))
                self.cubeComplexFaces.add(frozenset(square))
            else:
                cube["missing edges"].add(edge)
                self.needToAdd.add(edge)

        for edge in list(cube["missing edges"]):
            newOppositeEdge = self.freshGeneratorPair()
            cube["new labels"].update(newOppositeEdge)

            newSquare = self.makeSquareFromEdge(edge, newOppositeEdge)
            self.addSquare(newSquare)

            cube["square faces"].add(frozenset(newSquare))
            self.cubeComplexFaces.add(frozenset(newSquare))

        self.buildEdgeToSquareMap()

        newCorners = self.inferCornersFromSeed(corner)

        for newCorner in newCorners:
            self.simplicialConditionAdd(newCorner)
            cube["corners"].add(newCorner)
            self.cubeComplexFaces.add(newCorner)

        self.cubes.append(cube)
        return cube

    def runFlagCubulationRecursion(self, maxSteps=50):

        steps = 0

        while steps < maxSteps:
            steps += 1

            self.buildEdgeToSquareMap()
            self.linkComplexFromSquares()

            currentSize = self.maxVertexLabel()
            simplexObject = simplexAlgorithm(self.simplexSet, currentSize)
            missing = simplexObject.checkIfComplexIsFlag()

            missingCorners = set()
            for x in missing:
                if len(x) >= 3:
                    missingCorners.add(x)

            if len(missingCorners) == 0:
                print("cubulation finished, link complex is flag (sorta)")
                return self.cubeComplexFaces, self.simplexSet, self.needToAdd

            print("current recursion", steps, ": adding cubes for corners", list(missingCorners))

            oldSquareCount = len(self.squareCycles)
            oldSimplexCount = len(self.simplexSet)

            for corner in missingCorners:
                self.addCubeFromCorner(corner)

            self.buildEdgeToSquareMap()
            self.linkComplexFromSquares()

            if len(self.squareCycles) == oldSquareCount and len(self.simplexSet) == oldSimplexCount:
                print("no progress made, terminating program")
                return

        if steps >= maxSteps:
            print("recursed? too long!", maxSteps)

        return self.cubeComplexFaces, self.simplexSet, self.needToAdd



sq1 = (
    frozenset({6,1}),
    frozenset({2,6}),
    frozenset({5,2}),
    frozenset({1,5}),
)
sq2 = (
    frozenset({6,3}),
    frozenset({4,6}),
    frozenset({1,4}),
    frozenset({3,1}),
)
sq3 = (
    frozenset({5,8}),
    frozenset({7,5}),
    frozenset({2,7}),
    frozenset({8,2}),
)

squareCycleList = [sq1, sq2, sq3]
squareComplexAsSet = [set(sq1), set(sq2), set(sq3)]
squareComplex = [set(sq1), set(sq2), set(sq3)]
cubeComplexFaces = []

cubeObj = cubulationAlgorithm(squareComplex, squareComplexAsSet, cubeComplexFaces, 8)

cubeObj.initializeSquareCycles(squareCycleList)

cubeObj.buildEdgeToSquareMap()

cubeObj.linkComplexFromSquares()

print("square cycles =", cubeObj.squareCycles)
print("edge to square map =", cubeObj.edgeToSquare)
print("intial simplex set =", cubeObj.simplexSet)

simplexObj = simplexAlgorithm(cubeObj.simplexSet, cubeObj.maxVertexLabel())
missing = simplexObj.checkIfComplexIsFlag()
print("missing simplices =", missing)

missingCorners = set()
for x in missing:
    if len(x) >= 3:
        missingCorners.add(x)

print("missing corners =", missingCorners)

testCorner = None
for x in missingCorners:
    testCorner = x
    break
print("testCorner =", testCorner)

if testCorner is not None:
    inferred = cubeObj.inferCornersFromSeed(testCorner)
    print("inferred corners from seed =", inferred)

result = cubeObj.runFlagCubulationRecursion()
print("final resutl hopefully :", result)



