const fetch = require('node-fetch');
const fs = require('fs');
const FormData = require('form-data');
const path = require('path');

// Path to a sample DOCX found in node_modules
const SAMPLE_DOCX_PATH = path.join(__dirname, 'node_modules/mammoth/test/test-data/single-paragraph.docx');

async function testFullExtraction() {
    console.log("Testing Full API Extraction...");

    if (!fs.existsSync(SAMPLE_DOCX_PATH)) {
        console.error("❌ Sample file not found:", SAMPLE_DOCX_PATH);
        return;
    }

    try {
        const formData = new FormData();
        formData.append('file', fs.createReadStream(SAMPLE_DOCX_PATH));

        const response = await fetch('http://localhost:3000/api/analyze', {
            method: 'POST',
            body: formData,
            headers: formData.getHeaders(),
        });

        console.log(`Response Status: ${response.status}`);
        const data = await response.json();

        if (response.ok && data.success) {
            console.log("✅ Analysis Success!");
            console.log("Extracted Text Preview:", data.text.substring(0, 100));
        } else {
            console.error("❌ Analysis Failed:", data);
        }

    } catch (e) {
        console.error("❌ Request Error:", e);
    }
}

// Wait for server to be likely ready
console.log("Waiting for server...");
setTimeout(testFullExtraction, 3000);
