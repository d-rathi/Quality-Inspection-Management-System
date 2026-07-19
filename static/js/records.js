// ======================================
// Records Page
// ======================================

// Auto Focus on Search Box

window.onload = function () {

    const searchBox = document.querySelector(".top-right input");

    if (searchBox) {

        searchBox.focus();

    }

};


// ======================================
// Search (Frontend)
// ======================================

const searchInput = document.querySelector(".top-right input");

if (searchInput) {

    searchInput.addEventListener("keyup", function () {

        let filter = this.value.toLowerCase();

        let rows = document.querySelectorAll("tbody tr");

        rows.forEach(function (row) {

            let text = row.innerText.toLowerCase();

            if (text.includes(filter)) {

                row.style.display = "";

            } else {

                row.style.display = "none";

            }

        });

    });

}


// ======================================
// Status Filter
// ======================================

const statusFilter = document.querySelector(".top-right select");

if (statusFilter) {

    statusFilter.addEventListener("change", function () {

        let value = this.value;

        let rows = document.querySelectorAll("tbody tr");

        rows.forEach(function (row) {

            let status = row.querySelector(".status").innerText;

            if (value === "All Status" || status === value) {

                row.style.display = "";

            } else {

                row.style.display = "none";

            }

        });

    });

}

// ======================================
// Pagination
// ======================================

const rowsPerPage = 5;
const tableRows = document.querySelectorAll("tbody tr");
const pagination = document.querySelector(".pagination");

let currentPage = 1;

function showPage(page) {

    currentPage = page;

    tableRows.forEach((row, index) => {

        if (index >= (page - 1) * rowsPerPage &&
            index < page * rowsPerPage) {

            row.style.display = "";

        } else {

            row.style.display = "none";

        }

    });

    updateButtons();

}

function updateButtons() {

    pagination.innerHTML = "";

    const totalPages = Math.ceil(tableRows.length / rowsPerPage);

    // Previous
    const prev = document.createElement("button");
    prev.textContent = "Previous";
    prev.disabled = currentPage === 1;

    prev.onclick = () => showPage(currentPage - 1);

    pagination.appendChild(prev);

    // Numbers
    for (let i = 1; i <= totalPages; i++) {

        const btn = document.createElement("button");

        btn.textContent = i;

        if (i === currentPage)
            btn.classList.add("active-page");

        btn.onclick = () => showPage(i);

        pagination.appendChild(btn);
    }

    // Next
    const next = document.createElement("button");
    next.textContent = "Next";
    next.disabled = currentPage === totalPages;

    next.onclick = () => showPage(currentPage + 1);

    pagination.appendChild(next);

}

showPage(1);