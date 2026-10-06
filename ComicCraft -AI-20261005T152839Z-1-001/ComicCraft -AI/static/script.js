document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.getElementById(
                "comicForm"
            );

        const button =
            document.getElementById(
                "generateButton"
            );

        const storyPrompt =
            document.getElementById(
                "storyPrompt"
            );

        const characterName =
            document.getElementById(
                "characterName"
            );

        const promptCount =
            document.getElementById(
                "promptCount"
            );

        const loadingMessage =
            document.getElementById(
                "loadingMessage"
            );


        // Character counter
        if (
            storyPrompt &&
            promptCount
        ) {

            function updateCounter() {

                promptCount.textContent =
                    `${storyPrompt.value.length} / 5000 characters`;

            }

            storyPrompt.addEventListener(
                "input",
                updateCounter
            );

            updateCounter();
        }


        // Form validation
        if (form) {

            form.addEventListener(
                "submit",
                (event) => {

                    if (
                        !storyPrompt.value.trim()
                    ) {

                        event.preventDefault();

                        alert(
                            "Please enter your story prompt."
                        );

                        storyPrompt.focus();

                        return;
                    }


                    if (
                        !characterName.value.trim()
                    ) {

                        event.preventDefault();

                        alert(
                            "Please enter the character name."
                        );

                        characterName.focus();

                        return;
                    }


                    // Loading state
                    button.disabled = true;

                    button.textContent =
                        "Creating Your Comic...";

                    loadingMessage.hidden =
                        false;
                }
            );
        }

    }
);