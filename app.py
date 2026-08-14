from flask import Flask, render_template, request

from solver.gaussian_solver import (
    solve_by_gaussian_elimination,
    gauss_jordan
)

from solver.dependence_solver import (
    check_dependence
)

from solver.span_basis_solver import (
    span_basis_dimension
)

from solver.kernel_image_solver import (
    find_kernel,
    find_image
)

from solver.polynomial_solver import (
    characteristic_polynomial
)

from solver.gram_schmidt_solver import (
    gram_schmidt
)


app = Flask(__name__)


# ============================================================
# Helper Functions
# ============================================================

def read_matrix(rows, cols, field_name="matrix"):
    """
    Reads matrix values submitted by the HTML form.
    """

    values = request.form.getlist(field_name)

    if not values:
        raise ValueError(
            "Please enter the matrix values."
        )

    if len(values) != rows * cols:
        raise ValueError(
            "Please generate and fill the complete matrix."
        )

    matrix = []

    index = 0

    for i in range(rows):

        current_row = []

        for j in range(cols):

            value = values[index].strip()

            if value == "":
                raise ValueError(
                    "Matrix values cannot be empty."
                )

            current_row.append(float(value))

            index += 1

        matrix.append(current_row)

    return matrix


def read_vectors(number_of_vectors, dimension):
    """
    Reads vector values submitted by the HTML form.

    The generated input boxes must use:

        name="vector"
    """

    values = request.form.getlist("vector")

    expected = (
        number_of_vectors * dimension
    )

    if not values:
        raise ValueError(
            "Please enter the vector values."
        )

    if len(values) != expected:
        raise ValueError(
            "Please generate and fill all vector values."
        )

    vectors = []

    index = 0

    for i in range(number_of_vectors):

        current_vector = []

        for j in range(dimension):

            value = values[index].strip()

            if value == "":
                raise ValueError(
                    "Vector values cannot be empty."
                )

            current_vector.append(
                float(value)
            )

            index += 1

        vectors.append(current_vector)

    return vectors


# ============================================================
# Main Route
# ============================================================

@app.route("/", methods=["GET", "POST"])
def home():

    # Determine the selected topic
    topic = (
        request.form.get("topic")
        or request.args.get("topic")
    )

    # Gaussian form currently does not have
    # a hidden topic input, so identify it
    # using the operation field.
    if not topic and request.form.get("operation"):
        topic = "gaussian"

    # --------------------------------------------------------
    # GET request
    # --------------------------------------------------------

    if request.method == "GET":

        return render_template(
            "index.html",
            topic=topic
        )

    # --------------------------------------------------------
    # POST request
    # --------------------------------------------------------

    try:

        # ====================================================
        # 1. GAUSSIAN / GAUSS-JORDAN
        # ====================================================

        if topic == "gaussian":

            operation = request.form.get(
                "operation"
            )

            rows = int(
                request.form.get("rows")
            )

            cols = int(
                request.form.get("cols")
            )

            if rows < 1 or cols < 1:
                raise ValueError(
                    "Rows and columns must be at least 1."
                )

            matrix = read_matrix(
                rows,
                cols,
                "matrix"
            )

            # ------------------------------------------------
            # Gaussian Elimination
            # ------------------------------------------------

            if operation == "gaussian":

                (
                    solution,
                    elimination_steps,
                    substitution_steps,
                    status
                ) = solve_by_gaussian_elimination(
                    matrix
                )

                if elimination_steps:

                    final_matrix = (
                        elimination_steps[-1]["matrix"]
                    )

                else:

                    final_matrix = matrix

                return render_template(
                    "index.html",
                    topic="gaussian",
                    operation="gaussian",
                    final_matrix=final_matrix,
                    steps=elimination_steps,
                    back_steps=substitution_steps,
                    status=status,
                    solution=solution
                )

            # ------------------------------------------------
            # Gauss-Jordan Elimination
            # ------------------------------------------------

            elif operation == "gauss_jordan":

                (
                    final_matrix,
                    jordan_steps
                ) = gauss_jordan(matrix)

                return render_template(
                    "index.html",
                    topic="gaussian",
                    operation="gauss_jordan",
                    final_matrix=final_matrix,
                    steps=jordan_steps
                )

            else:

                raise ValueError(
                    "Please select a valid operation."
                )

        # ====================================================
        # 2. LINEAR DEPENDENCE
        # ====================================================

        elif topic == "dependence":

            number_of_vectors = int(
                request.form.get("vectors")
            )

            dimension = int(
                request.form.get("dimension")
            )

            if (
                number_of_vectors < 1
                or dimension < 1
            ):
                raise ValueError(
                    "Number of vectors and dimension "
                    "must be at least 1."
                )

            vectors = read_vectors(
                number_of_vectors,
                dimension
            )

            result = check_dependence(
                vectors
            )

            return render_template(
                "index.html",
                topic="dependence",
                result=result
            )

        # ====================================================
        # 3. SPAN, BASIS & DIMENSION
        # ====================================================

        elif topic == "span":

            number_of_vectors = int(
                request.form.get("vectors")
            )

            dimension = int(
                request.form.get("dimension")
            )

            if (
                number_of_vectors < 1
                or dimension < 1
            ):
                raise ValueError(
                    "Number of vectors and dimension "
                    "must be at least 1."
                )

            vectors = read_vectors(
                number_of_vectors,
                dimension
            )
            (
             span,
             basis,
             result_dimension,
             basis_indices,
            steps
) = span_basis_dimension(
    vectors
)

            return render_template(
               "index.html",
                topic="span",
                span=span,
                basis=basis,
                dimension=result_dimension,
                basis_indices=basis_indices,
                steps=steps
)
        # ====================================================
        # 4. KERNEL & IMAGE
        # ====================================================

        elif topic == "kernel":

            rows = int(
                request.form.get("rows")
            )

            cols = int(
                request.form.get("cols")
            )

            if rows < 1 or cols < 1:
                raise ValueError(
                    "Rows and columns must be at least 1."
                )

            matrix = read_matrix(
                rows,
                cols,
                "matrix"
            )

            # ------------------------------------------------
            # Kernel
            # ------------------------------------------------

            (
               kernel_basis,
               kernel_dimension,
               free_columns,
               kernel_pivot_columns,
               kernel_rref_matrix,
               kernel_steps
) = find_kernel(
    matrix
)

            # ------------------------------------------------
            # Image
            # ------------------------------------------------

            (
                image_basis,
                image_dimension,
                image_pivot_columns,
                image_rref_matrix,
                image_steps
) = find_image(
    matrix
)

            return render_template(
    "index.html",
    topic="kernel",

    kernel_basis=kernel_basis,
    kernel_dimension=kernel_dimension,

    image_basis=image_basis,
    image_dimension=image_dimension,

    kernel_steps=kernel_steps,
    image_steps=image_steps,

    kernel_rref_matrix=kernel_rref_matrix,
    image_rref_matrix=image_rref_matrix,

    free_columns=free_columns,
    kernel_pivot_columns=kernel_pivot_columns,
    image_pivot_columns=image_pivot_columns
)

        # ====================================================
        # 5. GRAM-SCHMIDT
        # ====================================================

        elif topic == "gram":

            number_of_vectors = int(
                request.form.get("vectors")
            )

            dimension = int(
                request.form.get("dimension")
            )

            if (
                number_of_vectors < 1
                or dimension < 1
            ):
                raise ValueError(
                    "Number of vectors and dimension "
                    "must be at least 1."
                )

            vectors = read_vectors(
                number_of_vectors,
                dimension
            )

            (
                orthogonal,
                orthonormal,
                steps
            ) = gram_schmidt(
                vectors
            )

            return render_template(
                "index.html",
                topic="gram",
                orthogonal=orthogonal,
                orthonormal=orthonormal,
                steps=steps
            )

        # ====================================================
        # 6. CHARACTERISTIC POLYNOMIAL
        # ====================================================

        elif topic == "characteristic":

            size = int(
                request.form.get("size")
            )

            if size < 1:
                raise ValueError(
                    "Matrix size must be at least 1."
                )

            matrix = read_matrix(
                size,
                size,
                "matrix"
            )

            (
                polynomial,
                steps
            ) = characteristic_polynomial(
                matrix
            )

            return render_template(
                "index.html",
                topic="characteristic",
                polynomial=polynomial,
                steps=steps
            )

        # ====================================================
        # Invalid Topic
        # ====================================================

        else:

            raise ValueError(
                "Please select a valid topic."
            )

    # --------------------------------------------------------
    # Expected Input Errors
    # --------------------------------------------------------

    except ValueError as e:

        return render_template(
            "index.html",
            topic=topic,
            error=str(e)
        )

    # --------------------------------------------------------
    # Unexpected Errors
    # --------------------------------------------------------

    except Exception as e:

        print("ERROR:", e)

        return render_template(
            "index.html",
            topic=topic,
            error=(
                "Unable to solve the problem. "
                "Please check your input."
            )
        )


# ============================================================
# Run Flask Application
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)

