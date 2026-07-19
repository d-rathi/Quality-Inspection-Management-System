
console.log("inspection.js loaded");
// =====================================
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

        // Fixed ID (tire_id)
        const tireId = document.getElementById("tire_id").value.trim();

        const article = document.getElementById("article_number").value.trim();

        if (tireId === "" || article === "") {

            alert("Please fill all mandatory fields.");

            e.preventDefault();

        }

    });

}

// ======================================
// Enable / Disable Raise Defect Button
// ======================================

const inspectionStatus = document.getElementById("inspectionStatus");
const raiseDefectBtn = document.getElementById("raiseDefectBtn");

if (inspectionStatus && raiseDefectBtn) {

    inspectionStatus.addEventListener("change", function () {

        if (this.value === "Fail") {

            raiseDefectBtn.disabled = false;

        }

        else {

            raiseDefectBtn.disabled = true;

        }

    });

}

// ==============================
// Enable / Disable Raise Defect Button
// ==============================

const inspectionStatus = document.getElementById("inspectionStatus");
const raiseDefectBtn = document.getElementById("raiseDefectBtn");

inspectionStatus.addEventListener("change", function () {

    if (this.value === "Fail") {

        raiseDefectBtn.disabled = false;

    } else {

        raiseDefectBtn.disabled = true;

    }

});

}