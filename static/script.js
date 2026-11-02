
const messages = document.getElementById("messages");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const newChatBtn = document.getElementById("newChatBtn");

let conversationId = null;

function addMessage(text, sender) {
    const welcome = messages.querySelector(".welcome");
    if (welcome) welcome.remove();

    const message = document.createElement("div");
    message.className = `message ${sender}`;
    message.textContent = text;

    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;

    return message;
}

async function createNewChat() {
    try {
        const response = await fetch("/api/new-chat", {
            method: "POST"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Could not create a new chat.");
        }

        conversationId = data.conversation_id;
        messages.innerHTML = `
            <div class="welcome">
                <h2>Hello! 👋</h2>
                <p>How can I help you today?</p>
            </div>
        `;
        messageInput.focus();

    } catch (error) {
        addMessage(error.message, "bot");
    }
}

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = messageInput.value.trim();

    if (!message) return;

    if (!conversationId) {
        await createNewChat();
        if (!conversationId) return;
    }

    addMessage(message, "user");
    messageInput.value = "";

    sendBtn.disabled = true;
    sendBtn.textContent = "Sending...";

    const loadingMessage = addMessage("Thinking...", "bot");

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                conversation_id: conversationId,
                message: message
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Chat request failed.");
        }

        loadingMessage.textContent = data.reply;

    } catch (error) {
        loadingMessage.textContent = "Error: " + error.message;

    } finally {
        sendBtn.disabled = false;
        sendBtn.textContent = "Send";
        messageInput.focus();
    }
});

newChatBtn.addEventListener("click", createNewChat);

// Create the first conversation when the page loads.
createNewChat();
