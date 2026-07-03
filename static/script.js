// Show / Hide Registration Code

const showCode = document.getElementById("showCode");
const secretCode = document.getElementById("secretCode");

if (showCode && secretCode) {

    showCode.addEventListener("change", function () {

        if (this.checked) {

            secretCode.type = "text";

        } else {

            secretCode.type = "password";

        }

    });

}


// Verify Registration Code

function verifyCode() {

    const enteredCode = document.getElementById("secretCode").value;

    const message = document.getElementById("message");

    const correctCode = "QIMS2026";


    if (enteredCode === correctCode) {

        alert("Registration Code Verified Successfully!");

        window.location.href = "signup.html";

    }

    else {

        message.innerHTML = "❌ Invalid Registration Code! Please contact your Administrator.";

    }

}