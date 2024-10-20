const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');

function addMessage(sender, message) {
    const messageDiv = document.createElement('div');
    messageDiv.innerHTML = \`<strong>\${sender}:</strong> \${message}\`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

sendButton.addEventListener('click', () => {
    const question = userInput.value.trim();
    if (!question) {
        alert('Please enter a question.');
        return;
    }

    addMessage('You', question);
    userInput.value = '';

    fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'question': question })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            addMessage('Assistant', 'Error: ' + data.error);
        } else {
            addMessage('Assistant', data.answer);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage('Assistant', 'An error occurred while fetching the answer.');
    });
});
