document.addEventListener('DOMContentLoaded', () => {
    const toasts = document.querySelectorAll('.toast');

    toasts.forEach((toast) => {
        setTimeout(() => {
            toast.classList.add('fade-out');
            setTimeout(() => toast.remove(), 500);
        }, 6000);

        const closeButton = toast.querySelector('.toast-close');
        closeButton.addEventListener('click', () => {
            toast.classList.add('fade-out');
            setTimeout(() => toast.remove(), 500);
        });
    });
});
