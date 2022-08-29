"""Compute homology groups of a simplicial complex."""

import algelinpy


def sublists(in_list):
    """return every sublist of a given list (empty list included)."""
    if len(in_list) == 0:
        return [[]]
    first = in_list[0]
    rec_lists = sublists(in_list[1:])
    return [[first] + x for x in rec_lists] + rec_lists

class SimplicialComplex():
    def __init__(self, name, complex):
        if SimplicialComplex._check(complex) is False:
            raise Exception("axioms doesn't hold for the informed complex.")
        self.name = name
        self.complex = complex
        self.dimension = len(max(self.complex, key=len)) - 1

    def __repr__(self):
        return f"Space: {self.name}\n\
Dimension: {self.dimension}\n\
Euler's characteristic: {self.euler_char()}\n\
Betti numbers: {self.homology()}\n"

    def _check(complex):
        """Checks if a complex satisfies axioms of simplicial complex.
        
        the axioms are:
        - lists should be ordered because this induces the correct orientation.
        - every face of a simplex should be in the complex.
        """
        freq = []
        if len(complex) == 0:
            return False
        for s in complex:
            if len(s) == 0 or all(isinstance(v, int) for v in s) is False:
                return False
            if all(s[i] < s[i+1] for i in range(len(s) - 1)) is False:
                raise ValueError(f"simplex {s} isn't ordered.")
            faces = sublists(s)
            faces.pop() # remove empty set/simplex
            for face in faces:
                if face not in complex:
                    return False
            if s in freq:
                raise Warning(f"simplex {s} repeated, computations won't work.")
            freq.append(s)
        return True

    def _n_simplexes(self, n):
        """return a list with the n-simplexes of the complex."""
        nsimps = []
        for simplex in self.complex:
            if len(simplex) == n+1:
                nsimps.append(simplex)
        return nsimps

    def euler_char(self):
        """compute the Euler's characteristic of the complex.

        recall: the Euler's characteristic is the alternating sum
        k_0 - k_1 + k_2 - k_3 + ...,
        being k_n the number of n-simplexes in the complex.
        this formula generalizes V - A + F = 2.
        """
        chi = 0
        for i in range(self.dimension + 1):
            chi += ((-1) ** i) * len(self._n_simplexes(i))
        return chi

    def _d_matrix(self, n):
        """return the matrix representation of the n-th boundary operator.

        recall: the boundary operator d_n:C_n(X) -> C_{n-1}(X) goes from the
        space of n-chains (ie, formal linear combinations of n-simplexes) to
        the space of (n-1)-chains.

        example: d_n([0, 1, 2]) := [1, 2] - [0, 2] + [0, 1]
        """
        C_n = self._n_simplexes(n)
        C_n_minus_1 = self._n_simplexes(n-1)
        d = [[0.0 for _ in range(len(C_n))] for _ in range(len(C_n_minus_1))]
        for dom in C_n:
            for k in range(len(dom)):
                aux = dom[:k] + dom[k+1:]
                if aux in C_n_minus_1:
                    i = C_n_minus_1.index(aux)
                    j = C_n.index(dom)
                    d[i][j] = (-1) ** k
        return d

    def _betti(self, n):
        """compute the n-th Betti number of the complex.

        recall: the n-th Betti number is the dimension of the n-th homology
        group and the homology group is defined as the quotient

        H_n := Z_n / B_n = ker(d_n) / im(d_{n+1}).

        since we want to compute dim(ker(d_n)) and dim(im(d_{n+1})), we have
        to do gaussian elimination in the matrix representation and count the
        number of pivots. recall that, by the rank-nullity theorem,
        
        dim(ker(d_n)) = dim(C_n) - dim(im(d_n)).

        we also know that dim(V/W) = dim(V) - dim(W), which gives the final
        answer setting V = Z_n and W = B_n.
        """
        d_n = self._d_matrix(n)
        d_n_plus_1 = self._d_matrix(n+1)

        algelinpy.gaussian_elimination(d_n)
        algelinpy.gaussian_elimination(d_n_plus_1)

        dim_dom = len(d_n_plus_1)
        dim_cycles = dim_dom - algelinpy.count_pivots(d_n)
        dim_boundaries = algelinpy.count_pivots(d_n_plus_1)

        return dim_cycles - dim_boundaries

    def homology(self):
        """return a list with the Betti numbers of the complex."""
        bettis = []
        for n in range(self.dimension + 1):
            bettis.append(self._betti(n))
        return bettis


point = [[0]]
point = SimplicialComplex("Point", point)
print(point)


two_points = [[0], [1]]
two_points = SimplicialComplex("Two points", two_points)
print(two_points)


seg = [[0,1], [0], [1]]
seg = SimplicialComplex("Line segment", seg)
print(seg)


circle = [[0,1], [0,2], [1,2], [0], [1], [2]]
circle = SimplicialComplex("Circle", circle)
print(circle)


circle_seg = [[0,1], [0,2], [1,2], [0], [1], [2], [3], [4], [3,4]]
circle_seg = SimplicialComplex("Circle + line segment", circle_seg)
print(circle_seg)


closed_disk = [[0,1,2], [0,1], [0,2], [1,2], [0], [1], [2]]
closed_disk = SimplicialComplex("Closed disk", closed_disk)
print(closed_disk)


tetrahedron_with_arm = [[0], [1], [2], [3], [4], [0,1], [0,3], [0,2], [0,4],
                        [1,2], [1,3], [2,3], [2,4], [0,1,2], [0,1,3], [0,2,3],
                        [1,2,3]]
tetrahedron_with_arm = SimplicialComplex("Tetrahedron with arm",
                                         tetrahedron_with_arm)
print(tetrahedron_with_arm)


tetrahedron = [[0,1,2], [0,1,3], [0,2,3], [1,2,3], [0,1], [0,2],
               [0,3], [1,2], [1,3], [2,3], [0], [1], [2], [3]]
tetrahedron = SimplicialComplex("Tetrahedron", tetrahedron)
print(tetrahedron)


octahedron = [[0,1,2], [0,1,4], [0,2,3], [0,3,4], [1,2,5], [1,4,5],
              [2,3,5], [3,4,5], [0,1], [0,2], [0,3], [0,4], [1,2],
              [1,4], [1,5], [2,3], [2,5], [3,4], [3,5], [4,5], [0], [1],
              [2], [3], [4], [5]]
octahedron = SimplicialComplex("Octahedron", octahedron)
print(octahedron)


torus = [[0], [1], [2], [3], [4], [5], [6], [7], [8], [0,1], [1,2], [0,2],
         [4,8], [7,8], [4,7], [3,5], [5,6], [3,6], [0,4], [3,4],
         [0,3], [1,8], [5,8], [1,5], [2,7], [6,7], [2,6], [0,8],
         [2,8], [0,7], [3,8], [5,7], [4,6], [0,5], [1,6], [0,6],
         [0,4,8], [0,1,8], [1,2,8], [2,7,8], [0,2,7], [0,4,7],
         [3,4,8], [3,5,8], [5,7,8], [5,6,7], [4,6,7], [3,4,6],
         [0,3,5], [0,1,5], [1,5,6], [1,2,6], [0,2,6], [0,3,6]]
torus = SimplicialComplex("Torus", torus)
print(torus)


projective_plane = [[0], [1], [2], [3], [4], [5], [0,1], [0,2], [0,3], [0,4],
                    [0,5], [1,2], [1,3], [1,4], [1,5], [2,3], [2,4], [2,5],
                    [3,4], [3,5], [4,5], [0,2,3], [0,3,4], [0,1,4], [0,1,5],
                    [0,2,5], [1,2,3], [1,3,5], [3,4,5], [2,4,5], [1,2,4]]
projective_plane = SimplicialComplex("Projective plane", projective_plane)
print(projective_plane)


mobius = [[0], [1], [2], [3], [4], [0,1], [0,2], [0,3], [0,4], [1,2], [1,3],
          [2,3], [2,4], [3,4], [0,1,3], [1,2,3], [2,3,4], [0,2,4]]
mobius = SimplicialComplex("Möbius strip", mobius)
print(mobius)


klein = [[0], [1], [2], [3], [4], [5], [6], [7], [8],
         [0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [0,7], [0,8],
         [1,2], [1,5], [1,6], [1,7], [1,8], [2,6], [2,8],
         [3,4], [3,5], [3,6], [3,8], [4,6], [4,7], [4,8],
         [5,6], [5,7], [5,8], [6,7], [7,8], [0,1,5], [0,3,5],
         [1,2,6], [1,5,6], [0,2,6], [0,3,6], [3,5,8], [3,4,8],
         [5,6,7], [5,7,8], [4,6,7], [3,4,6], [0,4,8], [0,2,8],
         [1,7,8], [1,2,8], [0,1,7], [0,4,7]]
klein = SimplicialComplex("Klein bottle", klein)
print(klein)


cylinder = [[0], [1], [2], [3], [4], [5], [0,1], [0,2], [0,3], [0,4], [0,5],
            [1,2], [1,4], [1,5], [2,5], [3,4], [3,5], [4,5], [0,3,4], [0,3,5],
            [0,1,4], [0,2,5], [1,2,5], [1,4,5]]
cylinder = SimplicialComplex("Cylinder", cylinder)
print(cylinder)
