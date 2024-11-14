document.addEventListener('DOMContentLoaded', function() {
    const deleteForms = document.querySelectorAll('form.delete-form');

    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const confirmation = confirm('Are you sure you want to delete this item?');
            if (confirmation) {
                form.submit();
            }
        });
    });
});