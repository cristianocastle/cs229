import math

""" ----------------- PROBLEM 1 ----------------- """


def translate(S, z0):
    """
    translates the complex numbers of set S by z0
    :param S: set type; a set of complex numbers
    :param z0: complex type; a complex number
    :return: set type; a set consisting of points in S translated by z0
    """
    # Translate each complex number in S by z0 and return a new set
    return {z + z0 for z in S}


""" ----------------- PROBLEM 2 ----------------- """


def scale(S, k):
    """
    scales the complex numbers of set S by k.
    :param S: set type; a set of complex numbers
    :param k: float type; positive real number
    :return: set type; a set consisting of points in S scaled by k
    :raise: raises ValueError if k <= 0
    """
    # Validate scale factor
    if k <= 0:
        raise ValueError("Scale factor k must be positive.")
    # Scale each complex number in S by k
    return {k * z for z in S}


""" ----------------- PROBLEM 3 ----------------- """


def rotate(S, tau):
    """
    rotates the complex numbers of set S by tau radians.  
    :param S: set type; - set of complex numbers
    :param tau: float type; radian measure of the rotation value. 
                If negative, the rotation is clockwise.  
                If positive the rotation is counterclockwise. 
                If zero, no rotation.
    :returns: set type; a set consisting of points in S rotated by tau radians
    """
    # Rotate each complex number in S by tau radians about the origin
    # Multiply by e^{i tau} = cos(tau) + i sin(tau)
    rot = math.cos(tau) + 1j * math.sin(tau)
    return {z * rot for z in S}


""" ----------------- PROBLEM 4 ----------------- """


class Vec:
    def __init__(self, contents=[]):
        """
        Constructor defaults to empty vector
        :param contents: list type; list of elements to initialize a vector object, defaults to empty list
        """
        self.elements = contents
        return

    def __abs__(self):
        """
        Overloads the built-in function abs(v)
        :returns: float type; the Euclidean norm of vector v
        """
        return math.sqrt(sum(x * x for x in self.elements))

    def __add__(self, other):
        """
        overloads the + operator to support Vec + Vec
        :raises: ValueError if vectors are not same length
        :returns: Vec type; a Vec object that is the sum vector of this Vec and 'other' Vec
        """
        if len(self.elements) != len(other.elements):
            raise ValueError("Vectors must be the same length for addition.")
        return Vec([x + y for x, y in zip(self.elements, other.elements)])

    def __sub__(self, other):
        """
        overloads the - operator to support Vec - Vec
        :raises: ValueError if vectors are not same length
        :returns: Vec type; a Vec object that is the difference vector of this Vec and 'other' Vec
        """
        if len(self.elements) != len(other.elements):
            raise ValueError("Vectors must be the same length for subtraction.")
        return Vec([x - y for x, y in zip(self.elements, other.elements)])

    def __mul__(self, other):
        """
        Overloads the * operator to support
          - Vec * Vec (dot product) raises ValueError if vectors are not
            same length in the case of dot product; returns scalar
          - Vec * float (component-wise product); returns Vec object
          - Vec * int (component-wise product); returns Vec object
        """
        if type(other) == Vec:  # define dot product
            if len(self.elements) != len(other.elements):
                raise ValueError("Vectors must be the same length for dot product.")
            return sum(x * y for x, y in zip(self.elements, other.elements))

        elif type(other) == float or type(other) == int:  # scalar-vector multiplication
            return Vec([other * x for x in self.elements])

    def __rmul__(self, other):
        """
        Overloads the * operation to support
              - float * Vec; returns Vec object
              - int * Vec; returns Vec object
        """
        if isinstance(other, (int, float)):
            return Vec([other * x for x in self.elements])
        return NotImplemented

    def __str__(self):
        """returns string representation of this Vec object"""
        return str(self.elements)  # does NOT need further implementation
