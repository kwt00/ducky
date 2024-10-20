// Get references to UI elements
const folderInput = document.getElementById('folderInput');
const uploadFolderButton = document.getElementById('uploadFolderButton');
const fileListDiv = document.getElementById('fileList');
const editor = document.getElementById('editor');
const saveButton = document.getElementById('saveButton');
const messageDiv = document.getElementById('message');

const chatWindow = document.getElementById('chatWindow');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');

const beginConversationButton = document.getElementById('beginConversationButton');
const speakerIndicator = document.getElementById('speakerIndicator');

// Variables for file handling
let currentFileHandle;
let filesMap = new Map();
let currentFilePath = '';

// Variables for speech recognition
let recognition;
let timeoutId;
let isSpeaking = false;
let finalTranscript = '';
let isFirstResult = true;

// Check if speech recognition is supported
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
} else {
    alert('Speech recognition not supported in this browser.');
}

// Awaiting reply messages
const awaitingReplyMessages = [
    "Pondering the mysteries of the universe...",
    "Consulting with the AI elders...",
    "Searching for the meaning of life...",
    "Decoding the matrix...",
    "Calculating the answer to life, the universe, and everything...",
    "Asking the magic 8-ball...",
    "Summoning the spirits of Silicon Valley...",
    "Analyzing the collective consciousness...",
    "Consulting the ancient scrolls of machine learning...",
    "Channeling the wisdom of tech gurus..."
];

// Function to update the speaker indicator
function updateSpeakerIndicator(speaker) {
    if (speaker === "Awaiting reply") {
        const randomMessage = awaitingReplyMessages[Math.floor(Math.random() * awaitingReplyMessages.length)];
        speakerIndicator.textContent = randomMessage;
        speakerIndicator.className = "awaiting-reply";
    } else {
        speakerIndicator.textContent = speaker + " speaking";
        speakerIndicator.className = speaker.toLowerCase().replace(' ', '-') + "-speaking";
    }
}

// Function to display selected files
function displayFiles(files) {
    fileListDiv.innerHTML = '<h2>Files:</h2>';
    Array.from(files).forEach(file => {
        const fileButton = document.createElement('button');
        const relativePath = file.webkitRelativePath || file.name;
        fileButton.textContent = relativePath;
        fileButton.addEventListener('click', () => openFile(file, relativePath));
        fileListDiv.appendChild(fileButton);
        filesMap.set(relativePath, file);
    });
}

// Function to open and read a file
function openFile(file, relativePath) {
    currentFileHandle = file;
    currentFilePath = relativePath;
    const reader = new FileReader();
    reader.onload = function(e) {
        editor.value = e.target.result;
    };
    reader.readAsText(file);
}

// Event listener for folder selection
folderInput.addEventListener('change', () => {
    const files = folderInput.files;
    if (files.length > 0) {
        displayFiles(files);
    } else {
        alert('No folder selected.');
    }
});

// Modified Event Listener for the Upload Button
uploadFolderButton.addEventListener('click', () => {
    const files = folderInput.files;
    if (files.length > 0) {
        // Create a FormData object to send files via POST
        const formData = new FormData();
        Array.from(files).forEach(file => {
            // Include the full relative path in the form data
            formData.append('files[]', file, file.webkitRelativePath || file.name);
        });

        // Send files to the server
        fetch('/upload_folder', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            return response.json().then(data => ({
                status: response.status,
                ok: response.ok,
                body: data
            }));
        })
        .then(({ status, ok, body }) => {
            if (ok) {
                messageDiv.innerText = body.message || 'Upload complete.';
                // Start indexing process
                startIndexing();
            } else {
                messageDiv.innerText = body.error || 'Failed to upload folder.';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            messageDiv.innerText = 'An error occurred during upload.';
        });
    } else {
        alert('No folder selected.');
    }
});

// Function to start indexing process
function startIndexing() {
    uploadFolderButton.disabled = true;
    messageDiv.innerText += '\nIndexing started...';
    fetch('/start_indexing', {
        method: 'POST'
    })
    .then(response => {
        return response.json().then(data => ({
            status: response.status,
            ok: response.ok,
            body: data
        }));
    })
    .then(({ status, ok, body }) => {
        uploadFolderButton.disabled = false;
        if (ok) {
            messageDiv.innerText += '\n' + (body.message || 'Indexing complete.');
        } else {
            messageDiv.innerText += '\n' + (body.error || 'Failed to index files.');
        }
    })
    .catch(error => {
        uploadFolderButton.disabled = false;
        console.error('Error:', error);
        messageDiv.innerText += '\nAn error occurred during indexing.';
    });
}

// Event listener for the save button
saveButton.addEventListener('click', () => {
    if (currentFilePath === '') {
        alert('No file selected.');
        return;
    }
    const content = editor.value;
    // Send the updated content to the server
    fetch('/save_file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'file_path': currentFilePath, 'content': content })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert('File saved successfully.');
        } else if (data.error) {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while saving the file.');
    });
});

// Event listener for the send button in chat
sendButton.addEventListener('click', () => {
    const question = chatInput.value.trim();
    if (question !== '') {
        // Display user's message
        displayMessage(question, 'user-message');
        chatInput.value = '';
        // Send question to the server
        fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 'question': question })
        })
        .then(response => response.json())
        .then(data => {
            if (data.answer) {
                // Display assistant's response
                displayMessage(data.answer, 'assistant-message');
            } else if (data.error) {
                displayMessage('Error: ' + data.error, 'assistant-message');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            displayMessage('An error occurred while getting the answer.', 'assistant-message');
        });
    }
});

// Optional: Allow sending messages with Enter key in chat
chatInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        sendButton.click();
        event.preventDefault();
    }
});

// Function to display messages in the chat window
function displayMessage(message, className) {
    const messageDiv = document.createElement('div');
    messageDiv.className = className;
    messageDiv.textContent = message;
    chatWindow.appendChild(messageDiv);
    // Scroll to the bottom of the chat window
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Event listener for the begin conversation button (speech recognition)
beginConversationButton.addEventListener('click', () => {
    beginConversationButton.style.display = 'none';
    startConversation();
});

// Function to start the speech recognition conversation
function startConversation() {
    recognition.start();
    finalTranscript = '';
    isSpeaking = true;
    isFirstResult = true;
    updateSpeakerIndicator("User");
}

// Function to stop speaking and send the query
function stopSpeakingAndSend() {
    recognition.stop();
    isSpeaking = false;
    updateSpeakerIndicator("Awaiting reply");

    const question = finalTranscript.trim();

    // Display the user's question in the chat window
    displayMessage(question, 'user-message');

    // Send the question to the server
    fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'question': question })
    })
    .then(response => response.json())
    .then(data => {
        if (data.answer) {
            // Update speaker indicator
            updateSpeakerIndicator("Assistant");

            // Display the assistant's response
            displayMessage(data.answer, 'assistant-message');

            // Use speech synthesis to read the response aloud
            const utterance = new SpeechSynthesisUtterance(data.answer);
            speechSynthesis.speak(utterance);

            // Restart conversation after speaking
            utterance.onend = () => {
                updateSpeakerIndicator("User");
                recognition.start();
                isSpeaking = true;
                finalTranscript = '';
            };
        } else if (data.error) {
            displayMessage('Error: ' + data.error, 'assistant-message');
            updateSpeakerIndicator("User");
            recognition.start();
            isSpeaking = true;
            finalTranscript = '';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        displayMessage('An error occurred while getting the answer.', 'assistant-message');
        updateSpeakerIndicator("User");
        recognition.start();
        isSpeaking = true;
        finalTranscript = '';
    });
}

// Speech recognition event handlers
recognition.onresult = function (event) {
    clearTimeout(timeoutId);

    let interimTranscript = '';

    for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
            finalTranscript += transcript;
        } else {
            interimTranscript += transcript;
        }
    }

    // Optionally, display interim results somewhere
    // For simplicity, we're not displaying interim transcripts here

    if (isSpeaking) {
        timeoutId = setTimeout(() => {
            if (interimTranscript.trim() === '') {
                stopSpeakingAndSend();
            }
        }, 1000);
    }

    isFirstResult = false;
};

recognition.onend = function () {
    if (isSpeaking && !isFirstResult) {
        recognition.start();
    }
};

recognition.onerror = function(event) {
    console.error('Speech recognition error detected: ' + event.error);
    updateSpeakerIndicator("Error");
    recognition.stop();
};
