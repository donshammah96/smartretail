document.addEventListener('DOMContentLoaded', function() {
    // Example of initializing a chart using Chart.js
    const ctx = document.getElementById('performanceChart').getContext('2d');
    const performanceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Employee 1', 'Employee 2', 'Employee 3'], // Replace with actual employee names
            datasets: [{
                label: 'Performance Score',
                data: [75, 85, 90], // Replace with actual performance scores
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Example of dynamic content loading using AJAX (if needed)
    const loadContent = (url, targetElementId) => {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                document.getElementById(targetElementId).innerHTML = html;
            })
            .catch(error => console.error('Error loading content:', error));
    };
});