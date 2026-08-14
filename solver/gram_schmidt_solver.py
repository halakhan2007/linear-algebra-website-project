import math


def gram_schmidt(vectors):
    """
    Applies the Gram-Schmidt orthogonalization process.

    Converts a set of linearly independent vectors into:
        1. Orthogonal vectors
        2. Orthonormal vectors

    Returns:
        orthogonal, orthonormal, steps
    """

    steps = []

    # ----------------------------------------
    # Input validation
    # ----------------------------------------

    if not vectors:

        raise ValueError(
            "At least one vector is required."
        )

    # Check that vectors are not empty
    for index, vector in enumerate(vectors):

        if not vector:

            raise ValueError(
                f"Vector v{index + 1} cannot be empty."
            )

    # Check that all vectors have
    # the same dimension
    dimension = len(vectors[0])

    for index, vector in enumerate(vectors):

        if len(vector) != dimension:

            raise ValueError(
                "All vectors must have "
                "the same dimension."
            )

    # ----------------------------------------
    # Store orthogonal vectors
    # ----------------------------------------

    orthogonal = []

    # ----------------------------------------
    # Gram-Schmidt process
    # ----------------------------------------

    for vector_index, vector in enumerate(vectors):

        # Start with the original vector
        u = vector[:]

        steps.append({
            "operation":
                f"Start with v{vector_index + 1}",
            "vector": vector[:]
        })

        # ------------------------------------
        # Subtract projections onto
        # previous orthogonal vectors
        # ------------------------------------

        for previous_index, previous_u in enumerate(
            orthogonal
        ):

            # Calculate v · u
            dot_v_u = sum(
                vector[i] * previous_u[i]
                for i in range(dimension)
            )

            # Calculate u · u
            dot_u_u = sum(
                previous_u[i] * previous_u[i]
                for i in range(dimension)
            )

            # --------------------------------
            # Safety check
            # --------------------------------

            if abs(dot_u_u) < 1e-10:

                steps.append({
                    "operation":
                        f"u{previous_index + 1} "
                        "is a zero vector."
                })

                return None, None, steps

            # --------------------------------
            # Projection coefficient
            # --------------------------------

            coefficient = (
                dot_v_u / dot_u_u
            )

            steps.append({
                "operation":
                    f"Calculate projection coefficient "
                    f"for v{vector_index + 1} "
                    f"onto u{previous_index + 1}",
                "dot_v_u": dot_v_u,
                "dot_u_u": dot_u_u,
                "coefficient": coefficient
            })

            # --------------------------------
            # Projection vector
            # --------------------------------

            projection = [
                coefficient * previous_u[i]
                for i in range(dimension)
            ]

            steps.append({
                "operation":
                    f"Projection of v{vector_index + 1} "
                    f"onto u{previous_index + 1}",
                "projection": projection
            })

            # --------------------------------
            # Subtract projection
            # --------------------------------

            u = [
                u[i] - projection[i]
                for i in range(dimension)
            ]

            steps.append({
                "operation":
                    f"Subtract projection from v{vector_index + 1}",
                "result": u[:]
            })

        # ------------------------------------
        # Calculate magnitude
        # ------------------------------------

        magnitude = math.sqrt(
            sum(
                element ** 2
                for element in u
            )
        )

        steps.append({
            "operation":
                f"Magnitude of u{vector_index + 1}",
            "magnitude": magnitude
        })

        # ------------------------------------
        # Check for linear dependence
        # ------------------------------------

        if magnitude < 1e-10:

            steps.append({
                "operation":
                    f"v{vector_index + 1} is linearly "
                    "dependent on the previous vectors."
            })

            return None, None, steps

        # ------------------------------------
        # Store orthogonal vector
        # ------------------------------------

        orthogonal.append(u)

        steps.append({
            "operation":
                f"Final orthogonal vector "
                f"u{vector_index + 1}",
            "vector": u[:]
        })

    # ----------------------------------------
    # Normalize orthogonal vectors
    # ----------------------------------------

    orthonormal = []

    for index, vector in enumerate(
        orthogonal
    ):

        magnitude = math.sqrt(
            sum(
                element ** 2
                for element in vector
            )
        )

        # ------------------------------------
        # Safety check
        # ------------------------------------

        if magnitude < 1e-10:

            steps.append({
                "operation":
                    f"Cannot normalize u{index + 1} "
                    "because its magnitude is zero."
            })

            return None, None, steps

        # ------------------------------------
        # Normalize
        # ------------------------------------

        unit_vector = [
            element / magnitude
            for element in vector
        ]

        orthonormal.append(unit_vector)

        steps.append({
            "operation":
                f"Normalize u{index + 1}",
            "magnitude": magnitude,
            "unit_vector": unit_vector
        })

    # ----------------------------------------
    # Final result
    # ----------------------------------------

    steps.append({
        "operation": "Gram-Schmidt Complete",
        "orthogonal": [
            vector[:]
            for vector in orthogonal
        ],
        "orthonormal": [
            vector[:]
            for vector in orthonormal
        ]
    })

    return orthogonal, orthonormal, steps


# --------------------------------------------------
# Temporary Testing
# --------------------------------------------------

if __name__ == "__main__":

    print("========================================")
    print("       GRAM-SCHMIDT METHOD TEST")
    print("========================================")

    vectors = [
        [1, 1],
        [1, 0]
    ]

    print("\nInput Vectors:")
    print(vectors)

    try:

        orthogonal, orthonormal, steps = (
            gram_schmidt(vectors)
        )

        print("\n========================================")
        print("ORTHOGONAL VECTORS")
        print("========================================")

        print(orthogonal)

        print("\n========================================")
        print("ORTHONORMAL VECTORS")
        print("========================================")

        print(orthonormal)

        print("\n========================================")
        print("STEPS")
        print("========================================")

        for step in steps:

            print("\nOperation:")
            print(step["operation"])

            if "vector" in step:
                print("Vector:", step["vector"])

            if "dot_v_u" in step:
                print(
                    "v · u:",
                    step["dot_v_u"]
                )

            if "dot_u_u" in step:
                print(
                    "u · u:",
                    step["dot_u_u"]
                )

            if "coefficient" in step:
                print(
                    "Coefficient:",
                    step["coefficient"]
                )

            if "projection" in step:
                print(
                    "Projection:",
                    step["projection"]
                )

            if "result" in step:
                print(
                    "After subtraction:",
                    step["result"]
                )

            if "magnitude" in step:
                print(
                    "Magnitude:",
                    step["magnitude"]
                )

            if "unit_vector" in step:
                print(
                    "Unit vector:",
                    step["unit_vector"]
                )

            if "orthogonal" in step:
                print(
                    "Final orthogonal:",
                    step["orthogonal"]
                )

            if "orthonormal" in step:
                print(
                    "Final orthonormal:",
                    step["orthonormal"]
                )

    except ValueError as e:

        print("Error:", e)