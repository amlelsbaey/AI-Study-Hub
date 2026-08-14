document.addEventListener("DOMContentLoaded", function () {

    const messagesContainer =
        document.getElementById("aiMessages");

    const messageForm =
        document.querySelector(".ai-message-form");

    const messageInput =
        document.getElementById("aiMessageInput");

    const sendButton =
        document.querySelector(".ai-send-btn");


    // =========================
    // Scroll To Bottom
    // =========================

    function scrollToBottom() {

        if (messagesContainer) {

            messagesContainer.scrollTop =
                messagesContainer.scrollHeight;

        }

    }


    scrollToBottom();


    // =========================
    // Copy Messages
    // =========================

    function setupCopyButtons() {

        const copyButtons =
            document.querySelectorAll(
                ".copy-message-btn"
            );


        copyButtons.forEach(function (button) {

            if (button.dataset.copyReady) {
                return;
            }


            button.dataset.copyReady = "true";


            button.addEventListener(
                "click",
                async function () {

                    const messageWrapper =
                        button.closest(
                            ".message-wrapper"
                        );


                    if (!messageWrapper) {
                        return;
                    }


                    const messageContent =
                        messageWrapper.querySelector(
                            ".message-content"
                        );


                    if (!messageContent) {
                        return;
                    }


                    const text =
                        messageContent.innerText.trim();


                    try {

                        await navigator.clipboard.writeText(
                            text
                        );


                        button.textContent =
                            "Copied!";


                        setTimeout(function () {

                            button.textContent =
                                "Copy";

                        }, 1500);


                    } catch (error) {

                        console.error(
                            "Copy failed:",
                            error
                        );

                    }

                }
            );

        });

    }


    setupCopyButtons();


    // =========================
    // Send Message
    // =========================

    if (messageForm) {

        messageForm.addEventListener(
            "submit",
            async function (event) {

                event.preventDefault();


                const content =
                    messageInput.value.trim();


                if (!content) {
                    return;
                }


                // =========================
                // Prevent Double Submit
                // =========================

                if (sendButton.disabled) {
                    return;
                }


                sendButton.disabled = true;

                sendButton.style.opacity = "0.6";

                sendButton.style.cursor =
                    "not-allowed";


                // =========================
                // Show User Message
                // =========================

                const userMessage =
                    document.createElement("div");


                userMessage.className =
                    "ai-message user-message";


                userMessage.innerHTML = `
                    <div class="message-content"></div>

                    <div class="message-avatar user-avatar">
                        ${getUserInitial()}
                    </div>
                `;


                userMessage.querySelector(
                    ".message-content"
                ).textContent = content;


                messagesContainer.appendChild(
                    userMessage
                );


                // =========================
                // Clear Input
                // =========================

                messageInput.value = "";

                messageInput.style.height =
                    "auto";


                scrollToBottom();


                // =========================
                // Prepare Request
                // =========================

                const formData =
                    new FormData(messageForm);


                // =========================
                // AI Loading Indicator
                // =========================

                const loadingMessage =
                    document.createElement("div");


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


                messagesContainer.appendChild(
                    loadingMessage
                );


                scrollToBottom();


                try {

                    // =========================
                    // Send Request
                    // =========================

                    const response =
                        await fetch(
                            messageForm.action,
                            {
                                method: "POST",

                                body: formData,

                                headers: {
                                    "X-Requested-With":
                                        "XMLHttpRequest"
                                }
                            }
                        );


                    const data =
                        await response.json();


                    // =========================
                    // Remove Loading
                    // =========================

                    loadingMessage.remove();


                    // =========================
                    // Check Response
                    // =========================

                    if (
                        !response.ok ||
                        !data.success
                    ) {

                        throw new Error(
                            data.error ||
                            "Something went wrong."
                        );

                    }


                    // =========================
                    // Show AI Response
                    // =========================

                    const assistantMessage =
                        document.createElement("div");


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


                    assistantMessage.querySelector(
                        ".message-content"
                    ).textContent =
                        data.ai_message;


                    messagesContainer.appendChild(
                        assistantMessage
                    );


                    // =========================
                    // Setup Copy Button
                    // =========================

                    setupCopyButtons();


                    scrollToBottom();


                    // =========================
                    // Update Conversation Title
                    // =========================

                    const chatTitle =
                        document.querySelector(
                            ".ai-chat-title h2"
                        );


                    if (
                        chatTitle &&
                        data.conversation_title
                    ) {

                        chatTitle.textContent =
                            data.conversation_title;

                    }


                } catch (error) {

                    console.error(
                        "AI Assistant Error:",
                        error
                    );


                    // =========================
                    // Remove Loading
                    // =========================

                    if (loadingMessage) {
                        loadingMessage.remove();
                    }


                    // =========================
                    // Show Error Message
                    // =========================

                    const errorMessage =
                        document.createElement("div");


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


                    messagesContainer.appendChild(
                        errorMessage
                    );


                    scrollToBottom();

                }


                // =========================
                // Enable Send Again
                // =========================

                sendButton.disabled = false;

                sendButton.style.opacity = "1";

                sendButton.style.cursor =
                    "pointer";

            }
        );

    }


    // =========================
    // User Initial
    // =========================

    function getUserInitial() {

        const avatar =
            document.querySelector(".user-avatar");


        if (
            avatar &&
            avatar.textContent.trim()
        ) {

            return avatar.textContent.trim();

        }


        return "U";

    }


    // =========================
    // Enter To Send
    // =========================

    if (messageInput) {

        messageInput.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key === "Enter" &&
                    !event.shiftKey
                ) {

                    event.preventDefault();


                    if (messageForm) {

                        messageForm.requestSubmit();

                    }

                }

            }
        );


        // =========================
        // Auto Resize Textarea
        // =========================

        messageInput.addEventListener(
            "input",
            function () {

                this.style.height =
                    "auto";


                this.style.height =
                    Math.min(
                        this.scrollHeight,
                        120
                    ) + "px";

            }
        );

    }


    // =========================
    // Suggestion Buttons
    // =========================

    const suggestionButtons =
        document.querySelectorAll(
            ".ai-suggestions button"
        );


    suggestionButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    if (!messageInput) {
                        return;
                    }


                    messageInput.value =
                        this.textContent.trim();


                    messageInput.focus();


                    messageInput.dispatchEvent(
                        new Event("input")
                    );

                }
            );

        }
    );

});