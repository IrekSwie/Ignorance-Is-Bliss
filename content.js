// Function to replace the text in the node
function replaceTextInNode(node, from, to) {
    node.nodeValue = node.nodeValue.replace(from, to);
  }
  
  // Function to fetch data from an API using POST
  async function fetchData(text) {
    const apiUrl = "http://127.0.0.1:5000/analyze2";
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: text }),
    });
  
    if (response.ok) {
      const data = await response.json();
      return data.modifiedText;
    } else {
      console.error("Server responded with status", response.status);
    }
  }
  
  // Main function to scan and replace text
  async function main() {
    // Get the main content section by its ID
    const mainContent = document.getElementById('mw-content-text');
    if (!mainContent) {
      console.log("Not a Wikipedia page or main content not found.");
      return;
    }
  
    // Search recursively within mainContent for text nodes
    const nodes = [];
    const walk = document.createTreeWalker(mainContent, NodeFilter.SHOW_TEXT, null, false);
    while (walk.nextNode()) nodes.push(walk.currentNode);
  
    // Process each text node
    for (const node of nodes) {
      const text = node.nodeValue;
      if (text.trim().length === 0) continue;  // Skip empty text nodes
      
      const chunkSize = 512;
      let newText = "";
  
      for (let start = 0; start < text.length; start += chunkSize) {
        const end = Math.min(start + chunkSize, text.length);
        const textChunk = text.slice(start, end);
        const modifiedChunk = await fetchData(textChunk);
        newText += modifiedChunk;
      }
  
      replaceTextInNode(node, text, newText);
    }
  }
  
  // Execute the main function
  main().catch(err => console.error(err));
  