document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-button');

    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const confirmation = confirm('Are you sure you want to delete this item?');
            if (confirmation) {
                const deleteUrl = this.getAttribute('data-url');
                fetch(deleteUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getAttribute('data-csrf-token')
                    }
                })
                .then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        console.error('Error deleting object');
                    }
                })
                .catch(error => {
                    console.error('Error deleting object:', error);
                });
            }
        });
    });
});