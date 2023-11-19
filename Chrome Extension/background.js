//This file pretty much works

function send_the_url_asin(url, asin) {
    //   // Example of an API call with the URL
    const apiUrl = 'https://jsonplaceholder.typicode.com/posts';
    fetch(apiUrl, {
      method: 'POST', // or 'GET', depending on your API
      body: JSON.stringify({ URL: url , ASIN: asin}), // send URL as part of the request body or as query parameters
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => console.log('API response:', data))
      .catch(error => console.error('API call error:', error));
  }

// function send_the_asin(url) 
// {
//     //   // Example of an API call with the URL
//     const apiUrl = 'https://jsonplaceholder.typicode.com/posts';
  
//     fetch(apiUrl, {
//       method: 'POST', // or 'GET', depending on your API
//       body: JSON.stringify({ url: url }), // send URL as part of the request body or as query parameters
//       headers: {
//         'Content-Type': 'application/json'
//       }
//     })
//       .then(response => response.json())
//       .then(data => console.log('API response:', data))
//       .catch(error => console.error('API call error:', error));
// }

  
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'getASIN') {
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            const activeTab = tabs[0];
            if (activeTab.url.includes('amazon.com') && activeTab.url.includes('/dp/')) {
                const asin = getASINFromAmazonURL(activeTab.url);
                sendResponse({ asin: asin });
                send_the_url_asin(activeTab.url, asin);
            }
        });
    }
    return true; // Indicates that sendResponse will be called asynchronously
});


function getASINFromAmazonURL(url) {
    const regex = /\/dp\/([A-Z0-9]{10})/;
    const match = url.match(regex);
    if (match && match[1]) {
        return match[1];
    }
    return null;
}

//   chrome.tabs.onActivated.addListener(function (activeInfo) {
//     chrome.tabs.get(activeInfo.tabId, function (tab) {
//       if (tab.url.includes('amazon.com') && tab.url.includes('/dp/')) {
//         console.log('Amazon page detected:', tab.url);
//         // Call your API here
//         const asin = getASINFromAmazonURL(tab.url);
//         console.log(asin);
//         send_the_url_asin(tab.url, asin);
//       }  
//       console.log("Current Tab URL:", tab.url);
//     });
//   });
