from Vec import Vec

"""-------------------- PROBLEM 1 --------------------"""
class Matrix:

    def __init__(self, rows):
        """
        initializes a Matrix with given rows
        :param rows: the list of rows that this Matrix object has
        """
        self.rows = rows
        self.cols = []
        self._construct_cols()
        return

    """
  INSERT MISSING SETTERS AND GETTERS HERE
  """
    def set_row(self, i, new_row):
        # i is 1-based
        m, n = self.dim()
        if i < 1 or i > m:
            raise IndexError("Row index out of range")
        if len(new_row) != n:
            raise ValueError("Incompatible row length.")
        self.rows[i-1] = list(new_row)
        self._construct_cols()

    def set_col(self, j, new_col):
        # j is 1-based
        m, n = self.dim()
        if j < 1 or j > n:
            raise IndexError("Column index out of range")
        if len(new_col) != m:
            raise ValueError("Incompatible column length.")
        self.cols[j-1] = list(new_col)
        self._construct_rows()

    def set_entry(self, i, j, val):
        m, n = self.dim()
        if i < 1 or i > m or j < 1 or j > n:
            raise IndexError("Index out of range")
        self.rows[i-1][j-1] = val
        self.cols[j-1][i-1] = val

    def get_row(self, i):
        m, n = self.dim()
        if i < 1 or i > m:
            raise IndexError("Row index out of range")
        return self.rows[i-1]

    def get_col(self, j):
        m, n = self.dim()
        if j < 1 or j > n:
            raise IndexError("Column index out of range")
        return self.cols[j-1]

    def get_entry(self, i, j):
        m, n = self.dim()
        if i < 1 or i > m or j < 1 or j > n:
            raise IndexError("Index out of range")
        return self.rows[i-1][j-1]

    def get_columns(self):
        return self.cols

    def get_rows(self):
        return self.rows

    def get_diag(self, k):
        # k can be negative or positive or zero
        m = len(self.rows)
        n = len(self.cols)
        diag = []
        if k >= 0:
            i = 0
            j = k
        else:
            i = -k
            j = 0
        while i < m and j < n:
            diag.append(self.rows[i][j])
            i += 1
            j += 1
        return diag

    def _construct_cols(self):
        """
        HELPER METHOD: Resets the columns according to the existing rows
        """
        self.cols = []
        if not self.rows:
            return
        ncols = len(self.rows[0])
        # build each column as list of entries from each row
        for j in range(ncols):
            col = [self.rows[i][j] for i in range(len(self.rows))]
            self.cols.append(col)
        return

    def _construct_rows(self):
        """
        HELPER METHOD: Resets the rows according to the existing columns
        """
        self.rows = []
        if not self.cols:
            return
        nrows = len(self.cols[0])
        ncols = len(self.cols)
        for i in range(nrows):
            row = [self.cols[j][i] for j in range(ncols)]
            self.rows.append(row)
        return

    def __add__(self, other):
        """
        overloads the + operator to support Matrix + Matrix
        :param other: the other Matrix object
        :raises: ValueError if the Matrix objects have mismatching dimensions
        :raises: TypeError if other is not of Matrix type
        :return: Matrix type; the Matrix object resulting from the Matrix + Matrix operation
        """
        if type(other) != Matrix:
            raise TypeError("Can only add Matrix to Matrix")
        m1, n1 = self.dim()
        m2, n2 = other.dim()
        if (m1, n1) != (m2, n2):
            raise ValueError("Matrix dimensions must agree for addition")
        new_rows = [[self.rows[i][j] + other.rows[i][j] for j in range(n1)] for i in range(m1)]
        return Matrix(new_rows)

    def __sub__(self, other):
        """
        overloads the - operator to support Matrix - Matrix
        :param other:
        :raises: ValueError if the Matrix objects have mismatching dimensions
        :raises: TypeError if other is not of Matrix type
        :return: Matrix type; the Matrix object resulting from Matrix - Matrix operation
        """
        if type(other) != Matrix:
            raise TypeError("Can only subtract Matrix from Matrix")
        m1, n1 = self.dim()
        m2, n2 = other.dim()
        if (m1, n1) != (m2, n2):
            raise ValueError("Matrix dimensions must agree for subtraction")
        new_rows = [[self.rows[i][j] - other.rows[i][j] for j in range(n1)] for i in range(m1)]
        return Matrix(new_rows)

    def __mul__(self, other):
        """
        overloads the * operator to support
            - Matrix * Matrix
            - Matrix * Vec
            - Matrix * float
            - Matrix * int
        :param other: the other Matrix object
        :raises: ValueError if the Matrix objects have mismatching dimensions
        :raises: TypeError if other is not of Matrix type
        :return: Matrix type; the Matrix object resulting from the Matrix + Matrix operation
        """
        if type(other) == float or type(other) == int:
            # scalar multiplication: multiply every entry
            m, n = self.dim()
            new_rows = [[self.rows[i][j] * other for j in range(n)] for i in range(m)]
            return Matrix(new_rows)
        elif type(other) == Matrix:
            # matrix multiplication: (m x n) * (n x p) -> (m x p)
            m, n = self.dim()
            m2, p = other.dim()
            if n != m2:
                raise ValueError("Matrix dimensions are not aligned for multiplication")
            # compute result rows
            result_rows = []
            for i in range(m):
                row = []
                for j in range(p):
                    s = 0
                    for t in range(n):
                        s += self.rows[i][t] * other.rows[t][j]
                    row.append(s)
                result_rows.append(row)
            return Matrix(result_rows)
        elif type(other) == Vec:
            # Matrix * Vec -> Vec of length m where m = number of rows
            m, n = self.dim()
            if len(other) != n:
                raise ValueError("Vector length does not match matrix columns")
            res = []
            for i in range(m):
                s = 0
                for j in range(n):
                    s += self.rows[i][j] * other.elements[j]
                res.append(s)
            return Vec(res)
        else:
            raise TypeError(f"Matrix * {type(other)} is not supported.")
        return

    def __rmul__(self, other):
        """
        overloads the * operator to support
            - float * Matrix
            - int * Matrix
        :param other: the other Matrix object
        :raises: ValueError if the Matrix objects have mismatching dimensions
        :raises: TypeError if other is not of Matrix type
        :return: Matrix type; the Matrix object resulting from the Matrix + Matrix operation
        """
        if type(other) == float or type(other) == int:
            # scalar * Matrix
            m, n = self.dim()
            new_rows = [[other * self.rows[i][j] for j in range(n)] for i in range(m)]
            return Matrix(new_rows)
        else:
            raise TypeError(f"{type(other)} * Matrix is not supported.")
        return

    '''-------- ALL METHODS BELOW THIS LINE ARE FULLY IMPLEMENTED -------'''

    def dim(self):
        """
        gets the dimensions of the mxn matrix
        where m = number of rows, n = number of columns
        :return: tuple type; (m, n)
        """
        m = len(self.rows)
        n = len(self.cols)
        return (m, n)

    def __str__(self):
        """prints the rows and columns in matrix form """
        mat_str = ""
        for row in self.rows:
            mat_str += str(row) + "\n"
        return mat_str

    def __eq__(self, other):
        """
        overloads the == operator to return True if
        two Matrix objects have the same row space and column space
        """
        if type(other) != Matrix:
            return False
        this_rows = [round(x, 3) for x in self.rows]
        other_rows = [round(x, 3) for x in other.rows]
        this_cols = [round(x, 3) for x in self.cols]
        other_cols = [round(x, 3) for x in other.cols]

        return this_rows == other_rows and this_cols == other_cols

    def __req__(self, other):
        """
        overloads the == operator to return True if
        two Matrix objects have the same row space and column space
        """
        if type(other) != Matrix:
            return False
        this_rows = [round(x, 3) for x in self.rows]
        other_rows = [round(x, 3) for x in other.rows]
        this_cols = [round(x, 3) for x in self.cols]
        other_cols = [round(x, 3) for x in other.cols]

        return this_rows == other_rows and this_cols == other_cols


"""-------------------- PROBLEM 2 --------------------"""


def rotate_2Dvec(v: Vec, tau: float):
    """
    computes the 2D-vector that results from rotating the given vector
    by the given number of radians
    :param v: Vec type; the vector to rotate
    :param tau: float type; the radians to rotate by
    :return: Vec type; the rotated vector
    """
    if len(v) != 2:
        raise ValueError(f"rotate_2Dvec is not defined for {len(v)} -D vectors.")
    import math
    c = math.cos(tau)
    s = math.sin(tau)
    x = v.elements[0]
    y = v.elements[1]
    rx = c * x - s * y
    ry = s * x + c * y
    return Vec([rx, ry])
