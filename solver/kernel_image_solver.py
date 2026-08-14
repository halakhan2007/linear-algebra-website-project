def _rref(matrix):
    """
    Converts a matrix to Reduced Row Echelon Form (RREF).

    Returns:
        rref_matrix, pivot_columns, steps
    """

    matrix = [row[:] for row in matrix]

    if not matrix or not matrix[0]:
        return [], [], []

    rows = len(matrix)
    cols = len(matrix[0])

    steps = []

    steps.append({
        "operation": "Initial Matrix",
        "matrix": [row[:] for row in matrix]
    })

    pivot_row = 0
    pivot_columns = []

    for pivot_col in range(cols):

        if pivot_row >= rows:
            break

        # ----------------------------------------
        # Find a non-zero pivot
        # ----------------------------------------

        pivot_found = None

        for row in range(pivot_row, rows):

            if abs(matrix[row][pivot_col]) > 1e-10:
                pivot_found = row
                break

        if pivot_found is None:
            continue

        # ----------------------------------------
        # Swap rows if necessary
        # ----------------------------------------

        if pivot_found != pivot_row:

            matrix[pivot_row], matrix[pivot_found] = (
                matrix[pivot_found],
                matrix[pivot_row]
            )

            steps.append({
                "operation":
                    f"Swap Row {pivot_row + 1} "
                    f"with Row {pivot_found + 1}",
                "matrix": [r[:] for r in matrix]
            })

        # ----------------------------------------
        # Make pivot equal to 1
        # ----------------------------------------

        pivot = matrix[pivot_row][pivot_col]

        if abs(pivot - 1) > 1e-10:

            for col in range(cols):

                matrix[pivot_row][col] /= pivot

            steps.append({
                "operation":
                    f"Divide Row {pivot_row + 1} "
                    f"by {pivot}",
                "matrix": [r[:] for r in matrix]
            })

        # ----------------------------------------
        # Eliminate entries above and below pivot
        # ----------------------------------------

        for row in range(rows):

            if row == pivot_row:
                continue

            if abs(matrix[row][pivot_col]) < 1e-10:
                continue

            multiplier = matrix[row][pivot_col]

            for col in range(cols):

                matrix[row][col] -= (
                    multiplier
                    * matrix[pivot_row][col]
                )

            steps.append({
                "operation":
                    f"R{row + 1} = R{row + 1} - "
                    f"({multiplier})R{pivot_row + 1}",
                "matrix": [r[:] for r in matrix]
            })

        pivot_columns.append(pivot_col)
        pivot_row += 1

    return matrix, pivot_columns, steps


def find_image(matrix):
    """
    Finds a basis and dimension for the image
    (column space) of a matrix.

    Returns:
        image_basis,
        dimension,
        pivot_columns,
        rref_matrix,
        steps
    """

    # ----------------------------------------
    # Validation
    # ----------------------------------------

    if not matrix or not matrix[0]:

        return [], 0, [], [], []

    cols = len(matrix[0])

    for row in matrix:

        if len(row) != cols:

            return [], 0, [], [], [{
                "operation":
                    "All rows must have the same length."
            }]

    # ----------------------------------------
    # Find pivot columns
    # ----------------------------------------

    rref_matrix, pivot_columns, steps = _rref(matrix)

    # ----------------------------------------
    # Image basis
    #
    # IMPORTANT:
    # We take the corresponding ORIGINAL
    # columns, not columns from the RREF.
    # ----------------------------------------

    image_basis = []

    for pivot_col in pivot_columns:

        column_vector = []

        for row in matrix:

            column_vector.append(
                row[pivot_col]
            )

        image_basis.append(column_vector)

    dimension = len(image_basis)

    # ----------------------------------------
    # Add final result to steps
    # ----------------------------------------

    steps.append({
        "operation": "Image / Column Space",
        "pivot_columns": [
            col + 1
            for col in pivot_columns
        ],
        "image_basis": image_basis,
        "dimension": dimension,
        "rref_matrix": [
            row[:] for row in rref_matrix
        ]
    })

    return (
        image_basis,
        dimension,
        pivot_columns,
        rref_matrix,
        steps
    )


def find_kernel(matrix):
    """
    Finds a basis and dimension for the kernel
    (null space) of a matrix.

    Returns:
        kernel_basis,
        dimension,
        free_columns,
        pivot_columns,
        rref_matrix,
        steps
    """

    # ----------------------------------------
    # Validation
    # ----------------------------------------

    if not matrix or not matrix[0]:

        return [], 0, [], [], [], []

    cols = len(matrix[0])

    for row in matrix:

        if len(row) != cols:

            return [], 0, [], [], [], [{
                "operation":
                    "All rows must have the same length."
            }]

    # ----------------------------------------
    # Convert to RREF
    # ----------------------------------------

    rref_matrix, pivot_columns, steps = _rref(matrix)

    # ----------------------------------------
    # Find free columns
    # ----------------------------------------

    free_columns = []

    for col in range(cols):

        if col not in pivot_columns:

            free_columns.append(col)

    kernel_basis = []

    # ----------------------------------------
    # Construct one kernel vector
    # for every free variable
    # ----------------------------------------

    for free_col in free_columns:

        solution = [0] * cols

        # Set the selected free variable = 1
        solution[free_col] = 1

        # Solve pivot variables
        for row in range(
            len(pivot_columns) - 1,
            -1,
            -1
        ):

            pivot_col = pivot_columns[row]

            value = 0

            for col in range(
                pivot_col + 1,
                cols
            ):

                value += (
                    rref_matrix[row][col]
                    * solution[col]
                )

            solution[pivot_col] = -value

        kernel_basis.append(solution)

        steps.append({
            "operation":
                f"Set free variable x{free_col + 1} = 1",
            "kernel_vector": solution[:]
        })

    dimension = len(kernel_basis)

    # ----------------------------------------
    # Final result
    # ----------------------------------------

    steps.append({
        "operation": "Kernel / Null Space",
        "pivot_columns": [
            col + 1
            for col in pivot_columns
        ],
        "free_columns": [
            col + 1
            for col in free_columns
        ],
        "kernel_basis": kernel_basis,
        "dimension": dimension,
        "rref_matrix": [
            row[:] for row in rref_matrix
        ]
    })

    return (
        kernel_basis,
        dimension,
        free_columns,
        pivot_columns,
        rref_matrix,
        steps
    )


# --------------------------------------------------
# Temporary Testing
# --------------------------------------------------

if __name__ == "__main__":

    print("========================================")
    print("        KERNEL / IMAGE TEST")
    print("========================================")

    # Matrix:
    #
    # [1  2  3]
    # [2  4  6]
    #
    # The second row is 2 times the first.
    #
    # Rank = 1
    # Nullity = 2
    #
    # Therefore:
    # Image dimension = 1
    # Kernel dimension = 2

    matrix = [
        [1, 2, 3],
        [2, 4, 6]
    ]

    print("\nOriginal Matrix:")
    print(matrix)

    # ----------------------------------------
    # IMAGE
    # ----------------------------------------

    (
        image_basis,
        image_dimension,
        pivot_columns,
        rref_matrix,
        image_steps
    ) = find_image(matrix)

    print("\n========================================")
    print("IMAGE / COLUMN SPACE")
    print("========================================")

    print("Pivot columns:")
    print([
        col + 1
        for col in pivot_columns
    ])

    print("Image basis:")
    print(image_basis)

    print("Image dimension:")
    print(image_dimension)

    print("\nSteps:")

    for step in image_steps:

        print(step["operation"])

        if "matrix" in step:
            print(step["matrix"])

    # ----------------------------------------
    # KERNEL
    # ----------------------------------------

    (
        kernel_basis,
        kernel_dimension,
        free_columns,
        pivot_columns,
        rref_matrix,
        kernel_steps
    ) = find_kernel(matrix)

    print("\n========================================")
    print("KERNEL / NULL SPACE")
    print("========================================")

    print("Pivot columns:")
    print([
        col + 1
        for col in pivot_columns
    ])

    print("Free columns:")
    print([
        col + 1
        for col in free_columns
    ])

    print("Kernel basis:")
    print(kernel_basis)

    print("Kernel dimension:")
    print(kernel_dimension)

    print("\nRREF:")
    print(rref_matrix)

    print("\nSteps:")

    for step in kernel_steps:

        print(step["operation"])

        if "matrix" in step:
            print(step["matrix"])

        if "kernel_vector" in step:
            print(
                "Kernel vector:",
                step["kernel_vector"]
            )