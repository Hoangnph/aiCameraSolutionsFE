#!/bin/bash

# AI Camera Counting System - Service Test Script
# Tests all services and API endpoints

echo "🔍 Testing AI Camera Counting System Services..."
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test endpoint
test_endpoint() {
    local name="$1"
    local url="$2"
    local method="${3:-GET}"
    local data="$4"
    local headers="$5"
    
    echo -n "Testing $name... "
    
    if [ -n "$data" ]; then
        response=$(curl -s -w "%{http_code}" -X $method "$url" -H "Content-Type: application/json" $headers -d "$data")
    else
        response=$(curl -s -w "%{http_code}" -X $method "$url" $headers)
    fi
    
    http_code="${response: -3}"
    body="${response%???}"
    
    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
        echo -e "${GREEN}✅ PASS${NC} ($http_code)"
    else
        echo -e "${RED}❌ FAIL${NC} ($http_code)"
        echo "Response: $body"
    fi
}

# Test 1: beAuth Health Check
echo ""
echo "1. Testing beAuth Service Health..."
test_endpoint "beAuth Health" "http://localhost:3001/health"

# Test 2: beCamera Health Check
echo ""
echo "2. Testing beCamera Service Health..."
test_endpoint "beCamera Health" "http://localhost:3002/health"

# Test 3: Database Connection (via beCamera)
echo ""
echo "3. Testing Database Connection..."
test_endpoint "Database via beCamera" "http://localhost:3002/api/v1/test/cameras"

# Test 4: User Registration
echo ""
echo "4. Testing User Registration..."
test_endpoint "User Registration" "http://localhost:3001/api/v1/auth/register" "POST" '{"username": "testuser2", "email": "testuser2@example.com", "password": "Test123!", "confirmPassword": "Test123!", "registrationCode": "REG001", "firstName": "Test", "lastName": "User2"}'

# Test 5: User Login
echo ""
echo "5. Testing User Login..."
login_response=$(curl -s -X POST "http://localhost:3001/api/v1/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username": "testadmin", "password": "Test123!"}')

if echo "$login_response" | grep -q "accessToken"; then
    echo -e "User Login ${GREEN}✅ PASS${NC}"
    # Extract token for authenticated tests
    token=$(echo "$login_response" | grep -o '"accessToken":"[^"]*"' | cut -d'"' -f4)
else
    echo -e "User Login ${RED}❌ FAIL${NC}"
    echo "Response: $login_response"
    token=""
fi

# Test 6: Authenticated Camera API
if [ -n "$token" ]; then
    echo ""
    echo "6. Testing Authenticated Camera API..."
    test_endpoint "Authenticated Cameras" "http://localhost:3002/api/v1/cameras" "GET" "" "-H \"Authorization: Bearer $token\""
else
    echo ""
    echo "6. Testing Authenticated Camera API... ${YELLOW}⚠️ SKIP (no token)${NC}"
fi

# Test 7: Analytics API
echo ""
echo "7. Testing Analytics API..."
test_endpoint "Analytics Summary" "http://localhost:3002/api/v1/analytics/summary"

# Test 8: Docker Containers Status
echo ""
echo "8. Checking Docker Containers Status..."
containers=("beauth_service" "becamera_service" "becamera_postgres" "becamera_redis" "becamera_websocket")

for container in "${containers[@]}"; do
    if docker ps --format "table {{.Names}}\t{{.Status}}" | grep -q "$container.*Up"; then
        echo -e "  $container ${GREEN}✅ Running${NC}"
    else
        echo -e "  $container ${RED}❌ Not Running${NC}"
    fi
done

# Test 9: Port Availability
echo ""
echo "9. Checking Port Availability..."
ports=(3001 3002 3004 5432 6379)

for port in "${ports[@]}"; do
    if lsof -i :$port > /dev/null 2>&1; then
        echo -e "  Port $port ${GREEN}✅ Available${NC}"
    else
        echo -e "  Port $port ${RED}❌ Not Available${NC}"
    fi
done

echo ""
echo "================================================"
echo "🎉 Service Test Complete!"
echo ""
echo "📊 Summary:"
echo "- beAuth Service: http://localhost:3001"
echo "- beCamera Service: http://localhost:3002"
echo "- WebSocket Service: ws://localhost:3004"
echo "- Database: localhost:5432"
echo "- Redis: localhost:6379"
echo ""
echo "🔗 Useful URLs:"
echo "- Health Checks: http://localhost:3001/health, http://localhost:3002/health"
echo "- API Docs: Check individual service documentation"
echo "- Test Data: Available in database (users, cameras, registration codes)"
echo ""
echo "📝 Next Steps:"
echo "1. Test frontend integration"
echo "2. Implement AI model processing"
echo "3. Add real-time features"
echo "4. Deploy to production" 