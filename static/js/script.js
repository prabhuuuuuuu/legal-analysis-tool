document.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const crimeDescription = document.getElementById('crimeDescription');
    const resultCard = document.getElementById('resultCard');
    const resultContent = document.getElementById('resultContent');
    const loadingSpinner = document.getElementById('loadingSpinner');

    analyzeBtn.addEventListener('click', function() {
        const userInput = crimeDescription.value.trim();
        
        if (!userInput) {
            alert('Please describe the crime before analyzing.');
            return;
        }

        // Show loading spinner and hide result content
        resultCard.style.display = 'block';
        resultContent.style.display = 'none';
        loadingSpinner.style.display = 'block';

        // Send request to backend
        fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ crime_description: userInput }),
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error || 'Something went wrong. Please try again.');
                });
            }
            return response.json();
        })
        .then(data => {
            loadingSpinner.style.display = 'none';
            resultContent.style.display = 'block';
            resultContent.classList.add('fade-in');

            if (data.error) {
                resultContent.innerHTML = `<div class="alert alert-danger">Error: ${data.error}</div>`;
            } else {
                const formattedResult = formatLegalResponse(data.result);
                resultContent.innerHTML = formattedResult;
            }

            // Smooth scroll to the result section
            resultCard.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            loadingSpinner.style.display = 'none';
            resultContent.style.display = 'block';
            resultContent.classList.add('fade-in');
            resultContent.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        });
    });

    function formatLegalResponse(text) {
        const sections = text.split(/(?=\b(?:Constitutional Law|IPC Sections|Steps to Take|Legal Advice)s?:)/i);
        let formattedHtml = '';

        sections.forEach(section => {
            if (section.trim()) {
                const titleMatch = section.match(/^([\w\s]+):/i);
                if (titleMatch) {
                    const title = titleMatch[0];
                    const content = section.substring(title.length).trim();
                    formattedHtml += `<div class="mb-4">
                        <h4 class="text-primary">${title}</h4>
                        <div class="pl-3">${content.replace(/\n/g, '<br>')}</div>
                    </div>`;
                } else {
                    formattedHtml += `<div class="mb-4">${section.replace(/\n/g, '<br>')}</div>`;
                }
            }
        });

        return formattedHtml;
    }
});