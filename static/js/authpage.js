const showMobileRegisterBtn = document.getElementById('showMobileRegister');
const showMobileLoginBtn = document.getElementById('showMobileLogin');
const mobileLoginForm = document.querySelector('.mobile-login-form');
const mobileRegisterForm = document.querySelector('.mobile-register-form');

showMobileRegisterBtn.addEventListener('click', () => {
    mobileLoginForm.style.display = 'none';
    mobileRegisterForm.style.display = 'block';
});

showMobileLoginBtn.addEventListener('click', () => {
    mobileRegisterForm.style.display = 'none';
    mobileLoginForm.style.display = 'block';
});


const registerButton = document.getElementById('registerBtn');
const loginButton = document.getElementById('loginBtn');
const authWrapper = document.getElementById('authWrapper');

registerButton.addEventListener('click', () => {
    if (window.innerWidth > 768) { 
        authWrapper.classList.add("right-panel-active");
    }
});

loginButton.addEventListener('click', () => {
    if (window.innerWidth > 768) { 
        authWrapper.classList.remove("right-panel-active");
    }
});


function highlightIcon(iconID) {
    document.getElementById(iconID).style.color = "#FDC500";
}

function removeHighlight(iconID) {
    document.getElementById(iconID).style.color = "#00296B";
}
