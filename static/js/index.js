// Получаем все кнопки сортировки
const sortingButtons = document.querySelectorAll('.sorting-btn');

// Обрабатываем клик на каждой кнопке
sortingButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Удаляем класс active у всех кнопок
        sortingButtons.forEach(btn => btn.classList.remove('active'));
        // Добавляем класс active только к нажатой кнопке
        button.classList.add('active');
    });
});

function sendLikeDislike(url, id, action) {
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')
        },
        body: JSON.stringify({ id: id, type: action })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.rating !== undefined) {
            const inputElement = document.getElementById(`like${id}`);
            if (inputElement) {
                inputElement.value = data.rating;
            } else {
                console.error("Element not found:", `like${id}`);
            }
        } else {
            console.error("Error:", data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}

function increaseValue(questionId) {
    sendLikeDislike(likeDislikeQuestionUrl, questionId, 'like');
}

function decreaseValue(questionId) {
    sendLikeDislike(likeDislikeQuestionUrl, questionId, 'dislike');
}

function AnsincreaseValue(answerId) {
    sendLikeDislike(likeDislikeAnswerUrl, answerId, 'like');
}

function decreaseValueAns(answerId) {
    sendLikeDislike(likeDislikeAnswerUrl, answerId, 'dislike');
}

document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.answer-checkbox');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const answerId = this.dataset.answerId;
            const questionId = this.closest('.qa-container').dataset.questionId;

            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/set_correct_answer/', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    if (response.status === 'error') {
                        alert(response.message);
                    }
                }
            };

            xhr.send(`question_id=${questionId}&answer_id=${answerId}`);
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; cookies.length > i; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
