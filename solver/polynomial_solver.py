import sympy as sp


def characteristic_polynomial(matrix):
    """
    Computes the characteristic polynomial of a square matrix.

    Characteristic polynomial:
        det(A - λI)

    Returns:
        polynomial, steps
    """

    steps = []

    # ----------------------------------------
    # Validate input
    # ----------------------------------------

    if not matrix or not matrix[0]:

        raise ValueError(
            "Matrix cannot be empty."
        )

    rows = len(matrix)
    cols = len(matrix[0])

    # Characteristic polynomial requires
    # a square matrix
    if rows != cols:

        raise ValueError(
            "Characteristic polynomial requires "
            "a square matrix."
        )

    # Make sure all rows have the same length
    for row in matrix:

        if len(row) != cols:

            raise ValueError(
                "All rows of the matrix "
                "must have the same length."
            )

    # ----------------------------------------
    # Create SymPy matrix
    # ----------------------------------------

    A = sp.Matrix(matrix)

    steps.append({
        "operation": "Original Matrix",
        "matrix": str(A)
    })

    # ----------------------------------------
    # Define lambda symbol
    # ----------------------------------------

    lam = sp.symbols("λ")

    steps.append({
        "operation": "Define λ",
        "expression": "λ"
    })

    # ----------------------------------------
    # Create identity matrix
    # ----------------------------------------

    I = sp.eye(rows)

    steps.append({
        "operation": "Identity Matrix I",
        "matrix": str(I)
    })

    # ----------------------------------------
    # Calculate A - λI
    # ----------------------------------------

    shifted_matrix = A - lam * I

    steps.append({
        "operation": "Calculate A - λI",
        "matrix": str(shifted_matrix)
    })

    # ----------------------------------------
    # Calculate determinant
    # ----------------------------------------

    determinant = shifted_matrix.det()

    steps.append({
        "operation": "Calculate det(A - λI)",
        "expression": str(determinant)
    })

    # ----------------------------------------
    # Expand polynomial
    # ----------------------------------------

    polynomial = sp.expand(determinant)

    steps.append({
        "operation": "Expand the determinant",
        "expression": str(polynomial)
    })

    # ----------------------------------------
    # Final result
    # ----------------------------------------

    steps.append({
        "operation": "Characteristic Polynomial",
        "polynomial": str(polynomial)
    })

    return polynomial, steps


# --------------------------------------------------
# Temporary Testing
# --------------------------------------------------

if __name__ == "__main__":

    print("========================================")
    print("      CHARACTERISTIC POLYNOMIAL TEST")
    print("========================================")

    # Example matrix
    matrix = [
        [2, 1],
        [1, 2]
    ]

    print("\nInput Matrix:")
    print(matrix)

    try:

        polynomial, steps = (
            characteristic_polynomial(matrix)
        )

        print("\nSteps:")
        print("----------------------------------------")

        for step in steps:

            print(step["operation"])

            if "matrix" in step:
                print(step["matrix"])

            if "expression" in step:
                print(
                    step["expression"]
                )

            if "polynomial" in step:
                print(
                    "Polynomial:",
                    step["polynomial"]
                )

            print()

        print("----------------------------------------")
        print("Final Characteristic Polynomial:")
        print(polynomial)

    except ValueError as e:

        print("Error:", e)