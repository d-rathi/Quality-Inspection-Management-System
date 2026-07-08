// ===============================
// Dashboard JavaScript
// ===============================

// Search Table

const searchInput = document.querySelector(".top-right input");

if (searchInput) {

    searchInput.addEventListener("keyup", function () {

        let filter = this.value.toLowerCase();

        let rows = document.querySelectorAll("tbody tr");

        rows.forEach(function (row) {

            let text = row.innerText.toLowerCase();

            row.style.display = text.includes(filter) ? "" : "none";

        });

    });

}


// ===============================
// Pagination (Demo)
// ===============================

const pageButtons = document.querySelectorAll(".pagination button");

pageButtons.forEach(button => {

    button.addEventListener("click", function () {

        pageButtons.forEach(btn => {

            if(btn.innerText !== "Previous" && btn.innerText !== "Next"){

                btn.classList.remove("active-page");

            }

        });

        if(this.innerText !== "Previous" && this.innerText !== "Next"){

            this.classList.add("active-page");

        }

    });

});


// ===============================
// Line Chart
// ===============================

const lineCanvas = document.getElementById("lineChart");

if(lineCanvas){

new Chart(lineCanvas,{

type:"line",

data:{

labels:["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],

datasets:[{

label:"Inspection",

data:[18,25,20,28,35,30,40],

borderColor:"#2d7ff9",

backgroundColor:"rgba(45,127,249,0.2)",

fill:true,

tension:0.4

}]

},

options:{

responsive:true,

plugins:{

legend:{

display:false

}

}

}

});

}


// ===============================
// Pie Chart
// ===============================

const pieCanvas=document.getElementById("pieChart");

if(pieCanvas){

new Chart(pieCanvas,{

type:"pie",

data:{

labels:["Passed","Rejected","Pending"],

datasets:[{

data:[115,5,3],

backgroundColor:[

"#4CAF50",

"#F44336",

"#FFC107"

]

}]

},

options:{

responsive:true

}

});

}


// ===============================
// Logout
// ===============================

const logout=document.querySelector(".sidebar ul li:last-child");

if(logout){

logout.addEventListener("click",function(){

let confirmLogout=confirm("Are you sure you want to logout?");

if(confirmLogout){

window.location.href="/login";

}

});

}