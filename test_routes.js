const fetch = require('node-fetch');
const fs = require('fs');
const FormData = require('form-data');
const path = require('path');

async function testRoutes() {
    console.log("--- Testing /api/ping ---");
    try {
        const res = await fetch('http://localhost:3000/api/ping');
        console.log(`Ping Status: ${res.status}`);
        const data = await res.json();
        console.log('Ping Body:', data);
    } catch (e) {
        console.log("Ping Failed:", e.message);
    }

    console.log("\n--- Testing /api/analyze ---");
    // Simple POST with no file to see if we get 400 (Success) or 404 (Fail)
    try {
        const res = await fetch('http://localhost:3000/api/analyze', { method: 'POST' });
        console.log(`Analyze Status: ${res.status}`);
        const data = await res.json();
        console.log('Analyze Body:', data);
    } catch (e) {
        console.log("Analyze Failed:", e.message);
    }
}

// Wait for server restart
setTimeout(testRoutes, 3000);
