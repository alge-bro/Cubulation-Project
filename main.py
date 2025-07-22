from simplex_program.simplex_algorithm import simplexAlgorithm

testSet = frozenset([frozenset({1,2,3}),frozenset({1,2,4}),frozenset({2,3,4})])
size = 4
testObj = simplexAlgorithm(testSet,size)
testObj.checkIfValidComplex()
testObj.checkIfComplexIsFlag()
