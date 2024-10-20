document.addEventListener('DOMContentLoaded', function() {
    // Example of initializing a chart using Chart.js
    const ctx = document.getElementById('performanceChart').getContext('2d');
    const performanceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Employee 1', 'Employee 2', 'Employee 3'],
            datasets: [{
                label: 'Performance Score',
                data: [75, 85, 90],
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
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

    // Example of dynamic content loading using AJAX
    const loadContent = (url, targetElementId) => {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                document.getElementById(targetElementId).innerHTML = html;
            })
            .catch(error => console.error('Error loading content:', error));
    };

    // Load employee list dynamically
    document.getElementById('manageEmployeesLink').addEventListener('click', function(event) {
        event.preventDefault();
        loadContent(this.href, 'dynamicContent');
    });

    // Load performance report dynamically
    document.getElementById('performanceReportLink').addEventListener('click', function(event) {
        event.preventDefault();
        loadContent(this.href, 'dynamicContent');
    });

    // Load activity report dynamically
    document.getElementById('activityReportLink').addEventListener('click', function(event) {
        event.preventDefault();
        loadContent(this.href, 'dynamicContent');
    });
});