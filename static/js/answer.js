function AnsincreaseValue(AnswerID) {
    let value = parseInt(document.getElementById(`${AnswerID}`).value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    document.getElementById(`${AnswerID}`).value = value;
}

function decreaseValueAns(AnswerID) {
    let value = parseInt(document.getElementById(`${AnswerID}`).value, 10);
    value = isNaN(value) ? 0 : value;
    value--;
    document.getElementById(`${AnswerID}`).value = value;
}