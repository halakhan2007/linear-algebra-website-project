def gaussian_elimination(matrix):
    """
    Converts an augmented matrix to row-echelon form
    using Gaussian elimination.

    Returns:
        final_matrix, steps
    """

    matrix = [row[:] for row in matrix]

    rows = len(matrix)
    cols = len(matrix[0])
    steps = []

    steps.append({
        "operation": "Initial Matrix",
        "matrix": [row[:] for row in matrix]
    })

    pivot_row = 0

    for pivot_col in range(cols - 1):

        if pivot_row >= rows:
            break

        pivot_found = None

        # Find a non-zero pivot
        for row in range(pivot_row, rows):

            if matrix[row][pivot_col] != 0:
                pivot_found = row
                break

        # No pivot in this column
        if pivot_found is None:
            continue

        # Swap rows if necessary
        if pivot_found != pivot_row:

            matrix[pivot_row], matrix[pivot_found] = (
                matrix[pivot_found],
                matrix[pivot_row]
            )

            steps.append({
                "operation":
                    f"Swap Row {pivot_row + 1} "
                    f"with Row {pivot_found + 1}",
                "matrix": [row[:] for row in matrix]
            })

        pivot = matrix[pivot_row][pivot_col]

        # Eliminate entries below the pivot
        for row in range(pivot_row + 1, rows):

            if matrix[row][pivot_col] == 0:
                continue

            multiplier = (
                matrix[row][pivot_col] / pivot
            )

            for col in range(pivot_col, cols):

                matrix[row][col] -= (
                    multiplier * matrix[pivot_row][col]
                )

            steps.append({
                "operation":
                    f"R{row + 1} = R{row + 1} - "
                    f"({multiplier})R{pivot_row + 1}",
                "matrix": [r[:] for r in matrix]
            })

        pivot_row += 1

    return matrix, steps


def back_substitution(matrix):
    """
    Solves an upper-triangular augmented matrix
    using back-substitution.

    Returns:
        solution, steps
    """

    matrix = [row[:] for row in matrix]

    rows = len(matrix)
    cols = len(matrix[0])

    variables = cols - 1

    solution = [0] * variables
    steps = []

    steps.append({
        "operation": "Starting Back Substitution",
        "matrix": [row[:] for row in matrix]
    })

    # Check for inconsistent rows and
    # determine whether the system has enough pivots
    pivot_columns = []

    for row in range(rows):

        pivot_col = None

        for col in range(variables):

            if matrix[row][col] != 0:
                pivot_col = col
                break

        if pivot_col is None:

            # 0 = non-zero
            if matrix[row][-1] != 0:

                steps.append({
                    "operation":
                        "No solution: inconsistent system.",
                    "matrix": [r[:] for r in matrix]
                })

                return None, "no_solution", steps

        else:

            pivot_columns.append(pivot_col)

    # If fewer pivots than variables,
    # there are free variables
    if len(pivot_columns) < variables:

        steps.append({
            "operation":
                "Infinitely many solutions: "
                "free variable(s) detected.",
            "matrix": [r[:] for r in matrix]
        })

        return None, "infinite_solutions", steps

    # Perform back substitution
    for row in range(rows - 1, -1, -1):

        pivot_col = None

        for col in range(variables):

            if matrix[row][col] != 0:
                pivot_col = col
                break

        if pivot_col is None:
            continue

        pivot = matrix[row][pivot_col]

        known_value = matrix[row][-1]

        # Subtract already-known variable terms
        for col in range(pivot_col + 1, variables):

            known_value -= (
                matrix[row][col] * solution[col]
            )

        if pivot == 0:

            steps.append({
                "operation":
                    "Cannot divide by zero during "
                    "back substitution.",
                "matrix": [r[:] for r in matrix]
            })

            return None, "error", steps

        solution[pivot_col] = known_value / pivot

        steps.append({
            "operation":
                f"Find x{pivot_col + 1} = "
                f"{solution[pivot_col]}",
            "matrix": [r[:] for r in matrix]
        })

    steps.append({
        "operation": "Final Solution",
        "solution": solution
    })

    return solution, "unique_solution", steps


def solve_by_gaussian_elimination(matrix):
    """
    Solves an augmented system using:
    1. Gaussian elimination
    2. Back-substitution

    Returns:
        solution,
        elimination_steps,
        substitution_steps,
        status
    """

    final_matrix, elimination_steps = gaussian_elimination(matrix)

    solution, status, substitution_steps = (
        back_substitution(final_matrix)
    )

    return (
        solution,
        elimination_steps,
        substitution_steps,
        status
    )


def gauss_jordan(matrix):
    """
    Converts an augmented matrix to
    reduced row-echelon form.

    Returns:
        final_matrix, steps
    """

    matrix = [row[:] for row in matrix]

    rows = len(matrix)
    cols = len(matrix[0])

    steps = []

    steps.append({
        "operation": "Initial Matrix",
        "matrix": [row[:] for row in matrix]
    })

    pivot_row = 0

    for pivot_col in range(cols - 1):

        if pivot_row >= rows:
            break

        pivot_found = None

        # Find a non-zero pivot
        for row in range(pivot_row, rows):

            if matrix[row][pivot_col] != 0:
                pivot_found = row
                break

        if pivot_found is None:
            continue

        # Swap rows if necessary
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

        # Make pivot equal to 1
        pivot = matrix[pivot_row][pivot_col]

        if pivot != 1:

            for col in range(cols):

                matrix[pivot_row][col] /= pivot

            steps.append({
                "operation":
                    f"Divide Row {pivot_row + 1} "
                    f"by {pivot}",
                "matrix": [r[:] for r in matrix]
            })

        # Make every other element in
        # the pivot column equal to zero
        for row in range(rows):

            if row == pivot_row:
                continue

            if matrix[row][pivot_col] == 0:
                continue

            multiplier = matrix[row][pivot_col]

            for col in range(cols):

                matrix[row][col] -= (
                    multiplier * matrix[pivot_row][col]
                )

            steps.append({
                "operation":
                    f"R{row + 1} = R{row + 1} - "
                    f"({multiplier})R{pivot_row + 1}",
                "matrix": [r[:] for r in matrix]
            })

        pivot_row += 1

    return matrix, steps


def extract_solution_from_rref(matrix):
    """
    Extracts the solution from an RREF augmented matrix.

    Returns:
        solution, status, steps
    """

    matrix = [row[:] for row in matrix]

    rows = len(matrix)
    cols = len(matrix[0])

    variables = cols - 1

    solution = [0] * variables

    pivot_columns = []
    steps = []

    # Check for inconsistency
    for row in range(rows):

        all_zero = True

        for col in range(variables):

            if matrix[row][col] != 0:

                all_zero = False
                break

        if all_zero and matrix[row][-1] != 0:

            steps.append({
                "operation":
                    "No solution: inconsistent system.",
                "matrix": [r[:] for r in matrix]
            })

            return None, "no_solution", steps

    # Find pivot columns
    for row in range(rows):

        pivot_col = None

        for col in range(variables):

            if matrix[row][col] != 0:

                pivot_col = col
                break

        if pivot_col is not None:

            pivot_columns.append(pivot_col)

    # Check for free variables
    if len(pivot_columns) < variables:

        steps.append({
            "operation":
                "Infinitely many solutions: "
                "free variable(s) detected.",
            "matrix": [r[:] for r in matrix]
        })

        return None, "infinite_solutions", steps

    # Extract solution from RREF
    for row in range(rows):

        pivot_col = None

        for col in range(variables):

            if matrix[row][col] != 0:

                pivot_col = col
                break

        if pivot_col is not None:

            solution[pivot_col] = matrix[row][-1]

            steps.append({
                "operation":
                    f"x{pivot_col + 1} = "
                    f"{solution[pivot_col]}",
                "matrix": [r[:] for r in matrix]
            })

    steps.append({
        "operation": "Final Solution",
        "solution": solution
    })

    return solution, "unique_solution", steps


# --------------------------------------------------
# Temporary Testing
# --------------------------------------------------

if __name__ == "__main__":

    print("========================================")
    print("      GAUSSIAN ELIMINATION TEST")
    print("========================================")

    matrix = [
        [2, 1, -1, 8],
        [-3, -1, 2, -11],
        [-2, 1, 2, -3]
    ]

    solution, elimination_steps, substitution_steps, status = (
        solve_by_gaussian_elimination(matrix)
    )

    print("\nGaussian Elimination Steps:\n")

    for step in elimination_steps:

        print(step["operation"])
        print(step["matrix"])
        print()

    print("Back Substitution Steps:\n")

    for step in substitution_steps:

        print(step["operation"])

        if "matrix" in step:
            print(step["matrix"])

        if "solution" in step:
            print("Solution:", step["solution"])

        print()

    print("Status:", status)
    print("Final Solution:", solution)

    print("\n========================================")
    print("       GAUSS-JORDAN TEST")
    print("========================================")

    matrix2 = [
        [2, 1, -1, 8],
        [-3, -1, 2, -11],
        [-2, 1, 2, -3]
    ]

    final_matrix, jordan_steps = gauss_jordan(matrix2)

    print("\nGauss-Jordan Steps:\n")

    for step in jordan_steps:

        print(step["operation"])
        print(step["matrix"])
        print()

    solution2, status2, solution_steps = (
        extract_solution_from_rref(final_matrix)
    )

    print("RREF:")
    print(final_matrix)

    print("\nGauss-Jordan Solution Steps:\n")

    for step in solution_steps:
        print(step["operation"])

    print("\nStatus:", status2)
    print("Final Solution:", solution2)