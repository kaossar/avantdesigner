const fetch = require('node-fetch'); // Needs node-fetch if not in node 18+, but next.js might have global fetch? Node test script might need it. 
// actually node 18+ has fetch.

async function testApi() {
    console.log("Testing API Reachability...");
    try {
        const response = await fetch('http://localhost:3000/api/analyze', {
            method: 'POST',
        });

        console.log(`Response Status: ${response.status}`);
        const data = await response.json();
        console.log('Response Body:', data);

        if (response.status === 400 && data.error === 'No file provided') {
            console.log("✅ API is responding correctly to missing file.");
        } else {
            console.log("❌ API response unexpected.");
        }

    } catch (e) {
        console.error("❌ API Request Failed:", e.message);
        console.log("Make sure the dev server is running (npm run dev).");
    }
}

testApi();
