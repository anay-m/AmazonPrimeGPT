document.addEventListener('DOMContentLoaded', function () {
    const searchButton = document.getElementById('searchButton');
    if (searchButton) {
        searchButton.addEventListener('click', sendSearch);
    }
    
});

function sendSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchQuery = searchInput.value;
    var ans = 'You: ' + searchQuery;
    if (searchQuery.trim() !== '') {
        const apiUrl = 'https://jsonplaceholder.typicode.com/posts';

        fetch(apiUrl, {
            method: 'POST',
            body: JSON.stringify({ query: ans }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            displayResponse(data);
            document.getElementById('response').style.display = 'block';
        })
        .catch(error => {
            displayResponse({ error: 'Error fetching data. Please try again.' });
            document.getElementById('response').style.display = 'block';
        });

        searchInput.value = '';
    }
}

function displayResponse(data) {
    const responseDiv = document.getElementById('response');

    if (data.error) {
        responseDiv.innerHTML += `<p>${data.error}</p>`;
    } 
    else {
        responseDiv.innerHTML += `<pre>${data.query}</pre>`;
        //Once I have the API response, I put the next part in here 
    }
}
