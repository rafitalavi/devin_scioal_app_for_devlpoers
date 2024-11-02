// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();
});


// Select all alert elements
let alertWrappers = document.querySelectorAll('.alert');

alertWrappers.forEach(alertWrapper => {
  let alertClose = alertWrapper.querySelector('.alert__close');
  
  if (alertClose) {
    alertClose.addEventListener('click', () => {
      alertWrapper.style.display = 'none';  // Hide the alert
      alertWrapper.setAttribute('aria-hidden', 'true'); // Accessibility improvement
    });
  }
});