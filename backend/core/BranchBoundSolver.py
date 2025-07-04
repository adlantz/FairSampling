# mosek.com
#
# The Branch-and-Bound algorithm
# for binary quadratic problems
# with Q=Q^T
#
# min x^TQx + Px + R
#
# x in {0,1}
#
# See the accompanying notebook for description and comments

from mosek.fusion import *
import mosek.fusion.pythonic
import numpy as np
import heapq
import string


# SDP relaxation
# min QX + Px + R
# st  Z = [X, x; x^T, 1] >> 0
def fusionSDP(Q, P, R):
    n = len(P)
    M = Model("fusionSDP")
    M.setSolverParam("numThreads", 1)  # For benchmarking
    Z = M.variable("Z", Domain.inPSDCone(n + 1))
    X = Z[0:n, 0:n]
    x = Z[0:n, n]
    M.constraint(X.diag() == x)
    M.constraint(Z[n, n] == 1)

    M.objective(
        ObjectiveSense.Minimize, Expr.constTerm(R) + Expr.dot(P, x) + Expr.dot(Q, X)
    )

    return M, x


# Branch and bound class
class BB:
    # Initialization
    def __init__(self, Q, P, R, relaxation=fusionSDP, verbose=True):
        # Problem data
        self.Q = Q
        self.Q0 = np.copy(Q)
        self.P = P
        self.P0 = np.copy(P)
        self.R = R
        self.R0 = np.copy(R)
        self.n = len(P)
        self.relaxation = relaxation
        # Global branch and bound data: current best solution and queue of nodes
        self.xx = np.zeros(self.n, dtype=int)
        self.active = []
        self.optimal_solutions = set()
        # Tolerances
        self.gaptol = 1e-6
        # Objective bounds
        self.lb = -1.0e10
        self.ub = 1.0e10
        # Statistics
        self.relSolved = 0
        self.optTime = 0.0
        self.intpntIter = 0
        # Other
        self.verbose = verbose

    # potentially add another function that passes in a complete state and returns the energy of that configurations
    def energy(self, state):
        return state.dot(self.Q0).dot(state) + self.P0.dot(state) + self.R0

    # Initiate solving the problem
    def solve(self):
        #         self.header()
        # Mapping from indices in current subproblem to [0..n)
        idxmap = np.arange(self.n, dtype=int)
        # Currently constructed solution
        curr = np.zeros(self.n, dtype=int)
        # Solve the root node
        obj, pivot = self.solveRelaxation(self.Q, self.P, self.R, curr, idxmap)
        heapq.heappush(
            self.active, (obj, 1, self.Q, self.P, self.R, curr, idxmap, pivot)
        )
        self.solveBB()
        #         self.stats()
        return self.optimal_solutions

    # Find index i where x[i] is closest to 0.5
    def pivot(self, x):
        return np.argmax(np.absolute(x - np.around(x)))

    #         return random.randint(0, self.n-1)

    # Printing out running statistics
    def header(self):
        if self.verbose:
            print(
                "{0: >10} {1: >10} {2: >15} {3: >15}".format(
                    "SELF.XX", "ACTIVE_NDS", "SELF.LB", "SELF.UB"
                )
            )

    def stats(self):
        if self.verbose:
            print(
                "{0: >10} {1: >10} {2: >15} {3: >15}".format(
                    (str(self.xx)), len(self.active), self.lb, self.ub
                )
            )

    def summary(self, verbose=False):
        if self.verbose or verbose:
            print("val = {0}".format(self.ub))
            print("sol = {0}".format(self.xx))
            print("optimal solutions = {0}".format(self.optimal_solutions))
            print("relaxations   = {0}".format(self.relSolved))
            print("intpntIter    = {0}".format(self.intpntIter))
            print("optimizerTime = {0}".format(self.optTime))

    # Check if we have a better solution and update
    def updateSol(self, obj, curr, idxmap, sol):
        if obj < self.ub:
            self.ub = obj
            for i in range(len(idxmap)):
                curr[idxmap[i]] = sol[i]
            np.copyto(self.xx, curr)
            self.optimal_solutions = set()
            self.optimal_solutions.add(str(curr))
        #             self.stats()
        elif obj == self.ub:
            for i in range(len(idxmap)):
                curr[idxmap[i]] = sol[i]
            self.optimal_solutions.add(str(curr))

    # Solve a single node.
    def solveRelaxation(self, Q, P, R, curr, idxmap):
        # Construct and solve model
        M, x = self.relaxation(Q, P, R)
        M.solve()
        # Obtain solution
        xx, relObj = x.level(), M.primalObjValue()
        # Update statistics
        self.optTime += M.getSolverDoubleInfo("optimizerTime")
        self.intpntIter += M.getSolverIntInfo("intpntIter")
        self.relSolved += 1
        M.dispose()
        # Round to nearest integers and try
        # to update the best solution
        xRnd = np.rint(xx).astype(int)
        objRnd = xRnd.dot(Q).dot(xRnd) + P.dot(xRnd) + R
        self.updateSol(objRnd, curr, idxmap, xRnd)
        # Return the objective bound and pivot
        return relObj, self.pivot(xx)

    # The node-processing loop
    def solveBB(self):
        while self.active:

            obj, _, Q, P, R, curr, idxmap, pivot = heapq.heappop(self.active)

            self.lb = obj

            # Optimality is proved

            if self.lb >= self.ub + self.gaptol:
                self.active = []
                return

            #             self.stats()

            if len(P) <= 1:
                pidx = idxmap[pivot]
                curr0 = np.copy(curr)

                val = 0
                if curr0[pidx] == 1:
                    val = 0
                    curr0[pidx] = 0
                elif curr0[pidx] == 0:
                    val = 1
                    curr0[pidx] = 1
                energy = self.energy(curr0)
                if energy == self.ub:
                    self.optimal_solutions.add(str(curr0))

                continue

            pidx = idxmap[pivot]

            # Construct and solve relaxations of two child nodes
            # where the pivot variable is assigned 0 or 1
            for val in [0, 1]:
                idxmap0 = np.delete(idxmap, pivot)
                curr0 = np.copy(curr)
                curr0[pidx] = val
                QT = np.delete(Q, pivot, axis=0)
                Q0 = np.delete(QT, pivot, axis=1)
                QZ = QT[:, pivot]
                PT = np.delete(P, pivot)
                P0 = PT + 2 * val * QZ
                R0 = val * Q[pivot, pivot] + val * P[pivot] + R

                obj0, pivot0 = self.solveRelaxation(Q0, P0, R0, curr0, idxmap0)

                heapq.heappush(
                    self.active,
                    (obj0, self.relSolved, Q0, P0, R0, curr0, idxmap0, pivot0),
                )

    def binary_to_decimal(self, array):
        """
        Converts an array of spins to its corresponding decimal value
        """
        array = array.translate(str.maketrans("", "", string.punctuation))
        array = array.replace(" ", "")

        binary = int(array, 2)

        return binary

    def get_ground_states(self):
        bm = self.solve()
        return [self.binary_to_decimal(b) for b in bm]
