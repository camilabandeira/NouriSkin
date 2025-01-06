document.getElementById('newsletter-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const form = e.target;
    const url = form.action;
    const emailInput = document.getElementById('mce-EMAIL');
    const messageDiv = document.getElementById('newsletter-message');

    messageDiv.style.display = 'block';
    messageDiv.style.color = 'black';
    messageDiv.textContent = 'Submitting...';

    const formData = new FormData(form);
    const params = new URLSearchParams(formData);

    fetch(`${url}&${params}`, {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            console.log('Mailchimp Response:', data);

            if (data.result === 'success') {
                messageDiv.style.color = 'green';
                messageDiv.textContent = 'Thank you for subscribing!';
                emailInput.value = '';
            } else {
                messageDiv.style.color = 'red';
                messageDiv.textContent = data.msg || 'An error occurred. Please try again.';
            }
        })
        .catch(error => {
            console.error('AJAX Error:', error);
            messageDiv.style.color = 'red';
            messageDiv.textContent = 'An error occurred. Please try again.';
        });
});
