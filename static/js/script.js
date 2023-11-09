document.addEventListener("DOMContentLoaded", function() {
    var toggleButton = document.getElementById("toggleDetails");
    var detailsContent = document.getElementById("detailsContent");
    var chartContainer = document.getElementById("chartContainer");
  
    // Event listener for the toggle button
    toggleButton.addEventListener("click", function() {
      var isHidden = chartContainer.style.display === 'none';
      chartContainer.style.display = isHidden ? 'block' : 'none';
      detailsContent.style.display = isHidden ? 'block' : 'none';
      toggleButton.textContent = isHidden ? 'Hide Details' : 'Show Details';
    });
  
    // Initialize the chart with data passed from Flask
    var ctx = document.getElementById('detailsChart').getContext('2d');
    var detailsChart = new Chart(ctx, {
        type: 'bar', // Change to 'line', 'doughnut', etc. as desired
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
  });
  