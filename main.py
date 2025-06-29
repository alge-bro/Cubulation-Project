from simplex_program.simplex_algorithm import simplexAlgorithm

testSet = frozenset([frozenset({1}),frozenset({2}),frozenset({3}),frozenset({4}),frozenset({1,2}),frozenset({1,4}),frozenset({3,4}),
                     frozenset({1,2,4})])
size = len(testSet)
testObj = simplexAlgorithm(testSet,size)
testObj.checkIfValidComplex()
testObj.checkIfComplexIsFlag()
