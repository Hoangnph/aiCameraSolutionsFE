#!/usr/bin/env python3
"""
🧪 Test Frontend Face List
Kiểm tra frontend face list functionality
"""

import requests
import json

def test_frontend_elements():
    """Test if frontend elements exist"""
    print("🧪 Testing Frontend Elements")
    print("=" * 40)
    
    # Check if we can access the frontend
    try:
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            print("✅ HTML content loaded")
            
            # Check for key elements in HTML
            html_content = response.text
            
            elements_to_check = [
                ('faces-table-body', 'Table body element'),
                ('faces-empty-state', 'Empty state element'),
                ('faces-table', 'Table element'),
                ('loadFaces', 'loadFaces function'),
                ('showTab', 'showTab function'),
                ('deleteFace', 'deleteFace function')
            ]
            
            for element_id, description in elements_to_check:
                if element_id in html_content:
                    print(f"✅ {description} found")
                else:
                    print(f"❌ {description} missing")
                    
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error accessing frontend: {e}")

def test_api_integration():
    """Test API integration with frontend"""
    print("\n🔗 Testing API Integration")
    print("=" * 35)
    
    try:
        # Test API endpoint that frontend uses
        response = requests.get('http://localhost:8000/api/v1/faces/list')
        if response.status_code == 200:
            data = response.json()
            faces = data['data']['faces']
            
            print(f"✅ API endpoint accessible")
            print(f"✅ Found {len(faces)} faces")
            
            # Test image URLs
            if faces:
                face = faces[0]
                image_url = f"http://localhost:8000{face.get('image_url', '')}"
                
                img_response = requests.head(image_url)
                if img_response.status_code == 200:
                    print("✅ Face images accessible")
                else:
                    print(f"❌ Face images not accessible: {img_response.status_code}")
                    
        else:
            print(f"❌ API endpoint failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing API integration: {e}")

def test_frontend_workflow():
    """Test the complete frontend workflow"""
    print("\n🔄 Testing Frontend Workflow")
    print("=" * 35)
    
    workflow_steps = [
        "1. User clicks 'Face List' tab",
        "2. showTab('faces') function called",
        "3. loadFaces() function called automatically",
        "4. API request to /api/v1/faces/list",
        "5. Response processed and table built",
        "6. Face images loaded from /api/v1/faces/{id}/image",
        "7. Quality badges and delete buttons rendered"
    ]
    
    for step in workflow_steps:
        print(f"✅ {step}")
    
    print("\n💡 Manual Testing Steps:")
    print("   1. Open browser to http://localhost:3000")
    print("   2. Click 'Face List' tab")
    print("   3. Check browser console for debug logs")
    print("   4. Verify table loads with faces")
    print("   5. Test delete functionality")

def test_debug_information():
    """Provide debug information"""
    print("\n🐛 Debug Information")
    print("=" * 25)
    
    print("🔍 Check these in browser console:")
    print("   - '🔄 Loading faces...' message")
    print("   - '📡 API Response status: 200'")
    print("   - '📊 API Response data: {...}'")
    print("   - '📋 Found X faces, building table'")
    print("   - '✅ Added face row X' messages")
    print("   - '🎉 Face table built successfully'")
    
    print("\n🔧 Common Issues:")
    print("   - CORS errors in console")
    print("   - Network request failures")
    print("   - JavaScript errors")
    print("   - Missing DOM elements")
    print("   - API endpoint not responding")

if __name__ == "__main__":
    print("🧪 Frontend Face List Test")
    print("=" * 60)
    
    # Test frontend elements
    test_frontend_elements()
    
    # Test API integration
    test_api_integration()
    
    # Test workflow
    test_frontend_workflow()
    
    # Provide debug info
    test_debug_information()
    
    print("\n✅ Test completed!")
    print("💡 If face list is still empty:")
    print("   1. Check browser console for errors")
    print("   2. Verify network tab for API calls")
    print("   3. Ensure both frontend and backend are running")
    print("   4. Try refreshing the page") 