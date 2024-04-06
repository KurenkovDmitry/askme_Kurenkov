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

function increaseValue(QuestionID) {
    let value = parseInt(document.getElementById(`like${QuestionID}`).value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    document.getElementById(`like${QuestionID}`).value = value;
}

function decreaseValue(QuestionID) {
    let value = parseInt(document.getElementById(`like${QuestionID}`).value, 10);
    value = isNaN(value) ? 0 : value;
    value--;
    document.getElementById(`like${QuestionID}`).value = value;
}