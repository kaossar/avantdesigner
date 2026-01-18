import requests
import time

print("Testing direct connection to Python backend...")

# Test 1: Health check
try:
    response = requests.get("http://127.0.0.1:8000/health", timeout=5)
    print(f"✅ Health check: {response.status_code} - {response.json()}")
except Exception as e:
    print(f"❌ Health check failed: {e}")

# Test 2: Upload a tiny test file
try:
    print("\nTesting file upload with streaming...")
    
    # Create a minimal PDF
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Test")
    pdf_bytes = doc.tobytes()
    
    files = {'file': ('test.pdf', pdf_bytes, 'application/pdf')}
    data = {'contract_type': 'auto'}
    
    start = time.time()
    response = requests.post(
        "http://127.0.0.1:8000/analyze-file",
        files=files,
        data=data,
        stream=True,  # Important for NDJSON
        timeout=30
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type')}")
    print(f"Time to first byte: {time.time() - start:.2f}s")
    
    print("\nReceived chunks:")
    for i, line in enumerate(response.iter_lines()):
        if line:
            print(f"  [{i}] {line.decode('utf-8')[:100]}")
            if i >= 5:  # Only show first 5 lines
                print("  ...")
                break
                
except Exception as e:
    print(f"❌ Upload test failed: {e}")
    import traceback
    traceback.print_exc()
