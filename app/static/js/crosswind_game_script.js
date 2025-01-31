document.addEventListener("DOMContentLoaded", () => {
    const choiceButtons = document.querySelectorAll(".choice");
    const choiceInput = document.getElementById("choice");
    const crosswindInput = document.getElementById("crosswind-slider");
    const submitBtn = document.getElementById("submit-btn");
    const crosswindValueDisplay = document.getElementById("crosswind-value");

    // Handle choice button selection
    choiceButtons.forEach(button => {
        button.addEventListener("click", () => {
            choiceInput.value = button.dataset.choice; // Update the hidden input with the user's choice
            choiceButtons.forEach(btn => btn.classList.remove("selected"));
            button.classList.add("selected");
            checkInputs();
        });
    });

    // Update crosswind value display on slider input
    crosswindInput.addEventListener("input", () => {
        updateCrosswindValue(crosswindInput.value); // Update the displayed value dynamically
        updateSliderStyle(crosswindInput); // Update the slider's gradient color
        checkInputs(); // Check inputs to enable/disable Submit button
    });

    // Add touch event listeners for better touch screen support
    crosswindInput.addEventListener("touchstart", handleTouch);
    crosswindInput.addEventListener("touchmove", handleTouch);
    crosswindInput.addEventListener("touchend", handleTouch);

    // Initialize the slider gradient and value display
    updateSliderStyle(crosswindInput); // Initialize the slider gradient and value display
});

    // Function to enable/disable the Submit button
    function checkInputs() {
        const choiceInput = document.getElementById("choice");
        const crosswindInput = document.getElementById("crosswind-slider");
        const submitBtn = document.getElementById("submit-btn");

        if (choiceInput.value && crosswindInput.value) {
            submitBtn.disabled = false;
        } else {
            submitBtn.disabled = true;
        }
    }

    // Function to update the crosswind value display in #.# format
    function updateCrosswindValue(value) {
        const formattedValue = parseFloat(value).toFixed(1); // Format to one decimal place
        const crosswindValueDisplay = document.getElementById("crosswind-value");
        crosswindValueDisplay.textContent = formattedValue; // Update the displayed value
    }

    // Function to update the slider's gradient color
    function updateSliderStyle(slider) {
        const value = parseFloat(slider.value); // Get the slider value
        const max = parseFloat(slider.max); // Get the slider max value
        const percentage = (value / max) * 100; // Calculate percentage position

        // Generate gradient color based on the value
        const color = generateGradientColor(value, max);

        // Update the slider's background gradient
        slider.style.background = `linear-gradient(90deg, ${color} ${percentage}%, gray ${percentage}%)`;

        // Update the displayed value
        const crosswindValueDisplay = document.getElementById("crosswind-value");
        crosswindValueDisplay.textContent = value.toFixed(1); // Display value in #.# format
    }

    // Function to generate gradient color based on the slider value
    function generateGradientColor(value, max) {
        const ratio = value / max; // Normalize value between 0 and 1

        // Determine RGB components for the gradient
        let r = 0, g = 0, b = 0;

        if (ratio <= 0.5) {
            // Green to Yellow (0-50%)
            r = Math.round(255 * (ratio / 0.5)); // Increase red
            g = 255; // Full green
        } else {
            // Yellow to Red (50-100%)
            r = 255; // Full red
            g = Math.round(255 * ((1 - ratio) / 0.5)); // Decrease green
        }

        return `rgb(${r}, ${g}, ${b})`; // Return the calculated RGB color
    }

    // Function to handle touch events for the slider
    function handleTouch(event) {
        event.preventDefault(); // Prevent scrolling
        const touch = event.touches[0];
        const rect = crosswindInput.getBoundingClientRect();
        const value = ((touch.clientX - rect.left) / rect.width) * crosswindInput.max;
        crosswindInput.value = Math.min(Math.max(value, 0), crosswindInput.max);
        updateSliderStyle(crosswindInput);
        updateCrosswindValue(crosswindInput.value);
        checkInputs();
    }