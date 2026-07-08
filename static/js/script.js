// ============================
// Registration Page
// ============================

const showCode = document.getElementById("showCode");
const secretCode = document.getElementById("secretCode");

if (showCode && secretCode) {

    showCode.addEventListener("change", function () {

        secretCode.type = this.checked ? "text" : "password";

    });

}

function verifyCode() {

    const code = document.getElementById("secretCode").value.trim();

    const message = document.getElementById("message");

    // Remove previous classes
    message.className = "message";

    // Empty Input
    if (code === "") {

        message.classList.add("warning");

        message.innerHTML =
        "⚠ Please enter the Registration Code.";

        return;

    }

    // Correct Code
    if (code === "QIMS2026") {

        message.classList.add("success");

        message.innerHTML =
        "✔ Verification Successful!<br>Redirecting to Account Registration...";

        setTimeout(function () {

            window.location.href = "/signup";

        }, 1500);

    }

    // Wrong Code
    else {

        message.classList.add("error");

        message.innerHTML =
        "✖ Verification Failed!<br>Please enter a valid Registration Code.";

    }

}



// ============================
// Signup Page
// ============================

function togglePassword(){

    const password=document.getElementById("password");

    if(password){

        password.type=password.type==="password" ? "text" : "password";

    }

}

function toggleConfirmPassword(){

    const confirm=document.getElementById("confirmPassword");

    if(confirm){

        confirm.type=confirm.type==="password" ? "text" : "password";

    }

}

// ============================
// Login Page
// ============================

function toggleLoginPassword() {

    const password = document.getElementById("loginPassword");

    if (password.type === "password") {
        password.type = "text";
    } else {
        password.type = "password";
    }

}

