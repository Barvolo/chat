// script.js
document.addEventListener("DOMContentLoaded", function() {
    var toggleButton = document.getElementById("toggleDetails");
    var detailsContent = document.getElementById("detailsContent");
  
    toggleButton.addEventListener("click", function() {
      var isHidden = detailsContent.style.display === 'none';
      detailsContent.style.display = isHidden ? 'block' : 'none';
      toggleButton.textContent = isHidden ? 'Hide Details' : 'Show Details';
    });
  });