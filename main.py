from simplex_program.simplex_algorithm import simplexAlgorithm

testSet = frozenset([frozenset({1}),frozenset({2}),frozenset({1,2}),frozenset({1,3}),frozenset({2,3})
                     ])
size = 3
testObj = simplexAlgorithm(testSet,size)
testObj.checkIfValidComplex()
testObj.checkIfComplexIsFlag()
