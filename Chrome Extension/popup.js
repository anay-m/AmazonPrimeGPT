document.addEventListener('DOMContentLoaded', function () {
    const searchButton = document.getElementById('searchButton');
    if (searchButton) {
        searchButton.addEventListener('click', sendSearch);
    }
    
});
let my_questions = [];
let my_answers = [];
//Get rid of you for the query 
function requestASINFromBackground() {
    return new Promise((resolve, reject) => {
        chrome.runtime.sendMessage({ action: 'getASIN' }, function(response) {
            if (response && response.asin) {
                resolve(response); // Resolve the Promise with the response
            } else {
                reject(new Error('No ASIN found')); // Reject the Promise if no ASIN is found
            }
        });
    });
}

function sendSearch() {
    document.getElementById('loader').style.display = 'block';

    requestASINFromBackground()
        .then(response => {
            const searchInput = document.getElementById('searchInput');
            const searchQuery = searchInput.value;

            if (searchQuery.trim() !== '') {
                const ASIN = JSON.stringify({asin : response.asin});
                const apiUrl = 'https://us-east1-gptprime.cloudfunctions.net/langchain';

                fetch(apiUrl, {
                    method: 'POST',
                    body: JSON.stringify({ query: searchQuery, filter: ASIN}),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    displayResponse(data);
                    document.getElementById('response').style.display = 'block';
                    document.getElementById('loader').style.display = 'none';
                })
                .catch(error => {
                    displayResponse({ error: 'Error fetching data. Please try again.' });
                    document.getElementById('response').style.display = 'block';
                    document.getElementById('loader').style.display = 'none';
                });

                searchInput.value = '';
            }
            return response;
        })
        .catch(error => {
            console.error(error);
            document.getElementById('loader').style.display = 'none';
            return null;
        });
}

function displayResponse(data) {
    const responseDiv = document.getElementById('response');
    // console.log(data);
    if (data.error) {
        responseDiv.innerHTML += `<p>${data.error}</p>`;
    } 
    else {
        my_answers.push(data.response);
        console.log('My Answers');
        console.log(my_answers);
        responseDiv.innerHTML += `<pre>'GPT: ' ${data.response}</pre>`;
        //Once I have the API response, I put the next part in here 
    }
}
