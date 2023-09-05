function typeWriter(elementId, speed) {
    var element = document.getElementById(elementId);
    var text = element.innerHTML;
    element.innerHTML = "";

    var i = 0;
    var interval = setInterval(function () {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
        } else {
            clearInterval(interval);
        }
    }, speed);
}

window.onload = function () {
    typeWriter('loadit', 200);
    setTimeout(function () {
        document.getElementById('lastline').style.visibility = "visible";
        typeWriter('lastline', 100);
    }, 10000);
}


document.body.classList.add('js-loaded');


