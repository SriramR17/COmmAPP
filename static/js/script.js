document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const nextButton = form.querySelector('.next-btn');
    const inputs = form.querySelectorAll('input[type="radio"], input[type="checkbox"]');

    // Check the current selection on load
    const checkSelection = () => {
        const isSelected = Array.from(inputs).some(input => input.checked);
        nextButton.disabled = !isSelected;
    };

    // Add event listeners to inputs
    inputs.forEach(input => {
        input.addEventListener('change', checkSelection);
    });

    // Highlight selected option (for better UI feedback)
    const highlightSelected = () => {
        inputs.forEach(input => {
            const label = input.nextElementSibling; // Assuming label follows input
            if (label) {
                if (input.checked) {
                    label.classList.add('selected');
                } else {
                    label.classList.remove('selected');
                }
            }
        });
    };

    // Add event listeners for highlighting
    inputs.forEach(input => {
        input.addEventListener('change', highlightSelected);
    });

    // Initial checks on page load
    checkSelection();
    highlightSelected();

    // Prevent accidental form submission (optional for debugging)
    form.addEventListener('submit', (e) => {
        if (nextButton.disabled) {
            e.preventDefault();
            alert("Please select an option before proceeding!");
        }
    });
});
