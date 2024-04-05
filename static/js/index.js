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

function increaseValue() {
    let value = parseInt(document.getElementById('tentacles').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    document.getElementById('tentacles').value = value;
}

function decreaseValue() {
    let value = parseInt(document.getElementById('tentacles').value, 10);
    value = isNaN(value) ? 0 : value;
    value--;
    document.getElementById('tentacles').value = value;
}