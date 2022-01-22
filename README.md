basic.py implements a dynamic programming solution to the genetic sequence alignment algorithm.<br>
efficient.py implements a space-efficient divide-and-conquer solution to the same.<br>
generate_tests.py can be used to generate random test cases. 

Observations/Insights:
1. Basic Dynamic Programming Solution
-	Let m and n be the lengths of strings X and Y respectively. 
-	The basic solution (in our case, the function alignment(X, Y)) constructs a matrix OPT of size (m+1) x (n+1) and spends constant time in calculating the value of each cell. This takes O(mn) time.
-	The function then traces the matrix from OPT[m][n] down to OPT[0][0] to produce the alignment. This takes O(m+n) time.
-	Thus, the overall time complexity is O(mn) and the overall space complexity is O(mn).

2. Space-efficient Divide-and-conquer Solution
-	It makes use of the fact that the recurrence relation used for computing OPT[i][j] depends on only three cells to the immediate left, diagonally right, and bottom of it - OPT[i-1][j], OPT[i-1][j-1], and OPT[i][j-1].
-	Hence, we only need to maintain two columns in memory instead of the whole matrix - the ith column and the (i-1)th column. The function space_efficient_alignment(X, Y) finds the optimal alignment cost between X and Y by constructing and computing such mx2 matrices.
-	However, it is now not possible to trace back the alignment as we have only the last two columns of the OPT matrix. The task then becomes to divide X and Y into subproblems such that an alignment is generated for each subproblem, and concatenated into a global alignment at the end.
-	We split Y into two equal halves. We have to find a split point for X that will give us the optimal cost. We do so by running space_efficient_alignment between every possible split of X and each half of Y (with the strings reversed) and finding the split point that gives the minimal cost.
-	The alignments of the subproblems are generated using the alignment(X,Y) function and stored in a global list P.
-	Essentially, we do O(mn) work in every step of the solution. Since the subproblems are halved in every step,
Total work done = cmn + (½)cmn + (¼)cmn + … <= 2cmn for some constant c
Thus, the overall time complexity is still O(mn) like the basic solution, but the space complexity is O(m*2) = O(m) i.e. linear. This is a major improvement over the basic solution considering that DNA strands can be about 3 billion base pairs long.

Results:
-	For problem sizes of upto 500, the basic and the efficient solutions grow at approximately the same rate in terms of time consumption and memory usage.
-	However, as problem size increases, the efficient solution grows much faster in runtime as compared to the basic solution. This can be attributed to the fact that the size and number of subproblems in the efficient solution increase with problem size.
-	Simultaneously, the efficient solution performs much better than the basic solution vis-à-vis memory usage due to the space complexity of the former being linear in input size while that of the latter is quadratic.
