function showToast(type, title, message) {
    const container = document.getElementById('toasts-container');

    const iconClass = {
        info: 'fa-info-circle',
        error: 'fa-times-circle',
        success: 'fa-check-circle',
        warning: 'fa-exclamation-circle',
    };

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="toast-icon fas ${iconClass[type]}"></i>
        <div class="toast-content">
            <strong>${title}</strong>
            <p>${message}</p>
        </div>
        <button class="toast-close" aria-label="Close toast">
            <i class="fas fa-times"></i>
        </button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('fade-out');
        setTimeout(() => toast.remove(), 500);
    }, 6000);
}
