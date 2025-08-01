"""
Streamlit Frontend for Face Detection System
Provides a user-friendly interface for face registration and recognition.
"""

import streamlit as st
import requests
import json
import cv2
import numpy as np
from PIL import Image
import io
import time
from datetime import datetime
import os

# Configuration
API_BASE_URL = "http://localhost:8000"
UPLOAD_DIR = "uploads"

# Page configuration
st.set_page_config(
    page_title="Face Detection System",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function"""
    
    # Sidebar
    st.sidebar.title("Face Detection System")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Home", "Face Registration", "Face Recognition", "Camera Stream", "System Status"]
    )
    
    # Page routing
    if page == "Home":
        show_home_page()
    elif page == "Face Registration":
        show_registration_page()
    elif page == "Face Recognition":
        show_recognition_page()
    elif page == "Camera Stream":
        show_camera_stream_page()
    elif page == "System Status":
        show_system_status_page()

def show_home_page():
    """Display home page with system overview"""
    st.title("👤 Face Detection System")
    st.markdown("---")
    
    # System overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("System Status", "🟢 Online")
    
    with col2:
        st.metric("Registered Faces", get_registered_faces_count())
    
    with col3:
        st.metric("Camera Status", get_camera_status())
    
    # Quick actions
    st.subheader("Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📷 Start Camera", use_container_width=True):
            start_camera()
            st.success("Camera started successfully!")
    
    with col2:
        if st.button("📊 View Analytics", use_container_width=True):
            st.info("Analytics feature coming soon...")
    
    # Recent activity
    st.subheader("Recent Activity")
    st.info("No recent activity to display.")

def show_registration_page():
    """Display face registration page"""
    st.title("📝 Face Registration")
    st.markdown("---")
    
    # Registration form
    with st.form("registration_form"):
        st.subheader("Person Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="Enter full name")
            email = st.text_input("Email", placeholder="Enter email address")
        
        with col2:
            phone = st.text_input("Phone", placeholder="Enter phone number")
            notes = st.text_area("Notes", placeholder="Additional notes")
        
        st.subheader("Face Image")
        
        # Image upload options
        upload_method = st.radio(
            "Choose upload method",
            ["Upload Image", "Camera Capture"]
        )
        
        if upload_method == "Upload Image":
            uploaded_file = st.file_uploader(
                "Choose an image file",
                type=['png', 'jpg', 'jpeg'],
                help="Upload a clear image of the person's face"
            )
            
            if uploaded_file is not None:
                # Display uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
        
        else:  # Camera Capture
            st.info("Camera capture feature will be implemented soon.")
            uploaded_file = None
        
        # Submit button
        submitted = st.form_submit_button("Register Face", type="primary")
        
        if submitted:
            if not name:
                st.error("Name is required!")
            elif uploaded_file is None:
                st.error("Please upload an image or capture from camera!")
            else:
                # Process registration
                with st.spinner("Registering face..."):
                    success = register_face(name, email, phone, notes, uploaded_file)
                    
                    if success:
                        st.success("Face registered successfully!")
                        st.balloons()
                    else:
                        st.error("Failed to register face. Please try again.")

def show_recognition_page():
    """Display face recognition page"""
    st.title("🔍 Face Recognition")
    st.markdown("---")
    
    # Recognition options
    recognition_method = st.radio(
        "Choose recognition method",
        ["Upload Image", "Camera Capture"]
    )
    
    if recognition_method == "Upload Image":
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg'],
            help="Upload an image to recognize the person"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Recognition threshold
            threshold = st.slider(
                "Recognition Threshold",
                min_value=0.0,
                max_value=1.0,
                value=0.6,
                step=0.1,
                help="Higher threshold = more strict matching"
            )
            
            if st.button("Recognize Face", type="primary"):
                with st.spinner("Processing recognition..."):
                    result = recognize_face(uploaded_file, threshold)
                    
                    if result:
                        display_recognition_result(result)
                    else:
                        st.error("No face detected or recognition failed.")
    
    else:  # Camera Capture
        st.info("Camera capture for recognition will be implemented soon.")

def show_camera_stream_page():
    """Display camera stream page"""
    st.title("📹 Camera Stream")
    st.markdown("---")
    
    # Camera controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Start Camera", use_container_width=True):
            start_camera()
            st.success("Camera started!")
    
    with col2:
        if st.button("⏹️ Stop Camera", use_container_width=True):
            stop_camera()
            st.success("Camera stopped!")
    
    with col3:
        if st.button("🔄 Refresh Status", use_container_width=True):
            st.rerun()
    
    # Camera status
    st.subheader("Camera Status")
    status = get_camera_status()
    st.json(status)
    
    # Stream display
    st.subheader("Live Stream")
    
    # Placeholder for video stream
    st.info("Video stream will be displayed here when camera is active.")
    
    # Recognition results
    st.subheader("Recognition Results")
    st.info("Real-time recognition results will appear here.")

def show_system_status_page():
    """Display system status page"""
    st.title("📊 System Status")
    st.markdown("---")
    
    # Health check
    st.subheader("System Health")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            health_data = response.json()
            st.success("✅ System is healthy")
            st.json(health_data)
        else:
            st.error("❌ System health check failed")
    except Exception as e:
        st.error(f"❌ Cannot connect to API: {str(e)}")
    
    # System information
    st.subheader("System Information")
    
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            system_info = response.json()
            st.json(system_info)
    except Exception as e:
        st.error(f"Cannot retrieve system information: {str(e)}")
    
    # Registered faces
    st.subheader("Registered Faces")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/faces/list")
        if response.status_code == 200:
            faces_data = response.json()
            if faces_data.get('data', {}).get('faces'):
                for face in faces_data['data']['faces']:
                    st.write(f"**{face.get('name', 'Unknown')}** - {face.get('created_at', 'Unknown date')}")
            else:
                st.info("No registered faces found.")
        else:
            st.error("Failed to retrieve faces list.")
    except Exception as e:
        st.error(f"Cannot retrieve faces list: {str(e)}")

# Helper functions

def register_face(name, email, phone, notes, uploaded_file):
    """Register a face with the API"""
    try:
        files = {"file": uploaded_file}
        data = {
            "name": name,
            "email": email or "",
            "phone": phone or "",
            "notes": notes or ""
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/v1/faces/upload",
            files=files,
            data=data
        )
        
        return response.status_code == 200
    except Exception as e:
        st.error(f"Registration error: {str(e)}")
        return False

def recognize_face(uploaded_file, threshold):
    """Recognize a face using the API"""
    try:
        files = {"file": uploaded_file}
        data = {"threshold": threshold}
        
        response = requests.post(
            f"{API_BASE_URL}/api/v1/faces/recognize",
            files=files,
            data=data
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Recognition error: {str(e)}")
        return None

def display_recognition_result(result):
    """Display recognition results"""
    if result.get('success') and result.get('data', {}).get('recognized'):
        data = result['data']
        person = data['person']
        
        st.success("✅ Face Recognized!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Name:** {person['name']}")
            if person.get('email'):
                st.write(f"**Email:** {person['email']}")
            if person.get('phone'):
                st.write(f"**Phone:** {person['phone']}")
        
        with col2:
            st.write(f"**Confidence:** {data['confidence']:.2%}")
            if person.get('notes'):
                st.write(f"**Notes:** {person['notes']}")
        
        # Show other matches
        if data.get('matches') and len(data['matches']) > 1:
            st.subheader("Other Possible Matches")
            for match in data['matches'][1:]:
                st.write(f"- {match['name']} ({match['confidence']:.2%})")
    
    else:
        st.warning("❌ No matching face found.")

def get_registered_faces_count():
    """Get count of registered faces"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/faces/list")
        if response.status_code == 200:
            data = response.json()
            faces = data.get('data', {}).get('faces', [])
            return len(faces)
        return 0
    except:
        return 0

def get_camera_status():
    """Get camera status"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/camera/status")
        if response.status_code == 200:
            data = response.json()
            return "🟢 Active" if data.get('data', {}).get('is_running') else "🔴 Inactive"
        return "❓ Unknown"
    except:
        return "❓ Unknown"

def start_camera():
    """Start the camera"""
    try:
        response = requests.post(f"{API_BASE_URL}/api/v1/camera/start")
        return response.status_code == 200
    except:
        return False

def stop_camera():
    """Stop the camera"""
    try:
        response = requests.post(f"{API_BASE_URL}/api/v1/camera/stop")
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    main() 