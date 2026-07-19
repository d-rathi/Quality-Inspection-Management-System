/* ==========================================
   QIMS REPORT JS
========================================== */

// ================================
// Inspection Trend Chart
// ================================

const trendCanvas = document.getElementById("trendChart");

if (trendCanvas) {

    new Chart(trendCanvas, {

        type: "bar",

        data: {

            labels: trendLabels,

            datasets: [{

                label: "Inspections",

                data: trendValues,

                backgroundColor: "#2d7ff9",

                borderRadius: 8,

                borderSkipped: false

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                y: {

                    beginAtZero: true,

                    ticks: {

                        precision: 0

                    }

                }

            }

        }

    });

}



// ================================
// Pass vs Reject Chart
// ================================

const resultCanvas = document.getElementById("resultChart");

if (resultCanvas) {

    new Chart(resultCanvas, {

        type: "doughnut",

        data: {

            labels: ["Passed", "Rejected"],

            datasets: [{

                data: [passCount, failCount],

                backgroundColor: [

                    "#28a745",

                    "#dc3545"

                ],

                borderWidth: 2

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            cutout: "65%",

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}



// ================================
// Top Defects Chart
// ================================

const defectCanvas = document.getElementById("defectChart");

if (defectCanvas) {

    new Chart(defectCanvas, {

        type: "bar",

        data: {

            labels: defectLabels,

            datasets: [{

                label: "Total Defects",

                data: defectValues,

                backgroundColor: [

                    "#dc3545",

                    "#f39c12",

                    "#2d7ff9",

                    "#28a745",

                    "#8e44ad"

                ],

                borderRadius: 8

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                y: {

                    beginAtZero: true,

                    ticks: {

                        precision: 0

                    }

                }

            }

        }

    });

}



// ================================
// Defect Distribution Chart
// ================================

const distributionCanvas = document.getElementById("distributionChart");

if (distributionCanvas) {

    new Chart(distributionCanvas, {

        type: "polarArea",

        data: {

            labels: defectLabels,

            datasets: [{

                data: defectValues,

                backgroundColor: [

                    "#2d7ff9",

                    "#28a745",

                    "#dc3545",

                    "#f39c12",

                    "#8e44ad"

                ]

            }]

        },

       options: {

    responsive: true,

    maintainAspectRatio: false,

    scales: {

        r: {

            ticks: {

                display: false   // Hide 0,1,2 numbers

            }

        }

    },

    plugins: {

        legend: {

            position: "bottom"

        }

    }

}

    });

}



// ================================
// Search Records
// ================================

const searchInput = document.getElementById("searchInput");

if (searchInput) {

    searchInput.addEventListener("keyup", function () {

        let value = this.value.toLowerCase();

        let rows = document.querySelectorAll("tbody tr");

        rows.forEach(function (row) {

            row.style.display = row.innerText.toLowerCase().includes(value)

                ? ""

                : "none";

        });

    });

}



// ================================
// Card Animation
// ================================

const cards = document.querySelectorAll(".card");

cards.forEach(function (card, index) {

    card.style.opacity = "0";

    card.style.transform = "translateY(20px)";

    setTimeout(function () {

        card.style.transition = ".5s";

        card.style.opacity = "1";

        card.style.transform = "translateY(0)";

    }, index * 120);

});



// ================================
// Graph Animation
// ================================

const graphCards = document.querySelectorAll(".graph-card");

graphCards.forEach(function (graph, index) {

    graph.style.opacity = "0";

    graph.style.transform = "translateY(25px)";

    setTimeout(function () {

        graph.style.transition = ".6s";

        graph.style.opacity = "1";

        graph.style.transform = "translateY(0)";

    }, 500 + (index * 150));

});



// ================================
// Page Loaded
// ================================

console.log("QIMS Report Loaded Successfully");