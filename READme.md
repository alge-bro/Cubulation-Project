This is an algorithm designed to cubulate hyperbolic groups. Given a square complex, it automatically builds out the missing structure needed to satisfy Gromov's Link Condition, producing a CAT(0) cube complex. This was written as part of an honors thesis in geometric group theory

A cube complex is CAT(0) precisely when the link of every vertex is a flag complex. i.e. whenever a set of vertices is pairwise connected, that whole set has to be filled in as a higher simplex, as pairwise connected is not sufficient. Checking the condition naively means testing every subset of vertices to see if it should be a simplex, which is combinatorially demanding. 

Early brute force enumeration over the full vertex and subset structure scaled exponentially combinatorially, and for larger test groups the candidate space grew into the billions as the structure was walked vertex by vertex. The fix was to stop checking subsets and instead target the maximal cliques directly using the Bron-Kerbosch algorithm, which states that any maximal clique in the vertex adjacency graph is a candidate simplex, and checking specifically those against the existing complex is far less demanding than testing every possible subset. Whatever cliques are missing from the complex tell you exactly where the link condition fails and become the corner that the algorithm fills in next.

How it works:
You start from a square complex, a set of 4 cycles (the edges forming a square), representing the known 2 dimensional structure. 
You then build the link complex with the function linkComplexFromSquares and extract vertices and edges from every square face.
We check the flag condition by calling simplex_algorithm.py, which proceeds to build the vertex adjacency graph, run Bron-Kerbosch to find the maximal cliques, and check each one against the current complex. Any clique of size >=3 that's missing is a corner where the link condition fails
We then proceed to patch the missing corners with the function addCubeFromCorner, and for each missing corner we find which of its edges already belong to a square face and which don't. For edges with no square yet, we introduce fresh generator pairs (new vertices) and construct a new square face connecting them (through the function makeSquareFromEdge), which extends the complex outwards.
We then recurse using runFlagCubulationRecursion and rebuild the link complex and recheck the flag condition. We repeat until no missing corners remain (the complex is flag, and therefore CAT(0)) or no progress is made within a step limit in the recursion.

main.py operates as the cubulationAlgorithm class, it contains square/cube bookkeeping, corner patching, and the main recursion loop. It also contains the runnable test case based off the presentation at the bottom of the file.
simplex_algorithm.py is the simplexAlgorithm class, it builds the vertex adjacency graph and runs Bron-Kerbosch to find maximal cliques, which makes the flag condition check trackable. 

Status:
This is thesis research code, not a packaged library. It includes debug print statements used during development and a hardcoded test case at the bottom of main.py rather than a proper test suite. The commented out sage.all import reflects a planned integration with SageMath that proved unnecessary and has not been wired back in because of that. The core algorithm, a clique based flag checking and recursive corner patching strategy is complete and has run successfully tested on multiple test groups. The packaging around it is still in a research state.

Background:
This work grew out of undergraduate research into geometric group theory, focused on translating CAT(0) cube complex theory and Gromov's Link Condition into a working, automated algorithm and presented as an honors thesis and undergraduate research presentation. I would like to thank my advisor Dr. Johanna Mangahas-Kutluhan for all of her help throughout the project and invaluable insight.
