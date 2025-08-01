#!/usr/bin/env python3
"""
🧪 Test Real Face Detection API
Kiểm tra API với real face detection
"""

import requests
import json
import cv2
import numpy as np
from PIL import Image, ImageDraw
import io

def create_realistic_face_image():
    """Create a more realistic face image using OpenCV"""
    # Create a 640x480 image
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img.fill(200)  # Light gray background
    
    # Draw a more realistic face
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
    
    # Add text
    cv2.putText(img, "Test Face", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img, "640x480", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    return img

def test_api_with_real_face():
    """Test API with a more realistic face image"""
    print("🧪 Testing API with Realistic Face Image")
    print("=" * 50)
    
    # Create realistic face image
    face_img = create_realistic_face_image()
    
    # Convert to PIL Image for saving
    pil_img = Image.fromarray(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))
    pil_img.save('realistic_face_test.jpg')
    print("📸 Saved realistic face image as 'realistic_face_test.jpg'")
    
    # Convert to bytes for API
    img_buffer = io.BytesIO()
    pil_img.save(img_buffer, format='JPEG')
    img_buffer.seek(0)
    
    try:
        files = {'file': ('realistic_face.jpg', img_buffer, 'image/jpeg')}
        response = requests.post('http://localhost:8000/api/v1/faces/detect', files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Response:")
            print(json.dumps(data, indent=2))
            
            if data.get('success') and data.get('data', {}).get('faces'):
                faces = data['data']['faces']
                print(f"\n🎯 Detected {len(faces)} face(s)")
                
                for i, face in enumerate(faces):
                    box = face.get('bounding_box', {})
                    print(f"\n📦 Face {i+1} Bounding Box:")
                    print(f"   Left: {box.get('left', 'N/A')}")
                    print(f"   Top: {box.get('top', 'N/A')}")
                    print(f"   Width: {box.get('width', 'N/A')}")
                    print(f"   Height: {box.get('height', 'N/A')}")
                    print(f"   Right: {box.get('right', 'N/A')}")
                    print(f"   Bottom: {box.get('bottom', 'N/A')}")
                    print(f"   Confidence: {face.get('confidence', 'N/A'):.3f}")
                    print(f"   Quality: {face.get('quality_score', 'N/A'):.3f}")
                    
                    # Calculate expected center
                    left = box.get('left', 0)
                    top = box.get('top', 0)
                    width = box.get('width', 0)
                    height = box.get('height', 0)
                    
                    center_x = left + width // 2
                    center_y = top + height // 2
                    
                    print(f"   Calculated Center: ({center_x}, {center_y})")
                    print(f"   Expected Center: (320, 240)")
                    
                    # Check if bounding box is reasonable
                    if 200 <= center_x <= 440 and 130 <= center_y <= 350:
                        print("   ✅ Bounding box position looks reasonable")
                    else:
                        print("   ⚠️  Bounding box position may be incorrect")
                        
            else:
                print("❌ No faces detected in realistic image")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def analyze_frontend_issues():
    """Analyze potential frontend issues"""
    print("\n🌐 Frontend Issues Analysis:")
    print("=" * 50)
    
    print("🔍 Common Frontend Problems:")
    print("1. Canvas size doesn't match video dimensions")
    print("2. Video element has CSS scaling applied")
    print("3. Browser zoom affects coordinate calculations")
    print("4. Device pixel ratio not accounted for")
    print("5. Video aspect ratio vs display aspect ratio mismatch")
    
    print("\n🔧 Frontend Solutions:")
    print("1. Set canvas.width = video.videoWidth")
    print("2. Set canvas.height = video.videoHeight")
    print("3. Use video.videoWidth/video.videoHeight for scaling")
    print("4. Account for window.devicePixelRatio")
    print("5. Handle browser zoom with window.visualViewport.scale")
    
    print("\n📐 Correct Frontend Implementation:")
    print("""
    // Correct way to handle coordinates
    const video = document.getElementById('webcam-video');
    const canvas = document.getElementById('webcam-canvas');
    
    // Set canvas to match video dimensions exactly
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Use original coordinates from API
    const box = face.bounding_box;
    const x = box.left;
    const y = box.top;
    const width = box.width;
    const height = box.height;
    
    // Draw bounding box
    ctx.strokeRect(x, y, width, height);
    """)

def create_debug_frontend_code():
    """Create debug code for frontend"""
    print("\n🔧 Frontend Debug Code:")
    print("=" * 50)
    
    debug_code = """
    // Add this to your frontend JavaScript for debugging
    
    function debugVideoAndCanvas() {
        const video = document.getElementById('webcam-video');
        const canvas = document.getElementById('webcam-canvas');
        
        console.log('=== VIDEO DEBUG ===');
        console.log('video.videoWidth:', video.videoWidth);
        console.log('video.videoHeight:', video.videoHeight);
        console.log('video.offsetWidth:', video.offsetWidth);
        console.log('video.offsetHeight:', video.offsetHeight);
        console.log('video.clientWidth:', video.clientWidth);
        console.log('video.clientHeight:', video.clientHeight);
        
        console.log('=== CANVAS DEBUG ===');
        console.log('canvas.width:', canvas.width);
        console.log('canvas.height:', canvas.height);
        console.log('canvas.offsetWidth:', canvas.offsetWidth);
        console.log('canvas.offsetHeight:', canvas.offsetHeight);
        
        console.log('=== BROWSER DEBUG ===');
        console.log('window.devicePixelRatio:', window.devicePixelRatio);
        console.log('window.visualViewport.scale:', window.visualViewport?.scale);
        
        const rect = video.getBoundingClientRect();
        console.log('video.getBoundingClientRect():', rect);
        
        const style = window.getComputedStyle(video);
        console.log('video transform:', style.transform);
        console.log('video scale:', style.scale);
    }
    
    function drawBoundingBoxCorrectly(faces, canvas) {
        const ctx = canvas.getContext('2d');
        const video = document.getElementById('webcam-video');
        
        // Clear and redraw video frame
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        faces.forEach((face, index) => {
            const box = face.bounding_box;
            
            // Use original coordinates directly
            const x = box.left;
            const y = box.top;
            const width = box.width;
            const height = box.height;
            
            console.log(`Face ${index + 1} coordinates:`, { x, y, width, height });
            
            // Draw bounding box
            ctx.strokeStyle = '#00ff00';
            ctx.lineWidth = 2;
            ctx.strokeRect(x, y, width, height);
            
            // Draw corner indicators
            const cornerSize = 8;
            ctx.fillStyle = '#00ff00';
            ctx.fillRect(x - 1, y - 1, cornerSize, 2);
            ctx.fillRect(x - 1, y - 1, 2, cornerSize);
            ctx.fillRect(x + width - cornerSize + 1, y - 1, cornerSize, 2);
            ctx.fillRect(x + width - 1, y - 1, 2, cornerSize);
            ctx.fillRect(x - 1, y + height - cornerSize + 1, cornerSize, 2);
            ctx.fillRect(x - 1, y + height - 1, 2, cornerSize);
            ctx.fillRect(x + width - cornerSize + 1, y + height - cornerSize + 1, cornerSize, 2);
            ctx.fillRect(x + width - 1, y + height - 1, 2, cornerSize);
            
            // Draw text
            ctx.fillStyle = '#00ff00';
            ctx.font = '14px Arial';
            ctx.fillText(`Face ${index + 1}: ${(face.confidence * 100).toFixed(1)}%`, x, y - 5);
            ctx.fillText(`Quality: ${(face.quality_score * 100).toFixed(1)}%`, x, y + height + 15);
        });
    }
    """
    
    print(debug_code)

if __name__ == "__main__":
    print("🧪 Real Face Detection Test")
    print("=" * 60)
    
    # Test with realistic face
    test_api_with_real_face()
    
    # Analyze frontend issues
    analyze_frontend_issues()
    
    # Create debug code
    create_debug_frontend_code()
    
    print("\n✅ Testing completed!")
    print("\n💡 Next steps:")
    print("1. Check 'realistic_face_test.jpg' for face quality")
    print("2. If API detects faces, use the debug code in frontend")
    print("3. Ensure canvas dimensions match video dimensions exactly")
    print("4. Test with real webcam feed") 