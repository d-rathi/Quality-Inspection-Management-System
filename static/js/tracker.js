// ======================================
// Defect Tracker
// ======================================

console.log("Tracker Loaded Successfully");

// ======================================
// Live Search
// ======================================

const searchInput = document.getElementById("searchInput");

if (searchInput) {

    searchInput.addEventListener("keyup", function () {

        let filter = this.value.toLowerCase();

        let rows = document.querySelectorAll("#trackerTable tbody tr");

        rows.forEach(function(row){

            let text = row.innerText.toLowerCase();

            if(text.includes(filter)){

                row.style.display = "";

            }

            else{

                row.style.display = "none";

            }

        });

    });

}

// ======================================
// Highlight High Severity
// ======================================

const rows = document.querySelectorAll("#trackerTable tbody tr");

rows.forEach(function(row){

    let severity = row.cells[4].innerText.trim();

    if(severity === "High"){

        row.style.background = "#fff5f5";

    }

});

// ======================================
// Row Click Effect
// ======================================

rows.forEach(function(row){

    row.addEventListener("click",function(){

        row.style.backgroundColor="#eaf3ff";

        setTimeout(function(){

            if(row.cells[4].innerText.trim()=="High"){

                row.style.background="#fff5f5";

            }

            else{

                row.style.background="";

            }

        },300);

    });

});