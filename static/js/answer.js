document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    document.querySelectorAll('.answer-checkbox').forEach(function(checkbox) {
        console.log('Checkbox found with ID:', checkbox.dataset.answerId);
        checkbox.addEventListener('change', function() {
            console.log('Checkbox changed:', this.dataset.answerId);
            let answerId = this.dataset.answerId;
            let isChecked = this.checked;

            fetch('/set-correct-answer/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.csrfToken // Используем токен из глобального контекста
                },
                body: JSON.stringify({
                    'answer_id': answerId,
                    'is_checked': isChecked
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status !== 'success') {
                    alert(data.message);
                    this.checked = !isChecked; // откат изменений
                }
            })
            .catch(error => {
                console.error('Error:', error);
                this.checked = !isChecked; // откат изменений
            });
        });
    });
});
