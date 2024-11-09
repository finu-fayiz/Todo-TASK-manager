document.addEventListener("DOMContentLoaded", function() {
    // Select all toggle buttons
    const toggleButtons = document.querySelectorAll('.btn-toggle');

    toggleButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // 
            const todoItem = button.closest('li');
            
            // Toggle complete or pending class
            if (todoItem.classList.contains('complete')) {
                todoItem.classList.remove('complete');
                todoItem.classList.add('pending');
                button.textContent = "Mark Complete";
            } else {
                todoItem.classList.remove('pending');
                todoItem.classList.add('complete');
                button.textContent = "Mark Pending";
            }
            
            
            fetch(button.href, {
                method: 'GET', 
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).then(response => response.json())
              .then(data => console.log('Status toggled:', data))
              .catch(error => console.error('Error:', error));
        });
    });
});