def span_basis_dimension(matrix):
    """
    Finds the span, basis, and dimension of a set of vectors.

    Vectors are represented as rows.

    Returns:
        span
        basis
        dimension
        basis_indices
        steps
    """

    # ----------------------------------------
    # Input validation
    # ----------------------------------------

    if not matrix or not matrix[0]:

        return (
            "Invalid Input",
            [],
            0,
            [],
            []
        )

    rows = len(matrix)
    cols = len(matrix[0])

    # Make sure every vector has the same dimension
    for row in matrix:

        if len(row) != cols:

            return (
                "Invalid Input",
                [],
                0,
                [],
                [{
                    "operation":
                        "All vectors must have the same dimension."
                }]
            )

    # ----------------------------------------
    # Create working copy
    # ----------------------------------------

    working_matrix = [
        row[:] for row in matrix
    ]

    # Keep track of which original vector
    # is currently in each row
    original_indices = list(range(rows))

    steps = []

    steps.append({
        "operation": "Initial Matrix",
        "matrix": [
            row[:] for row in working_matrix
        ]
    })

    pivot_row = 0
    pivot_indices = []

    # ----------------------------------------
    # Gaussian elimination
    # ----------------------------------------

    for pivot_col in range(cols):

        if pivot_row >= rows:
            break

        pivot_found = None

        # Search for a non-zero pivot
        for row in range(pivot_row, rows):

            if abs(working_matrix[row][pivot_col]) > 1e-10:

                pivot_found = row
                break

        # No pivot in this column
        if pivot_found is None:
            continue

        # ------------------------------------
        # Row swap
        # ------------------------------------

        if pivot_found != pivot_row:

            working_matrix[pivot_row], working_matrix[pivot_found] = (
                working_matrix[pivot_found],
                working_matrix[pivot_row]
            )

            original_indices[pivot_row], original_indices[pivot_found] = (
                original_indices[pivot_found],
                original_indices[pivot_row]
            )

            steps.append({
                "operation":
                    f"Swap Row {pivot_row + 1} "
                    f"with Row {pivot_found + 1}",
                "matrix": [
                    row[:] for row in working_matrix
                ]
            })

        # ------------------------------------
        # Record the original vector
        # corresponding to this pivot
        # ------------------------------------

        pivot_indices.append(
            original_indices[pivot_row]
        )

        pivot = working_matrix[pivot_row][pivot_col]

        # ------------------------------------
        # Eliminate entries below pivot
        # ------------------------------------

        for row in range(pivot_row + 1, rows):

            if abs(working_matrix[row][pivot_col]) < 1e-10:
                continue

            multiplier = (
                working_matrix[row][pivot_col]
                / pivot
            )

            for col in range(pivot_col, cols):

                working_matrix[row][col] -= (
                    multiplier
                    * working_matrix[pivot_row][col]
                )

            steps.append({
                "operation":
                    f"R{row + 1} = R{row + 1} - "
                    f"({multiplier})R{pivot_row + 1}",
                "matrix": [
                    row[:] for row in working_matrix
                ]
            })

        pivot_row += 1

    # ----------------------------------------
    # Basis vectors
    # ----------------------------------------

    basis = []

    for index in pivot_indices:

        basis.append(
            matrix[index][:]
        )

    # ----------------------------------------
    # Dimension
    # ----------------------------------------

    dimension = len(pivot_indices)

    # ----------------------------------------
    # Span
    # ----------------------------------------

    if dimension == cols:

        span = f"R^{cols}"

    else:

        span = (
            f"{dimension}-dimensional subspace "
            f"of R^{cols}"
        )

    # ----------------------------------------
    # Add final result to steps
    # ----------------------------------------

    steps.append({
        "operation": "Span, Basis and Dimension",
        "span": span,
        "basis": basis,
        "dimension": dimension,
        "basis_indices": [
            index + 1
            for index in pivot_indices
        ],
        "matrix": [
            row[:] for row in working_matrix
        ]
    })

    return (
        span,
        basis,
        dimension,
        pivot_indices,
        steps
    )


# --------------------------------------------------
# Temporary Testing
# --------------------------------------------------

if __name__ == "__main__":

    print("========================================")
    print("     SPAN / BASIS / DIMENSION TEST")
    print("========================================")

    # ----------------------------------------
    # Test 1: Two independent vectors in R2
    # ----------------------------------------

    matrix1 = [
        [1, 0],
        [0, 1]
    ]

    (
        span,
        basis,
        dimension,
        basis_indices,
        steps
    ) = span_basis_dimension(matrix1)

    print("\nTEST 1")
    print("----------------------------------------")

    print("Span:", span)
    print("Basis:", basis)
    print("Dimension:", dimension)

    print(
        "Basis vectors:",
        [
            index + 1
            for index in basis_indices
        ]
    )

    print("\nSteps:")

    for step in steps:

        print(step["operation"])

        if "matrix" in step:
            print(step["matrix"])

    # ----------------------------------------
    # Test 2: Three vectors, one dependent
    # ----------------------------------------

    matrix2 = [
        [1, 0],
        [0, 1],
        [1, 1]
    ]

    (
        span,
        basis,
        dimension,
        basis_indices,
        steps
    ) = span_basis_dimension(matrix2)

    print("\n\nTEST 2")
    print("----------------------------------------")

    print("Span:", span)
    print("Basis:", basis)
    print("Dimension:", dimension)

    print(
        "Basis vectors:",
        [
            index + 1
            for index in basis_indices
        ]
    )

    print("\nSteps:")

    for step in steps:

        print(step["operation"])

        if "matrix" in step:
            print(step["matrix"])

    # ----------------------------------------
    # Test 3: Three independent vectors in R3
    # ----------------------------------------

    matrix3 = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

    (
        span,
        basis,
        dimension,
        basis_indices,
        steps
    ) = span_basis_dimension(matrix3)

    print("\n\nTEST 3")
    print("----------------------------------------")

    print("Span:", span)
    print("Basis:", basis)
    print("Dimension:", dimension)

    print(
        "Basis vectors:",
        [
            index + 1
            for index in basis_indices
        ]
    )

    print("\nSteps:")

    for step in steps:

        print(step["operation"])

        if "matrix" in step:
            print(step["matrix"])