// ===============================
// Defect Library Search
// ===============================

const searchInput = document.getElementById("searchInput");

if (searchInput) {

    searchInput.addEventListener("keyup", function () {

        let filter = this.value.toLowerCase();

        let cards = document.querySelectorAll(".defect-card");

        cards.forEach(function(card){

            let text = card.innerText.toLowerCase();

            if(text.includes(filter)){

                card.style.display = "block";

            }

            else{

                card.style.display = "none";

            }

        });

    });

}

// ===============================
// Card Hover Animation
// ===============================

const cards = document.querySelectorAll(".defect-card");

cards.forEach(function(card){

    card.addEventListener("mouseenter", function(){

        card.style.transform = "translateY(-8px)";

        card.style.transition = "0.3s";

    });

    card.addEventListener("mouseleave", function(){

        card.style.transform = "translateY(0px)";

    });

});

// ===============================
// Page Loaded
// ===============================

window.onload = function(){

    console.log("Defect Library Loaded Successfully");

};