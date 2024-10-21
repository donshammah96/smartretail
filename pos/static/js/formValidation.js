document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(form);
        const xhr = new XMLHttpRequest();
        xhr.open('POST', form.action, true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.onload = function() {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                if (response.success) {
                    alert('Form submitted successfully!');
                    form.reset();
                } else {
                    const errors = response.errors;
                    const errorDiv = document.getElementById('formErrors');
                    errorDiv.innerHTML = '';
                    for (const field in errors) {
                        const errorList = errors[field];
                        errorList.forEach(error => {
                            const errorItem = document.createElement('div');
                            errorItem.innerText = `${field}: ${error}`;
                            errorDiv.appendChild(errorItem);
                        });
                    }
                    errorDiv.style.display = 'block';
                }
            } else {
                alert('An error occurred while submitting the form.');
            }
        };
        xhr.send(formData);
    });
});