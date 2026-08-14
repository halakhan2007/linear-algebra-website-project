```javascript
// ============================================================
// Gaussian Elimination / Gauss-Jordan
// ============================================================```

function generateMatrix() {
    const rows = document.getElementById("rows").value;
    const cols = document.getElementById("cols").value;
    const area = document.getElementById("matrix-inputs");

    area.innerHTML = "";

    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            area.innerHTML += `
                <input
                    type="number"
                    name="matrix"
                    placeholder="${i + 1},${j + 1}"
                    step="any"
                    required
                >
            `;
        }

        area.innerHTML += "<br><br>";
    }
}


// ============================================================
// Linear Dependence
// ============================================================

function generateVectors() {
    const vectors = document.getElementById("vectors").value;
    const dimension = document.getElementById("dimension").value;
    const area = document.getElementById("vector-inputs");

    area.innerHTML = "";

    for (let i = 0; i < vectors; i++) {
        area.innerHTML += "<label>V"+(i + 1)+":</label>";

        for (let j = 0; j < dimension; j++) {
               area.innerHTML +=
                '<input type="number" name="vector" ' +
                'placeholder="' + (j + 1) + '" ' +
                'step="any" required>';

        }


        area.innerHTML += "<br><br>";
    }
}


// ============================================================
// Span, Basis and Dimension
// ============================================================

function generateSpanVectors() {

    const vectors = document.getElementById("vectors").value;
    const dimension = document.getElementById("dimension").value;
    const area = document.getElementById("span-vector-inputs");

    area.innerHTML = "";

    for (let i = 0; i < vectors; i++) {

        area.innerHTML += "<label>V" + (i + 1) + ":</label>";

        for (let j = 0; j < dimension; j++) {

            area.innerHTML +=
                '<input type="number" name="vector" ' +
                'placeholder="' + (j + 1) + '" ' +
                'step="any" required>';

        }

        area.innerHTML += "<br><br>";
    }
}

// ============================================================
// Kernel and Image
// ============================================================

function generateKernelMatrix() {
    const rows = document.getElementById("kernel-rows").value;
    const cols = document.getElementById("kernel-cols").value;
    const area = document.getElementById("kernel-matrix-inputs");

    area.innerHTML = "";

    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            area.innerHTML += `
                <input
                    type="number"
                    name="matrix"
                    placeholder="${i + 1},${j + 1}"
                    step="any"
                    required
                >
            `;
        }

        area.innerHTML += "<br><br>";
    }
}


// ============================================================
// Characteristic Polynomial
// ============================================================

function generateCharacteristicMatrix() {
    const size = document.getElementById("matrix-size").value;
    const area = document.getElementById(
        "characteristic-matrix-inputs"
    );

    area.innerHTML = "";

    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            area.innerHTML += `
                <input
                    type="number"
                    name="matrix"
                    placeholder="${i + 1},${j + 1}"
                    step="any"
                    required
                >
            `;
        }

        area.innerHTML += "<br><br>";
    }
}


// ============================================================
// Gram-Schmidt
// ============================================================

function generateGramVectors() {
    const vectors = document.getElementById("gram-vectors").value;
    const dimension = document.getElementById("gram-dimension").value;
    const area = document.getElementById("gram-vector-inputs");

    area.innerHTML = "";

    for (let i = 0; i < vectors; i++) {
        area.innerHTML += "<label>V" + (i + 1) + ":</label>";

        for (let j = 0; j < dimension; j++) {
            area.innerHTML += `
                <input
                    type="number"
                    name="vector"
                    placeholder="${j + 1}"
                    step="any"
                    required
                >
            `;
        }

        area.innerHTML += "<br><br>";
    }
}

