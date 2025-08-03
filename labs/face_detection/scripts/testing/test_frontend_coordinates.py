#!/usr/bin/env python3
"""
🧪 Test Frontend Coordinate Handling
Kiểm tra frontend xử lý coordinates chính xác
"""

import requests
import json
import cv2
import numpy as np
from PIL import Image, ImageDraw
import io

def create_test_face_for_frontend():
    """Create a test face image that matches webcam dimensions"""
    # Create a 640x480 image (standard webcam resolution)
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img.fill(200)  # Light gray background
    
    # Draw a realistic face in the center
    center_x, center_y = 320, 240
    
    # Face skin color
    skin_color = (255, 200, 150)  # BGR
    
    # Draw face oval
    cv2.ellipse(img, (center_x, center_y), (90, 110), 0, 0, 360, skin_color, -1)
    cv2.ellipse(img, (center_x, center_y), (90, 110), 0, 0, 360, (0, 0, 0), 2)
    
    # Draw hair
    cv2.ellipse(img, (center_x, center_y - 80), (100, 40), 0, 0, 360, (50, 50, 150), -1)
    
    # Draw eyes
    eye_color = (255, 255, 255)  # White
    pupil_color = (0, 0, 0)      # Black
    
    # Left eye
    cv2.circle(img, (center_x - 40, center_y - 20), 15, eye_color, -1)
    cv2.circle(img, (center_x - 40, center_y - 20), 15, (0, 0, 0), 2)
    cv2.circle(img, (center_x - 40, center_y - 20), 6, pupil_color, -1)
    
    # Right eye
    cv2.circle(img, (center_x + 40, center_y - 20), 15, eye_color, -1)
    cv2.circle(img, (center_x + 40, center_y - 20), 15, (0, 0, 0), 2)
    cv2.circle(img, (center_x + 40, center_y - 20), 6, pupil_color, -1)
    
    # Draw nose
    nose_points = np.array([
        [center_x, center_y - 10],
        [center_x - 8, center_y + 15],
        [center_x + 8, center_y + 15]
    ], np.int32)
    cv2.fillPoly(img, [nose_points], skin_color)
    cv2.polylines(img, [nose_points], True, (0, 0, 0), 2)
    
    # Draw mouth
    cv2.ellipse(img, (center_x, center_y + 30), (25, 15), 0, 0, 180, (0, 0, 255), 3)
    
    # Add coordinate markers
    cv2.putText(img, "Test Face for Frontend", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(img, "640x480 - Center: (320,240)", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    return img

def test_api_coordinates():
    """Test API coordinates and verify they're correct"""
    print("🧪 Testing API Coordinates")
    print("=" * 50)
    
    # Create test image
    test_img = create_test_face_for_frontend()
    
    # Save for reference
    pil_img = Image.fromarray(cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB))
    pil_img.save('frontend_test_face.jpg')
    print("📸 Saved frontend test image as 'frontend_test_face.jpg'")
    
    # Test API
    img_buffer = io.BytesIO()
    pil_img.save(img_buffer, format='JPEG')
    img_buffer.seek(0)
    
    try:
        files = {'file': ('frontend_test.jpg', img_buffer, 'image/jpeg')}
        response = requests.post('http://localhost:8000/api/v1/faces/detect', files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Response received")
            
            if data.get('success') and data.get('data', {}).get('faces'):
                faces = data['data']['faces']
                print(f"🎯 Detected {len(faces)} face(s)")
                
                for i, face in enumerate(faces):
                    box = face.get('bounding_box', {})
                    print(f"\n📦 Face {i+1} Bounding Box:")
                    print(f"   Left: {box.get('left', 'N/A')}")
                    print(f"   Top: {box.get('top', 'N/A')}")
                    print(f"   Width: {box.get('width', 'N/A')}")
                    print(f"   Height: {box.get('height', 'N/A')}")
                    print(f"   Right: {box.get('right', 'N/A')}")
                    print(f"   Bottom: {box.get('bottom', 'N/A')}")
                    
                    # Calculate center
                    left = box.get('left', 0)
                    top = box.get('top', 0)
                    width = box.get('width', 0)
                    height = box.get('height', 0)
                    center_x = left + width // 2
                    center_y = top + height // 2
                    
                    print(f"   Calculated Center: ({center_x}, {center_y})")
                    print(f"   Expected Center: (320, 240)")
                    
                    # Check if coordinates are reasonable
                    if (200 <= center_x <= 440 and 130 <= center_y <= 350 and
                        width > 100 and height > 100):
                        print("   ✅ Coordinates look correct for frontend")
                        return box
                    else:
                        print("   ⚠️  Coordinates may need adjustment")
                        
            else:
                print("❌ No faces detected")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

def generate_frontend_test_code(box):
    """Generate frontend test code with the detected coordinates"""
    print("\n🔧 Frontend Test Code:")
    print("=" * 50)
    
    if not box:
        print("❌ No bounding box data available")
        return
    
    left = box.get('left', 0)
    top = box.get('top', 0)
    width = box.get('width', 0)
    height = box.get('height', 0)
    
    test_code = f"""
    // Frontend Test Code with Real Coordinates
    // API returned: left={left}, top={top}, width={width}, height={height}
    
    function testBoundingBoxCoordinates() {{
        const video = document.getElementById('webcam-video');
        const canvas = document.getElementById('webcam-canvas');
        
        // Set canvas to match video dimensions exactly
        canvas.width = video.videoWidth;  // Should be 640
        canvas.height = video.videoHeight; // Should be 480
        
        const ctx = canvas.getContext('2d');
        
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw video frame
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Draw bounding box with API coordinates
        const x = {left};
        const y = {top};
        const w = {width};
        const h = {height};
        
        console.log('Drawing bounding box at:', {{ x, y, w, h }});
        
        // Draw green bounding box
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 3;
        ctx.strokeRect(x, y, w, h);
        
        // Draw corner indicators
        const cornerSize = 10;
        ctx.fillStyle = '#00ff00';
        ctx.fillRect(x - 1, y - 1, cornerSize, 2);
        ctx.fillRect(x - 1, y - 1, 2, cornerSize);
        ctx.fillRect(x + w - cornerSize + 1, y - 1, cornerSize, 2);
        ctx.fillRect(x + w - 1, y - 1, 2, cornerSize);
        ctx.fillRect(x - 1, y + h - cornerSize + 1, cornerSize, 2);
        ctx.fillRect(x - 1, y + h - 1, 2, cornerSize);
        ctx.fillRect(x + w - cornerSize + 1, y + h - cornerSize + 1, cornerSize, 2);
        ctx.fillRect(x + w - 1, y + h - 1, 2, cornerSize);
        
        // Draw text
        ctx.fillStyle = '#00ff00';
        ctx.font = '16px Arial';
        ctx.fillText('API Face Detection', x, y - 10);
        ctx.fillText(`Box: ${{x}}, ${{y}} ${{w}}x${{h}}`, x, y + h + 20);
        
        console.log('Bounding box drawn successfully');
    }}
    
    // Call this function when face is detected
    // testBoundingBoxCoordinates();
    """
    
    print(test_code)
    
    print("\n📋 Manual Test Steps:")
    print("1. Open http://localhost:3000")
    print("2. Go to 'Register Face' tab")
    print("3. Click 'Use Webcam'")
    print("4. Open browser console (F12)")
    print("5. Copy and paste the test code above")
    print("6. Call testBoundingBoxCoordinates() in console")
    print("7. Verify bounding box aligns with face")

def create_coordinate_verification():
    """Create verification steps for coordinates"""
    print("\n✅ Coordinate Verification Steps:")
    print("=" * 50)
    
    print("🔍 Check these in browser console:")
    print("1. video.videoWidth should be 640")
    print("2. video.videoHeight should be 480")
    print("3. canvas.width should match video.videoWidth")
    print("4. canvas.height should match video.videoHeight")
    print("5. Bounding box should be green and visible")
    print("6. Box should surround the face completely")
    print("7. No scaling calculations should be used")
    
    print("\n⚠️  Common Issues to Check:")
    print("1. Canvas size doesn't match video size")
    print("2. Browser zoom affecting coordinates")
    print("3. CSS transforms on video element")
    print("4. Device pixel ratio differences")
    print("5. Video aspect ratio vs display ratio")

if __name__ == "__main__":
    print("🧪 Frontend Coordinate Test")
    print("=" * 60)
    
    # Test API coordinates
    box = test_api_coordinates()
    
    # Generate frontend test code
    generate_frontend_test_code(box)
    
    # Create verification steps
    create_coordinate_verification()
    
    print("\n✅ Frontend coordinate test completed!")
    print("\n💡 Next steps:")
    print("1. Use the generated test code in browser console")
    print("2. Verify bounding box alignment")
    print("3. Check console logs for coordinate values")
    print("4. Ensure canvas dimensions match video dimensions") 