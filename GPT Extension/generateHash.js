const crypto = require('crypto');

// Replace the following string with the content of your popup.js file
const popupJsContent = `
document.addEventListener('DOMContentLoaded', function() {
    const searchBtn = document.getElementById('searchBtn');
    searchBtn.addEventListener('click', sendSearch);
  
    function sendSearch() {
      const searchInput = document.getElementById('searchInput');
      const searchQuery = searchInput.value;
  
      if (searchQuery.trim() !== '') {
        const apiUrl = 'https://jsonplaceholder.typicode.com/posts'; // Replace with your API endpoint
  
        fetch(apiUrl, {
          method: 'POST',
          body: JSON.stringify({ query: searchQuery }),
          headers: {
            'Content-Type': 'application/json'
          }
        })
        .then(response => response.json())
        .then(data => {
          displayResponse(data);
        })
        .catch(error => {
          displayResponse({ error: 'Error fetching data. Please try again.' });
        });
  
        searchInput.value = '';
      }
    }
  
    function displayResponse(data) {
      const responseDiv = document.getElementById('response');
      responseDiv.innerHTML = '<h3>API Response:</h3>';
      
      if (data.error) {
        responseDiv.innerHTML += \`<p>\${data.error}</p>\`;
      } else {
        responseDiv.innerHTML += \`<pre>\${JSON.stringify(data, null, 2)}</pre>\`;
      }
    }
});
`;

function generateHash(input) {
  const hash = crypto.createHash('sha256');
  hash.update(input);
  return hash.digest('hex');
}

const hash = generateHash(popupJsContent);
console.log('Generated Hash:', hash);
