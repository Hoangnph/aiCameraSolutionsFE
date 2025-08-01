# 🔍 **Workflow Test Plan - Face Embedding System**

## 📋 **Tổng quan Workflow:**

### **1. Frontend → Backend → Database Flow:**
```
Frontend (Webcam/Upload) → API Server → Face Processing → Vector DB → SQLite DB
```

### **2. Recognition Flow:**
```
Frontend (Webcam/Upload) → API Server → Face Processing → Vector Search → Response
```

## 🎯 **Test Cases cần thực hiện:**

### **Phase 1: Backend API Testing**
- [ ] **1.1** API Server Startup
- [ ] **1.2** Health Check Endpoint
- [ ] **1.3** Database Connection
- [ ] **1.4** Vector Database Initialization

### **Phase 2: Face Upload Workflow**
- [ ] **2.1** Upload Face via API (curl)
- [ ] **2.2** Face Detection & Processing
- [ ] **2.3** Embedding Generation
- [ ] **2.4** Vector Database Storage
- [ ] **2.5** SQLite Database Storage
- [ ] **2.6** Metadata Validation

### **Phase 3: Face Recognition Workflow**
- [ ] **3.1** Recognition via API (curl)
- [ ] **3.2** Face Detection & Embedding
- [ ] **3.3** Vector Search
- [ ] **3.4** Similarity Matching
- [ ] **3.5** Response Format Validation

### **Phase 4: Frontend Integration**
- [ ] **4.1** Frontend Server Startup
- [ ] **4.2** Webcam Capture
- [ ] **4.3** File Upload
- [ ] **4.4** API Communication
- [ ] **4.5** Response Display

### **Phase 5: End-to-End Testing**
- [ ] **5.1** Complete Upload → Recognition Flow
- [ ] **5.2** Multiple Faces Testing
- [ ] **5.3** Error Handling
- [ ] **5.4** Performance Testing

## 🔧 **Các vấn đề cần giải quyết:**

### **1. API Server Issues:**
- ❌ ModuleNotFoundError: No module named 'src'
- ❌ Address already in use
- ❌ Server startup failures

### **2. Database Issues:**
- ❌ Empty database after cleanup
- ❌ Metadata field mismatches
- ❌ Person ID generation issues

### **3. Frontend Issues:**
- ❌ Webcam recognition display
- ❌ API endpoint mismatches
- ❌ Response parsing errors

## 📊 **Test Data Requirements:**

### **Test Images:**
- [ ] Sample face images for upload
- [ ] Different quality images
- [ ] Multiple faces for testing
- [ ] Invalid images for error testing

### **Test Scenarios:**
- [ ] Single face registration
- [ ] Multiple face registration
- [ ] Recognition with high confidence
- [ ] Recognition with low confidence
- [ ] No face detected scenarios
- [ ] Invalid file uploads

## 🚀 **Execution Plan:**

### **Step 1: Fix API Server**
1. Kill existing processes
2. Start API server correctly
3. Verify health check
4. Test basic endpoints

### **Step 2: Database Setup**
1. Initialize databases
2. Create test data
3. Verify storage mechanisms
4. Test data retrieval

### **Step 3: API Testing**
1. Test upload endpoint
2. Test recognition endpoint
3. Test list endpoint
4. Verify response formats

### **Step 4: Frontend Testing**
1. Start frontend server
2. Test webcam functionality
3. Test file upload
4. Verify API communication

### **Step 5: End-to-End Testing**
1. Complete workflow testing
2. Error scenario testing
3. Performance validation
4. Documentation update

## 📈 **Success Criteria:**

### **API Level:**
- ✅ All endpoints return 200 OK
- ✅ Correct response formats
- ✅ Proper error handling
- ✅ Database operations successful

### **Frontend Level:**
- ✅ Webcam capture working
- ✅ File upload working
- ✅ API communication successful
- ✅ Response display correct

### **Database Level:**
- ✅ Face embeddings stored
- ✅ Metadata preserved
- ✅ Recognition queries working
- ✅ Data consistency maintained

## 🎯 **Next Actions:**
1. Fix API server startup issues
2. Create comprehensive test suite
3. Execute test plan systematically
4. Document all findings and fixes 