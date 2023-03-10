from gmpy2 import mpz, is_even


def init_empty_cand_dict(n_cand, enc_zero):
    """each candidate initialized with 0 points"""
    cand_dict = {}
    for cand in range(n_cand):
        cand_dict[cand] = enc_zero

    return cand_dict


def if_then_else(cond, val_true, val_false):
    """
    A simple if then else branching.
    Inputs/Output:
    - cond (0 or 1, can be encrypted)
    - val_true (return if cond=1)
    - val_false (return if cond=0)
    """
    return cond * val_true + (1 - cond) * val_false


def ext_euclid(n, m):
    a_ = n
    b_ = m
    x_0 = 1
    y_0 = 0
    x_1 = 0
    y_1 = 1

    while b_ != 0:
        q = a_ // b_
        r = a_ % b_
        a_ = b_
        b_ = r
        x_0_ = x_0
        y_0_ = y_0
        x_0 = x_1
        y_0 = y_1
        x_1 = x_0_ - q * x_1
        y_1 = y_0_ - q * y_1

    result = m * y_0
    while result < 0:
        result += n*m
    return result


def eval_polynomial(coeffs, x, n):
    """
    this functions evals the polynomial 
    p(x) = coeffs[n-1]x^(n-1) + ... + 
    coeffs[1]x^1 + coeffs[0] mod n
    """
    y = 0
    for i, coeff in enumerate(coeffs):
        y += coeff * x ** i
        y %= n
    return y


def get_binary_representation(m, bits):
    """ Return the binary representation of m of length bits
    This function adds leading zeros if necessary and will 
    cut leading bits if m > 2**bits """
    bin_m = bin(m)[2:].zfill(bits)
    return [int(i) for i in bin_m]


def minus1to(k):
    if is_even(k):
        return 1
    return -1


def calc_lambda(shares, own_index, delta):
    """calculates lambda used for interpolation"""
    y = mpz(delta)
    for share in shares:
        if share[0] != own_index:
            y *= -share[0]
            y /= (own_index - share[0])
    return mpz(y)


def get_class_from_name(class_name: str, classes):
    """
    Return the class with the given name from the list of possible classes.

    Args:
        class_name (str): The name of the class which is to be returned.
        classes (List[type]): The list of valid classes which is scanned
                              for a class with the same name as class_name.

    Raises:
        ValueError: If no class is found with the given class name.

    Returns:
        type: The class from the given classes which has the same name as class_name.
    """
    if classes is None:
        classes = []
    found_class = next((c for c in classes if class_name == c.__name__), None)
    if found_class is None:
        raise ValueError(f"'{class_name}' is not an option from classes {classes}")
    return found_class


def subclasses_recursive(root_class) -> frozenset:
    """
    Return a set of all loaded subclasses of the given root class.

    Args:
        root_class (type): The class whose subclasses are to be found.

    Returns:
        frozenset: A set containing all of the subclasses of the given class.
    """
    return frozenset(root_class.__subclasses__()).union(
        s for c in root_class.__subclasses__()
          for s in subclasses_recursive(c))
