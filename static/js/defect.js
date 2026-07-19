// ======================================
// Defect Management Page
// ======================================

document.addEventListener("DOMContentLoaded", function () {

    const inspectionStatus = document.getElementById("inspectionStatus");
    const raiseDefectBtn = document.getElementById("raiseDefectBtn");

    // Status change code...

    raiseDefectBtn.addEventListener("click", function () {

        window.location.href = "/defect";

    });

});
    // ==============================
    // Auto Fill Today's Date
    // ==============================

    const defectDate = document.getElementById("defect_date");

    if (defectDate) {

        const today = new Date().toISOString().split("T")[0];
        defectDate.value = today;

    }

    // ==============================
    // Form Validation
    // ==============================

    const defectForm = document.querySelector("form");

    if (defectForm) {

        defectForm.addEventListener("submit", function (e) {

            const tyreId = document.getElementById("tyre_id").value.trim();
            const articleNumber = document.getElementById("article_number").value.trim();
            const defectCategory = document.getElementById("defect_category").value;
            const severity = document.getElementById("severity").value;
            const defectDescription = document.getElementById("defect_description").value.trim();
            const raisedBy = document.getElementById("raised_by").value.trim();

            if (
                tyreId === "" ||
                articleNumber === "" ||
                defectCategory === "" ||
                severity === "" ||
                defectDescription === "" ||
                raisedBy === ""
            ) {

                alert("Please fill all mandatory fields.");

                e.preventDefault();

            }

        });

    }

