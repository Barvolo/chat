document.addEventListener("DOMContentLoaded", function() {
    var toggleButton = document.getElementById("toggleDetails");
    var detailsContent = document.getElementById("detailsContent");
    var barChartContainer = document.getElementById("chartContainer");
    var pieChartContainer = document.getElementById("pieChartContainer");

    // Event listener for the toggle button
    // Event listener for the toggle button
toggleButton.addEventListener("click", function() {
    var isHidden = detailsContent.style.display === 'none';
    detailsContent.style.display = isHidden ? 'block' : 'none';
    barChartContainer.style.display = isHidden ? 'block' : 'none';
    pieChartContainer.style.display = isHidden ? 'block' : 'none';
    toggleButton.textContent = isHidden ? 'Hide Details' : 'Show Details';
});


    // Initialize the bar chart if the container exists
    if (barChartContainer) {
        var ctx = document.getElementById('detailsChart').getContext('2d');
        var detailsChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: chartLabels,
                datasets: [{
                    label: 'Monthly Savings',
                    data: chartData,
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
    }

    // Initialize the pie chart if the container exists
    if (pieChartContainer) {
        var pieCtx = document.getElementById('modelUsageChart').getContext('2d');
        var modelUsageChart = new Chart(pieCtx, {
            type: 'pie',
            data: {
                labels: modelUsageLabels,
                datasets: [{
                    data: modelUsageData,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255,99,132,1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Model Usage'
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
    }
});
