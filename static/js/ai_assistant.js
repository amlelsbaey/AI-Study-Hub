document.addEventListener("DOMContentLoaded", function () {
    const messagesContainer = document.getElementById("aiMessages");
    const messageForm = document.querySelector(".ai-message-form");
    const messageInput = document.getElementById("aiMessageInput");
    const sendButton = document.querySelector(".ai-send-btn");

    function scrollToBottom() {
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }

    function setupCopyButtons() {
        const copyButtons = document.querySelectorAll(".copy-message-btn");

        copyButtons.forEach(function (button) {
            if (button.dataset.copyReady) {
                return;
            }

            button.dataset.copyReady = "true";

            button.addEventListener("click", async function () {
                const messageWrapper = button.closest(".message-wrapper");

                if (!messageWrapper) {
                    return;
                }

                const messageContent =
                    messageWrapper.querySelector(".message-content");

                if (!messageContent) {
                    return;
                }

                const text = messageContent.innerText.trim();

                try {
                    await navigator.clipboard.writeText(text);

                    button.textContent = "Copied!";

                    setTimeout(function () {
                        button.textContent = "Copy";
                    }, 1500);
                } catch (error) {
                    console.error("Copy failed:", error);
                }
            });
        });
    }

    function getUserInitial() {
        const avatar = document.querySelector(".user-avatar");

        if (avatar && avatar.textContent.trim()) {
            return avatar.textContent.trim();
        }

        return "U";
    }

    function createUserMessage(content) {
        const userMessage = document.createElement("div");

        userMessage.className = "ai-message user-message";

        userMessage.innerHTML = `
            <div class="message-content"></div>
            <div class="message-avatar user-avatar">
                ${getUserInitial()}
            </div>
        `;

        userMessage.querySelector(".message-content").textContent = content;

        return userMessage;
    }

    function createLoadingMessage() {
        const loadingMessage = document.createElement("div");

        loadingMessage.className =
            "ai-message assistant-message ai-loading-message";

        loadingMessage.innerHTML = `
            <div class="message-avatar assistant-avatar">
                ✦
            </div>

            <div class="message-content ai-typing">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;

        return loadingMessage;
    }

    function createAssistantMessage(content) {
        const assistantMessage = document.createElement("div");

        assistantMessage.className =
            "ai-message assistant-message";

        assistantMessage.innerHTML = `
            <div class="message-avatar assistant-avatar">
                ✦
            </div>

            <div class="message-wrapper">
                <div class="message-content"></div>

                <button
                    type="button"
                    class="copy-message-btn"
                    title="Copy response">
                    Copy
                </button>
            </div>
        `;

        assistantMessage.querySelector(".message-content").textContent =
            content;

        return assistantMessage;
    }

    function createErrorMessage() {
        const errorMessage = document.createElement("div");

        errorMessage.className =
            "ai-message assistant-message";

        errorMessage.innerHTML = `
            <div class="message-avatar assistant-avatar">
                ✦
            </div>

            <div class="message-content">
                Sorry, something went wrong.
                Please try again.
            </div>
        `;

        return errorMessage;
    }

    function prepareFormData(content) {
        const formData = new FormData();

        formData.append("content", content);

        const csrfToken = messageForm.querySelector(
            'input[name="csrfmiddlewaretoken"]'
        );

        if (csrfToken) {
            formData.append(
                "csrfmiddlewaretoken",
                csrfToken.value
            );
        }

        return formData;
    }

    async function sendMessage() {
        if (!messageForm || !messageInput || !sendButton) {
            return;
        }

        const content = messageInput.value.trim();

        if (!content || sendButton.disabled) {
            return;
        }

        sendButton.disabled = true;
        sendButton.style.opacity = "0.6";
        sendButton.style.cursor = "not-allowed";

        const userMessage = createUserMessage(content);

        messagesContainer.appendChild(userMessage);

        messageInput.value = "";
        messageInput.style.height = "auto";

        scrollToBottom();

        const formData = prepareFormData(content);
        const loadingMessage = createLoadingMessage();

        messagesContainer.appendChild(loadingMessage);

        scrollToBottom();

        try {
            const response = await fetch(
                messageForm.action,
                {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                }
            );

            const data = await response.json();

            loadingMessage.remove();

            if (!response.ok || !data.success) {
                throw new Error(
                    data.error || "Something went wrong."
                );
            }

            const assistantMessage =
                createAssistantMessage(data.ai_message);

            messagesContainer.appendChild(assistantMessage);

            setupCopyButtons();
            scrollToBottom();

            const chatTitle =
                document.querySelector(".ai-chat-title h2");

            if (chatTitle && data.conversation_title) {
                chatTitle.textContent =
                    data.conversation_title;
            }
        } catch (error) {
            console.error("AI Assistant Error:", error);

            loadingMessage.remove();

            messagesContainer.appendChild(
                createErrorMessage()
            );

            scrollToBottom();
        } finally {
            sendButton.disabled = false;
            sendButton.style.opacity = "1";
            sendButton.style.cursor = "pointer";
        }
    }

    function setupMessageInput() {
        if (!messageInput) {
            return;
        }

        messageInput.addEventListener("keydown", function (event) {
            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {
                event.preventDefault();

                sendMessage();
            }
        });

        messageInput.addEventListener("input", function () {
            this.style.height = "auto";

            this.style.height =
                Math.min(this.scrollHeight, 120) + "px";
        });
    }

    function setupSuggestionButtons() {
        const suggestionButtons =
            document.querySelectorAll(
                ".ai-suggestions button"
            );

        suggestionButtons.forEach(function (button) {
            button.addEventListener("click", function () {
                if (!messageInput) {
                    return;
                }

                messageInput.value =
                    this.textContent.trim();

                messageInput.focus();

                messageInput.dispatchEvent(
                    new Event("input")
                );
            });
        });
    }

    if (messageForm) {
        messageForm.addEventListener("submit", function (event) {
            event.preventDefault();
            sendMessage();
        });
    }

    scrollToBottom();
    setupCopyButtons();
    setupMessageInput();
    setupSuggestionButtons();
});
س
