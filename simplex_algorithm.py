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
    missingPartsSet = set()
    mainSet = set()
    finalFace = set()
    int = 1
    currentTemp = set()
    missingForFlag = set()

    def __init__(self, inputSet, inputSize):
        self.inputSet = set(frozenset(s) for s in inputSet)
        self.inputSize = inputSize
        self.setFromSize = set()
        self.powerSet = set()

    def developSetFromSize(self):
        self.setFromSize.clear()
        for i in range(1, self.inputSize+1):
            self.setFromSize.add(i)
        return self.setFromSize

    def createPowerSet(self, s):
        s = sorted(s)
        return set(map(frozenset, chain.from_iterable(combinations(s,r) for r in range(len(s)+1))))

    def sizeOfSubset(self, x):
        return len(x)

    def checkIfValidComplex(self):
        #sorts set into largest size subset to smallest
        sortedSet = sorted(self.inputSet, key=self.sizeOfSubset, reverse=True)
        #loop through each set inside the larger set
        for subsets in sortedSet:
            #attatches variable to current set we are working with
            currentSetAsList = list(subsets)
            #attatches variable to size of set
            sizeOfCurrentSet = len(subsets)
            if sizeOfCurrentSet == 1:
                self.finalFace.add(subsets)
            #deal with case of sets of size {x,y}
            if sizeOfCurrentSet == 2:
                #walk through current set per element
                for n in currentSetAsList:
                    #turns the current value into a set, i.e. {1,2} -> 1 -> {1}
                    current = frozenset({n})
                    #checks if the current singleton is in the entire original complex
                    if current not in self.inputSet:
                        #if not in the original complex, report it to terminal and union it to new set
                        print("Added ", current, " to complex")
                        self.missingPartsSet.add(current)
            #anything of size larger than 2
            else:
                #creates powerset with current set working with, i.e. {1,2,3} = {1},{2},{3},{1,2},{2,3},{1,3},{1,2,3}
                currentPowerSet = self.createPowerSet(subsets)
                currentPowerSet.discard(frozenset())
                #now we have all required sets that must be in the complex to make this certain set valid in the complex
                #retrieve the missing sets from the complex
                tempSet = currentPowerSet - self.inputSet
                #missingPartsSet now contains all potential missing parts required for the complex to be valid with the current set
                if len(tempSet) != 0:
                    print("Added ", list(tempSet), " to complex")
                    self.missingPartsSet.update(tempSet)
                '''
                #gives us desired sets of the size we want to check, i.e. {1,2,3} = {1},{2},{3},{1,2},{2,3},{1,3},{1,2,3} with
                #size 2 gives us {1,2},{2,3},{1,3}
                desiredSets = {s for s in currentPowerSet if len(s) == sizeOfCurrentSet-1}
                #sorts through current sets, i.e. {1,2},{2,3},{1,3}
                for x in desiredSets:
                    #if not in complex, which it should be, report to terminal and union it with new set
                    if x not in self.inputSet:
                        print("Added ", x, " to complex")
                        self.missingPartsSet | x
             
               '''
        '''
        done finding missing pieces, but what if the missing pieces are missing pieces in the complex
        i.e. X = {{1},{2},{1,2},{1,2,3}}
        first part finds that {1,3},{2,3} is missing, and adds it to missingPartsSet
        but X is still missing {3}, so we need to run it again to find whats missing
        I believe the new powerset system with disjoint and union work better, and could solve this problem
        '''
        self.inputSet |= self.missingPartsSet
        
        return self.inputSet
    '''
    Let S be a set, X is flag if:
    For any S' in P(S) s.t. P(S') - {S'} is a subset of X, we have S' in X also
    '''
    def checkIfComplexIsFlag(self):
        #create set from inputted size
        S = self.developSetFromSize()
        #create power set based off inputted size
        powerSetOfS = self.createPowerSet(S)
        powerSetOfS.discard(frozenset())
        #sort power set to work large to small
        sortedPowerSet = sorted(powerSetOfS, key=self.sizeOfSubset, reverse=True)
        #for any S' in P(S)
        for sPrime in sortedPowerSet:
            #create P(S')
            powerSetOfsPrime = self.createPowerSet(sPrime)
            powerSetOfsPrime.discard(frozenset())
            #create P(S') - {S'}
            workingSet = powerSetOfsPrime - {sPrime}
            #check P(S')-{S'} is a subset of X
            if workingSet.issubset(self.inputSet):
                #S' in X
                if sPrime not in self.inputSet:
                    self.missingForFlag.add(sPrime)
                    print("Complex is not flag! added ", sPrime)
        return self.missingForFlag










'''
references

powerset function : https://www.youtube.com/watch?v=gXDTQEFzimU


'''