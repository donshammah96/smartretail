document.addEventListener('DOMContentLoaded', function() {
    // Example of initializing a chart using Chart.js
    const ctx = document.getElementById('activityChart').getContext('2d');
    const activityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['2023-01-01', '2023-01-02', '2023-01-03'], // Replace with actual timestamps
            datasets: [{
                label: 'User Activities',
                data: [5, 10, 3], // Replace with actual activity counts
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
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