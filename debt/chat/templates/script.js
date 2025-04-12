document.getElementById("send-btn").addEventListener("click", function () {
    const userMessage = document.getElementById("user-input").value.trim();

    if (!userMessage) {
        alert("Please enter a message.");
        return;
    }

    // Add user message to chat box
    const chatBox = document.getElementById("chat-box");
    const userMessageElement = document.createElement("div");
    userMessageElement.className = "user-message";
    userMessageElement.textContent = userMessage;
    chatBox.appendChild(userMessageElement);

    // Clear the input field
    document.getElementById("user-input").value = "";

    // Show loading spinner
    document.getElementById("loading").style.display = "block";

    // Simulate sending message to the server
    fetch("/api/chat/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage }),
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading spinner
        document.getElementById("loading").style.display = "none";

        // Add bot's response to the chat box
        const botMessageElement = document.createElement("div");
        botMessageElement.className = "bot-message";
        botMessageElement.textContent = data.response || "Sorry, something went wrong!";
        chatBox.appendChild(botMessageElement);

        // Scroll to bottom of chat box
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        document.getElementById("loading").style.display = "none";
        alert("Error: Unable to connect to the server.");
    });
});

// Login/Signup Button Functionality
document.getElementById("login-btn").addEventListener("click", function () {
    window.location.href = "/login"; // Redirect to login page
});

document.getElementById("signup-btn").addEventListener("click", function () {
    window.location.href = "/signup"; // Redirect to signup page
});

// Settings button functionality
document.getElementById("settings-btn").addEventListener("click", function () {
    alert("Settings feature coming soon!");
});
