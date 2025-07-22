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
    setFromSize = set()
    powerSet = set()
    #missingForFlag = set()

    def __init__(self, inputSet, inputSize):
        self.inputSet = set(frozenset(s) for s in inputSet)
        self.inputSize = inputSize
        self.setFromSize = set()
        self.powerSet = set()

    def developSetFromSize(self):
        self.setFromSize.clear()
        for i in range(1, self.inputSize + 1):
            self.setFromSize.add(i)
        return self.setFromSize

    def createPowerSet(self, s):
        s = sorted(s)
        return set(map(frozenset, chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))))

    def sizeOfSubset(self, x):
        return len(x)

    def checkIfValidComplex(self):
        sortedSet = sorted(self.inputSet, key=self.sizeOfSubset, reverse=True)
        #print(sortedSet)
        for subsets in sortedSet:
            #print(subsets)
            currentPowerSet = self.createPowerSet(subsets)
            currentPowerSet.discard(frozenset())
            tempSet = currentPowerSet - self.inputSet
            #print(tempSet)
            if len(tempSet) != 0:
              print("Added ", list(tempSet), " to complex")
              self.inputSet.update(tempSet)
        return self.inputSet

    '''
    Let S be a set, X is flag if:
    For any S' in P(S) s.t. P(S') - {S'} is a subset of X, we have S' in X also
    '''

    def checkIfComplexIsFlag(self):
        S = self.developSetFromSize()
        currentSet = set()
        comparisonSet = set()
        flagSet = set()
        sizeOneSet = set()

        powerSetOfS = self.createPowerSet(S)
        powerSetOfS.discard(frozenset())
        sortedPowerSet = sorted(powerSetOfS, key=self.sizeOfSubset, reverse=False)
        # for any S' in P(S)
        for sPrime in sortedPowerSet:
            if self.sizeOfSubset(sPrime) > 2:
                # create P(S')
                powerSetOfsPrime = self.createPowerSet(sPrime)
                powerSetOfsPrime.discard(frozenset())
                # create P(S') - {S'}
                workingSet = powerSetOfsPrime - {sPrime}
                # check P(S')-{S'} is a subset of X
                if workingSet.issubset(self.inputSet):
                    # S' in X
                    if sPrime not in self.inputSet:
                        self.inputSet.add(sPrime)
                        print("Complex is not flag! added ", sPrime)
        '''
        for s in self.inputSet:
            if len(s) == 1:
                sizeOneSet.add(s)
        sortedSet = sorted(self.inputSet, key = self.sizeOfSubset, reverse=False)
        for setX in sortedSet:
            for certainSizeSet in sortedSet:
                if(len(setX) == len(certainSizeSet)):
                    currentSet.add(certainSizeSet)
                if(len(setX)+1 == len(certainSizeSet)):
                    comparisonSet.add(certainSizeSet)
        '''



        print("flag!")
        #return self.missingForFlag