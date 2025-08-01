#!/usr/bin/env python3
"""
🔍 Debug Scaling Issue
Kiểm tra vấn đề scaling factors quá nhỏ
"""

import requests
import json
import os
from PIL import Image, ImageDraw
import io

def analyze_scaling_problem():
    """Phân tích vấn đề scaling"""
    print("🔍 Analyzing Scaling Problem...")
    
    print("\n📊 Problem Analysis:")
    print("   - Console logs show very small scaling factors:")
    print("     * scaleX: 0.46875")
    print("     * scaleY: 0.3125")
    print("   - This suggests video.offsetWidth is much larger than expected")
    print("   - Scaled coordinates are tiny:")
    print("     * x: 48.28125, y: 10")
    print("     * width: 50.625, height: 33.75")
    
    print("\n🔧 Root Cause Analysis:")
    print("   1. video.offsetWidth might be affected by browser zoom")
    print("   2. CSS scaling might be applied to video element")
    print("   3. Browser zoom level might be different than 100%")
    print("   4. Canvas size might not match video display size")
    
    print("\n📋 Potential Issues:")
    print("   1. Browser zoom level ≠ 100%")
    print("   2. CSS transform: scale() applied to video")
    print("   3. Video element has width/height CSS properties")
    print("   4. Canvas size doesn't match video display size")
    print("   5. Device pixel ratio (DPR) affecting calculations")

def test_with_real_image():
    """Test với real image để verify API data"""
    print("\n🔍 Testing with real uploaded image...")
    
    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        files = [f for f in os.listdir(uploads_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if files:
            test_file = os.path.join(uploads_dir, files[0])
            print(f"📷 Using: {test_file}")
            
            try:
                with open(test_file, 'rb') as f:
                    files = {'file': (files[0], f, 'image/jpeg')}
                    response = requests.post('http://localhost:8000/api/v1/faces/detect', files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data['success'] and data['data']['faces']:
                        faces = data['data']['faces']
                        image_size = data['data']['image_size']
                        
                        print(f"✅ API Response:")
                        print(f"   - Image size: {image_size['width']} x {image_size['height']}")
                        
                        for i, face in enumerate(faces):
                            box = face['bounding_box']
                            print(f"   - Face {i+1} box: ({box['left']}, {box['top']}) to ({box['right']}, {box['bottom']})")
                            print(f"   - Face {i+1} size: {box['width']} x {box['height']}")
                            
                            # Calculate expected scaling
                            expected_scale_x = 640 / image_size['width']  # Assuming canvas width = 640
                            expected_scale_y = 480 / image_size['height']  # Assuming canvas height = 480
                            
                            print(f"   - Expected scaling: scaleX={expected_scale_x:.3f}, scaleY={expected_scale_y:.3f}")
                            
                            # Calculate expected scaled coordinates
                            expected_x = box['left'] * expected_scale_x
                            expected_y = box['top'] * expected_scale_y
                            expected_width = box['width'] * expected_scale_x
                            expected_height = box['height'] * expected_scale_y
                            
                            print(f"   - Expected scaled: x={expected_x:.1f}, y={expected_y:.1f}, w={expected_width:.1f}, h={expected_height:.1f}")
                    else:
                        print("❌ No faces detected")
                else:
                    print(f"❌ HTTP Error: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("❌ No image files found")
    else:
        print("❌ Uploads directory not found")

def create_fix_recommendations():
    """Tạo recommendations để fix scaling issue"""
    print("\n🔧 Fix Recommendations:")
    
    print("\n1. **Check Browser Zoom Level**")
    print("   - Ensure browser zoom is at 100%")
    print("   - Check if user has zoomed in/out")
    print("   - Reset zoom: Ctrl+0 (Windows) or Cmd+0 (Mac)")
    
    print("\n2. **Check CSS Scaling**")
    print("   - Look for CSS transform: scale() on video element")
    print("   - Check if video has width/height CSS properties")
    print("   - Ensure video element is not being scaled by CSS")
    
    print("\n3. **Fix Canvas Size**")
    print("   - Ensure canvas.width matches video.offsetWidth")
    print("   - Ensure canvas.height matches video.offsetHeight")
    print("   - Add canvas size debugging")
    
    print("\n4. **Add Device Pixel Ratio Check**")
    print("   - Check window.devicePixelRatio")
    print("   - Account for high DPR displays")
    print("   - Use getBoundingClientRect() for accurate dimensions")
    
    print("\n5. **Improved Scaling Calculation**")
    print("   - Use getBoundingClientRect() instead of offsetWidth/offsetHeight")
    print("   - Account for CSS transforms")
    print("   - Handle browser zoom properly")

def create_debug_frontend_code():
    """Tạo debug code cho frontend"""
    print("\n🔧 Debug Frontend Code:")
    
    print("\n```javascript")
    print("// Add this to drawBoundingBoxes function")
    print("function debugVideoProperties() {")
    print("    const video = document.getElementById('webcam-video');")
    print("    const canvas = document.getElementById('webcam-canvas');")
    print("    ")
    print("    console.log('=== VIDEO PROPERTIES DEBUG ===');")
    print("    console.log('video.videoWidth:', video.videoWidth);")
    print("    console.log('video.videoHeight:', video.videoHeight);")
    print("    console.log('video.offsetWidth:', video.offsetWidth);")
    print("    console.log('video.offsetHeight:', video.offsetHeight);")
    print("    console.log('video.clientWidth:', video.clientWidth);")
    print("    console.log('video.clientHeight:', video.clientHeight);")
    print("    console.log('canvas.width:', canvas.width);")
    print("    console.log('canvas.height:', canvas.height);")
    print("    console.log('window.devicePixelRatio:', window.devicePixelRatio);")
    print("    ")
    print("    const rect = video.getBoundingClientRect();")
    print("    console.log('getBoundingClientRect():', rect);")
    print("    ")
    print("    // Check for CSS transforms")
    print("    const style = window.getComputedStyle(video);")
    print("    console.log('transform:', style.transform);")
    print("    console.log('scale:', style.scale);")
    print("    console.log('zoom:', style.zoom);")
    print("}")
    print("```")
    
    print("\n```javascript")
    print("// Improved scaling calculation")
    print("function getAccurateScaling() {")
    print("    const video = document.getElementById('webcam-video');")
    print("    const canvas = document.getElementById('webcam-canvas');")
    print("    ")
    print("    // Use getBoundingClientRect for accurate dimensions")
    print("    const rect = video.getBoundingClientRect();")
    print("    ")
    print("    const scaleX = canvas.width / rect.width;")
    print("    const scaleY = canvas.height / rect.height;")
    print("    ")
    print("    console.log('Accurate scaling:', { scaleX, scaleY });")
    print("    return { scaleX, scaleY };")
    print("}")
    print("```")

def main():
    """Main function"""
    print("🚀 Debug Scaling Issue")
    print("=" * 50)
    
    # Phân tích vấn đề
    analyze_scaling_problem()
    
    # Test với real image
    test_with_real_image()
    
    # Tạo recommendations
    create_fix_recommendations()
    
    # Tạo debug code
    create_debug_frontend_code()
    
    print("\n📋 Next Steps:")
    print("1. Add debug code to frontend")
    print("2. Check browser zoom level")
    print("3. Verify CSS scaling")
    print("4. Use getBoundingClientRect() for accurate dimensions")
    print("5. Test with different browser zoom levels")
    
    print("\n✅ Scaling issue debug completed!")

if __name__ == "__main__":
    main() 