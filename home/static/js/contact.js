const formResponse = document.getElementById("formResponse");
setTimeout(() => {
    formResponse.style.opacity = '0';
    formResponse.style.transition = 'opacity 0.5s ease';
    setTimeout(() => {
        formResponse.style.display = 'none';
    }, 500);
}, 3000);

