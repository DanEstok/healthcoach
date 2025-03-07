// Health Coach - Main JavaScript

// DOM Elements
const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const chatList = document.getElementById('chat-list');

// Chat History Management
let currentChatId = null;
let chats = JSON.parse(localStorage.getItem('healthcoach_chats') || '{}');

// Initialize the app
function initApp() {
    console.log('Initializing app...');
    
    // Add event listener for Enter key
    if (userInput) {
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        console.log('Added keypress event listener');
    } else {
        console.error('User input element not found');
    }
    
    // Add event listener for Send button
    const sendButton = document.getElementById('send-button');
    if (sendButton) {
        sendButton.addEventListener('click', function() {
            sendMessage();
        });
        console.log('Added send button click event listener');
    } else {
        console.error('Send button element not found');
    }
    
    // Load saved chats into sidebar
    loadSavedChats();
    
    // Create a new chat if none exists
    if (Object.keys(chats).length === 0) {
        createNewChat();
    } else {
        // Load the most recent chat
        const mostRecentChatId = getMostRecentChatId();
        loadChat(mostRecentChatId);
    }
    
    // Add welcome message
    if (chatContainer.children.length === 0) {
        addMessage("Hello! I'm your Health Coach. How can I help you with your wellness journey today?", false);
    }
}

// Get the most recent chat ID
function getMostRecentChatId() {
    let mostRecentTime = 0;
    let mostRecentId = null;
    
    for (const chatId in chats) {
        const lastMessageTime = chats[chatId].lastUpdated || 0;
        if (lastMessageTime > mostRecentTime) {
            mostRecentTime = lastMessageTime;
            mostRecentId = chatId;
        }
    }
    
    return mostRecentId;
}

// Create a new chat
function createNewChat() {
    const timestamp = Date.now();
    const chatId = 'chat_' + timestamp;
    
    chats[chatId] = {
        title: 'New Chat',
        messages: [],
        created: timestamp,
        lastUpdated: timestamp
    };
    
    saveChats();
    loadSavedChats();
    loadChat(chatId);
    
    return chatId;
}

// Save chats to localStorage
function saveChats() {
    localStorage.setItem('healthcoach_chats', JSON.stringify(chats));
}

// Load saved chats into sidebar
function loadSavedChats() {
    if (!chatList) return;
    
    chatList.innerHTML = '';
    
    // Sort chats by last updated time (most recent first)
    const sortedChatIds = Object.keys(chats).sort((a, b) => {
        return (chats[b].lastUpdated || 0) - (chats[a].lastUpdated || 0);
    });
    
    sortedChatIds.forEach(chatId => {
        const chat = chats[chatId];
        const chatTitle = chat.title || 'Unnamed Chat';
        
        const li = document.createElement('li');
        li.dataset.chatId = chatId;
        li.innerHTML = `
            <span class="chat-title">${chatTitle}</span>
            <span class="delete-chat">×</span>
        `;
        
        if (chatId === currentChatId) {
            li.classList.add('active');
        }
        
        li.querySelector('.chat-title').addEventListener('click', () => {
            loadChat(chatId);
        });
        
        li.querySelector('.delete-chat').addEventListener('click', (e) => {
            e.stopPropagation();
            deleteChat(chatId);
        });
        
        chatList.appendChild(li);
    });
}

// Load a specific chat
function loadChat(chatId) {
    if (!chats[chatId]) return;
    
    currentChatId = chatId;
    chatContainer.innerHTML = '';
    
    // Update active state in sidebar
    if (chatList) {
        const items = chatList.querySelectorAll('li');
        items.forEach(item => {
            item.classList.remove('active');
            if (item.dataset.chatId === chatId) {
                item.classList.add('active');
            }
        });
    }
    
    // Load messages
    const messages = chats[chatId].messages;
    messages.forEach(msg => {
        addMessage(msg.text, msg.isUser, msg.timestamp, false);
    });
    
    // Update chat title if needed
    updateChatTitle(chatId);
}

// Update chat title based on first user message
function updateChatTitle(chatId) {
    const chat = chats[chatId];
    
    if (chat.title === 'New Chat' && chat.messages.length > 0) {
        // Find first user message
        const firstUserMsg = chat.messages.find(msg => msg.isUser);
        if (firstUserMsg) {
            // Truncate message to create title
            let title = firstUserMsg.text.substring(0, 30);
            if (firstUserMsg.text.length > 30) title += '...';
            chat.title = title;
            saveChats();
            loadSavedChats();
        }
    }
}

// Delete a chat
function deleteChat(chatId) {
    if (confirm('Are you sure you want to delete this chat?')) {
        delete chats[chatId];
        saveChats();
        
        // If we deleted the current chat, load another one or create new
        if (chatId === currentChatId) {
            const remainingChatIds = Object.keys(chats);
            if (remainingChatIds.length > 0) {
                loadChat(remainingChatIds[0]);
            } else {
                createNewChat();
            }
        }
        
        loadSavedChats();
    }
}

// Add a message to the chat
function addMessage(text, isUser, timestamp = Date.now(), save = true) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    // Format the timestamp
    const date = new Date(timestamp);
    const timeStr = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    let messageContent = `<div class="message-content">${text}</div>`;
    
    // Add feedback buttons for bot messages
    if (!isUser) {
        messageContent += `
            <div class="feedback-buttons">
                <button class="feedback-btn" data-value="helpful">👍 Helpful</button>
                <button class="feedback-btn" data-value="not-helpful">👎 Not Helpful</button>
            </div>
        `;
    }
    
    messageContent += `<div class="timestamp">${timeStr}</div>`;
    messageDiv.innerHTML = messageContent;
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    // Add event listeners to feedback buttons
    if (!isUser) {
        const feedbackBtns = messageDiv.querySelectorAll('.feedback-btn');
        feedbackBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const feedback = this.dataset.value;
                provideFeedback(feedback, text);
                
                // Disable all feedback buttons in this message
                feedbackBtns.forEach(b => b.disabled = true);
                
                // Show feedback received message
                const feedbackMsg = document.createElement('div');
                feedbackMsg.className = 'feedback-received';
                feedbackMsg.textContent = 'Thanks for your feedback!';
                this.parentNode.appendChild(feedbackMsg);
            });
        });
    }
    
    // Save message to current chat
    if (save && currentChatId) {
        chats[currentChatId].messages.push({
            text,
            isUser,
            timestamp
        });
        chats[currentChatId].lastUpdated = timestamp;
        saveChats();
        updateChatTitle(currentChatId);
    }
}

// Send a message to the chatbot
function sendMessage() {
    console.log('sendMessage function called');
    const message = userInput.value.trim();
    console.log('User input:', message);
    
    if (!message) {
        console.log('Empty message, not sending');
        return;
    }
    
    // Make sure we have a current chat
    if (!currentChatId) {
        console.log('No current chat, creating new chat');
        currentChatId = createNewChat();
    }
    
    addMessage(message, true);
    userInput.value = '';
    
    // Send to backend
    console.log('Sending message to backend');
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_input=${encodeURIComponent(message)}`
    })
    .then(response => response.json())
    .then(data => {
        console.log('Received response:', data);
        addMessage(data.response, false);
        loadSavedChats(); // Refresh sidebar
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage('Sorry, I encountered an error. Please try again.', false);
    });
}

// Send feedback to the backend
function provideFeedback(feedback, responseText) {
    // Get the last user message for context
    const lastUserMessage = chats[currentChatId].messages.filter(msg => msg.isUser).pop();
    const userQuery = lastUserMessage ? lastUserMessage.text : '';
    
    // Send feedback to backend
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_input=${encodeURIComponent(userQuery)}&feedback=${encodeURIComponent(feedback)}`
    })
    .then(response => response.json())
    .catch(error => {
        console.error('Error sending feedback:', error);
    });
    
    // Store feedback in chat history
    if (currentChatId && chats[currentChatId]) {
        // Find the bot message that received feedback
        const messages = chats[currentChatId].messages;
        for (let i = messages.length - 1; i >= 0; i--) {
            if (!messages[i].isUser && messages[i].text === responseText) {
                messages[i].feedback = feedback;
                break;
            }
        }
        saveChats();
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initApp);