// ======================================
// Inspection Page
// ======================================

// Auto Fill Today's Date

window.onload = function () {

    const dateField = document.getElementById("inspection_date");

    if (dateField) {

        const today = new Date().toISOString().split("T")[0];

        dateField.value = today;

    }

};


// ======================================
// Status Color Change
// ======================================

const status = document.getElementById("status");

if (status) {

    status.addEventListener("change", function () {

        if (this.value === "Pass") {

            this.style.border = "2px solid green";

        }

        else if (this.value === "Fail") {

            this.style.border = "2px solid red";

        }

        else {

            this.style.border = "1px solid #ccc";

        }

    });

}


// ======================================
// Final Decision Alert
// ======================================

const decision = document.getElementById("final_decision");

if (decision) {

    decision.addEventListener("change", function () {

        if (this.value === "Rejected") {

            alert("Rejected tyre will require further quality review.");

        }

    });

}


// ======================================
// Form Validation
// ======================================

const inspectionForm = document.querySelector("form");

if (inspectionForm) {

    inspectionForm.addEventListener("submit", function (e) {

        const tyreId = document.getElementById("tyre_id").value.trim();

        const article = document.getElementById("article_number").value.trim();

        if (tyreId === "" || article === "") {

            alert("Please fill all mandatory fields.");

            e.preventDefault();

        }

    });

}