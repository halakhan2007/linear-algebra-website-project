from .gaussian_solver import gaussian_elimination


def check_dependence(matrix):
    """
    Checks whether a set of vectors is linearly
    independent or linearly dependent.

    Vectors are represented as rows.

    Returns:
        result information, pivot count, vectors count,
        reason, and Gaussian elimination steps.
    """

    # Make sure the matrix is not empty
    if not matrix or not matrix[0]:
        return {
            "result": "Invalid Input",
            "pivot_count": 0,
            "number_of_vectors": 0,
            "reason": "The matrix cannot be empty.",
            "steps": []
        }

    # Check that all rows have the same length
    number_of_columns = len(matrix[0])

    for row in matrix:

        if len(row) != number_of_columns:

            return {
                "result": "Invalid Input",
                "pivot_count": 0,
                "number_of_vectors": len(matrix),
                "reason":
                    "All vectors must have the same dimension.",
                "steps": []
            }

    # Number of vectors = number of rows
    number_of_vectors = len(matrix)

    # Perform Gaussian elimination
    final_matrix, steps = gaussian_elimination(matrix)

    # Count pivots
    pivot_count = 0

    for row in final_matrix:

        pivot_found = False

        for element in row:

            if abs(element) > 1e-10:

                pivot_found = True
                break

        if pivot_found:
            pivot_count += 1

    # Determine dependence
    if pivot_count == number_of_vectors:

        result = "Linearly Independent"

        reason = (
            "The number of pivots equals the number "
            "of vectors, so every vector contributes "
            "a new independent direction."
        )

    else:

        result = "Linearly Dependent"

        reason = (
            "The number of pivots is less than the "
            "number of vectors, so at least one vector "
            "does not contribute a new independent direction."
        )

    # Add our own explanation step
    steps.append({
        "operation": "Dependence Check",
        "pivot_count": pivot_count,
        "number_of_vectors": number_of_vectors,
        "result": result
    })

    return {
        "result": result,
        "pivot_count": pivot_count,
        "number_of_vectors": number_of_vectors,
        "reason": reason,
        "steps": steps
    }


# --------------------------------------------------
# Temporary Testing
# --------------------------------------------------

if __name__ == "__main__":

    print("========================================")
    print("     LINEAR DEPENDENCE TEST")
    print("========================================")

    # Test 1: Linearly independent vectors
    independent_matrix = [
        [1, 0],
        [0, 1]
    ]

    result = check_dependence(independent_matrix)

    print("\nTEST 1: Independent vectors")
    print("----------------------------------------")

    print("Result:", result["result"])
    print("Number of vectors:", result["number_of_vectors"])
    print("Number of pivots:", result["pivot_count"])
    print("Reason:", result["reason"])

    print("\nSteps:")

    for step in result["steps"]:

        print(step["operation"])

        if "matrix" in step:
            print(step["matrix"])

        if "pivot_count" in step:
            print(
                "Pivots:",
                step["pivot_count"]
            )

    # Test 2: Linearly dependent vectors
    dependent_matrix = [
        [1, 2],
        [2, 4]
    ]

    result = check_dependence(dependent_matrix)

    print("\n\nTEST 2: Dependent vectors")
    print("----------------------------------------")

    print("Result:", result["result"])
    print("Number of vectors:", result["number_of_vectors"])
    print("Number of pivots:", result["pivot_count"])
    print("Reason:", result["reason"])

    print("\nSteps:")

    for step in result["steps"]:

        print(step["operation"])

        if "matrix" in step:
            print(step["matrix"])

        if "pivot_count" in step:
            print(
                "Pivots:",
                step["pivot_count"]
            )