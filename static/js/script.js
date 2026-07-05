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

    const code = document.getElementById("secretCode").value;

    const message = document.getElementById("message");

    if (code === "QIMS2026") {

        window.location.href = "signup.html";

    }
    else {

        message.innerHTML = "Invalid Registration Code";

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

function toggleLoginPassword(){

    const login=document.getElementById("loginPassword");

    if(login){

        login.type=login.type==="password" ? "text" : "password";

    }

}