//This file pretty much works

function send_the_url(url) {
    //   // Example of an API call with the URL
    const apiUrl = 'https://jsonplaceholder.typicode.com/posts';
  
    fetch(apiUrl, {
      method: 'POST', // or 'GET', depending on your API
      body: JSON.stringify({ url: url }), // send URL as part of the request body or as query parameters
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => console.log('API response:', data))
      .catch(error => console.error('API call error:', error));
  }

function send_the_asin(url) 
{
    //   // Example of an API call with the URL
    const apiUrl = 'https://jsonplaceholder.typicode.com/posts';
  
    fetch(apiUrl, {
      method: 'POST', // or 'GET', depending on your API
      body: JSON.stringify({ url: url }), // send URL as part of the request body or as query parameters
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => console.log('API response:', data))
      .catch(error => console.error('API call error:', error));
}

  
function getASINFromAmazonURL(url)  
//Only thing I'm not sure about is if the match[1] works as intended but I think it does
{
    const regex = /\/dp\/([A-Z0-9]{10})/;
    const match = url.match(regex);
    if (match && match[1]) 
    {
        return match[1];
    }
    return null;
}

  console.log("Hello, World!");
  chrome.tabs.onActivated.addListener(function (activeInfo) {
    chrome.tabs.get(activeInfo.tabId, function (tab) {
      if (tab.url.includes('amazon.com') && tab.url.includes('/dp/')) {
        console.log('Amazon page detected:', tab.url);
        // Call your API here
        const asin = getASINFromAmazonURL(tab.url);
        console.log(asin);
        send_the_asin(asin);
        send_the_url(tab.url);
      }  
      console.log("Current Tab URL:", tab.url);
    });
  });