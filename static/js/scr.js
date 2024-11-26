
    // Dynamic Progress Bar and Navigation functionality
    let currentStep = 1;  // Track the current step in the process

    // Function to navigate to a specific page
    function navigateTo(page) {
        window.location.href = page;
        updateProgressBar();
    }

    // Function to navigate to the previous page
    function navigateBack() {
        if (currentStep > 1) {
            currentStep--;
            updateProgressBar();
            window.location.href = `step${currentStep}.html`;  // Assuming sequential step names
        }
    }

    // Function to navigate to the next page
    function navigateNext() {
        if (currentStep < 5) {
            currentStep++;
            updateProgressBar();
            window.location.href = `step${currentStep}.html`;  // Assuming sequential step names
        }
    }

    // Function to update the progress bar
    function updateProgressBar() {
        // Reset progress steps
        for (let i = 1; i <= 5; i++) {
            document.getElementById(`step${i}`).classList.remove('active');
        }

        // Set active steps based on the current step
        for (let i = 1; i <= currentStep; i++) {
            document.getElementById(`step${i}`).classList.add('active');
        }

        // Toggle next/previous buttons visibility
        document.getElementById('nextButton').style.display = currentStep === 5 ? 'none' : 'inline-block';
        document.getElementById('backButton').style.display = currentStep === 1 ? 'none' : 'inline-block';
    }

    // Initialize the page on load
    window.onload = updateProgressBar;

    // Function to enable/disable the "Next" button based on checkbox selection
    function toggleNextButton() {
        const nextButton = document.getElementById('nextButton');
        let isChecked = false;

        // Check if any of the checkboxes or radio buttons are selected
        const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
        const radioButtons = document.querySelectorAll('input[type="radio"]:checked');

        // If any checkbox or radio button is selected, enable the next button
        if (checkboxes.length > 0 || radioButtons.length > 0) {
            isChecked = true;
        }

        nextButton.disabled = !isChecked; // Enable or disable the button
    }

    // Add event listeners to all checkboxes and radio buttons
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', toggleNextButton);
    });

    document.querySelectorAll('input[type="radio"]').forEach(radio => {
        radio.addEventListener('change', toggleNextButton);
    });

    // Initial check to ensure button state is correct if the page is pre-filled
    document.addEventListener('DOMContentLoaded', toggleNextButton);

    // Back button functionality
    function goBack() {
        window.history.back();
    }

    // Tooltip functionality (for displaying information on hover)
    document.querySelectorAll('.tooltip').forEach((tooltip) => {
        tooltip.addEventListener('mouseenter', function() {
            const tooltipText = this.querySelector('.tooltip-text');
            tooltipText.style.visibility = 'visible';
            tooltipText.style.opacity = '1';
        });

        tooltip.addEventListener('mouseleave', function() {
            const tooltipText = this.querySelector('.tooltip-text');
            tooltipText.style.visibility = 'hidden';
            tooltipText.style.opacity = '0';
        });
    });

