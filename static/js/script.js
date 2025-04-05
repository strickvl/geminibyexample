/**
 * Gemini by Example JavaScript functionality
 */

// Function to copy code to clipboard
function copyCode(button) {
    const codeBlock = button.closest('.code').querySelector('pre');
    const code = codeBlock.textContent;
    
    navigator.clipboard.writeText(code).then(() => {
        // Show "Copied!" tooltip
        const tooltip = document.createElement('span');
        tooltip.textContent = 'Copied!';
        tooltip.className = 'tooltip';
        button.parentElement.appendChild(tooltip);
        
        // Remove tooltip after 1 second
        setTimeout(() => tooltip.remove(), 1000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
}

// Enable keyboard navigation between examples
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey || e.altKey || e.shiftKey || e.metaKey) {
        return;
    }
    
    if (e.key === 'ArrowRight') {
        const nextLink = document.querySelector('.next a');
        if (nextLink) {
            window.location.href = nextLink.getAttribute('href');
        }
    }
    
    if (e.key === 'ArrowLeft') {
        const prevLink = document.querySelector('.prev a');
        if (prevLink) {
            window.location.href = prevLink.getAttribute('href');
        }
    }
}); 
