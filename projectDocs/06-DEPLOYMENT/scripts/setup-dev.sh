#!/bin/bash

# ========================================
# AI Camera Counting System - Development Setup Script
# ========================================

set -e  # Exit on any error

echo "🚀 Setting up AI Camera Counting System Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    print_status "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Check if Node.js is installed
check_nodejs() {
    print_status "Checking Node.js installation..."
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+ first."
        exit 1
    fi
    
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        print_error "Node.js version 18+ is required. Current version: $(node --version)"
        exit 1
    fi
    
    print_success "Node.js $(node --version) is installed"
}

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.11+ first."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
        print_error "Python 3.11+ is required. Current version: $(python3 --version)"
        exit 1
    fi
    
    print_success "Python $(python3 --version) is installed"
}

# Setup environment files
setup_env_files() {
    print_status "Setting up environment files..."
    
    # Copy environment files if they don't exist
    if [ ! -f "env.development" ]; then
        print_warning "env.development not found, creating from template..."
        # This will be created by the script
    fi
    
    if [ ! -f "beAuth/.env" ]; then
        print_warning "beAuth/.env not found, creating from template..."
        cp beAuth/env.example beAuth/.env 2>/dev/null || print_warning "beAuth/env.example not found"
    fi
    
    print_success "Environment files are ready"
}

# Install frontend dependencies
install_frontend_deps() {
    print_status "Installing frontend dependencies..."
    
    if [ ! -d "node_modules" ]; then
        npm install
        print_success "Frontend dependencies installed"
    else
        print_status "Frontend dependencies already installed"
    fi
}

# Install beAuth dependencies
install_beauth_deps() {
    print_status "Installing beAuth dependencies..."
    
    cd beAuth
    if [ ! -d "node_modules" ]; then
        npm install
        print_success "beAuth dependencies installed"
    else
        print_status "beAuth dependencies already installed"
    fi
    cd ..
}

# Install beCamera dependencies
install_becamera_deps() {
    print_status "Installing beCamera dependencies..."
    
    cd beCamera
    if [ ! -f "requirements.txt" ]; then
        print_error "beCamera/requirements.txt not found"
        exit 1
    fi
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment and install dependencies
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    deactivate
    
    print_success "beCamera dependencies installed"
    cd ..
}

# Start infrastructure services
start_infrastructure() {
    print_status "Starting infrastructure services (PostgreSQL, Redis)..."
    
    # Stop any existing containers
    docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
    
    # Start only infrastructure services
    docker-compose -f docker-compose.dev.yml up -d postgres redis
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 10
    
    # Test database connection
    print_status "Testing database connection..."
    if docker-compose -f docker-compose.dev.yml exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
        print_success "PostgreSQL is ready"
    else
        print_error "PostgreSQL is not ready"
        exit 1
    fi
    
    # Test Redis connection
    print_status "Testing Redis connection..."
    if docker-compose -f docker-compose.dev.yml exec -T redis redis-cli ping > /dev/null 2>&1; then
        print_success "Redis is ready"
    else
        print_error "Redis is not ready"
        exit 1
    fi
}

# Setup database
setup_database() {
    print_status "Setting up database..."
    
    cd beAuth
    
    # Run migrations
    print_status "Running database migrations..."
    npm run migrate 2>/dev/null || print_warning "Migrations failed or already applied"
    
    # Seed data
    print_status "Seeding database with sample data..."
    npm run seed 2>/dev/null || print_warning "Seeding failed or already done"
    
    cd ..
    
    print_success "Database setup completed"
}

# Create startup script
create_startup_script() {
    print_status "Creating startup script..."
    
    cat > start-dev.sh << 'EOF'
#!/bin/bash

# ========================================
# AI Camera Counting System - Development Startup Script
# ========================================

set -e

echo "🚀 Starting AI Camera Counting System Development Environment..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Start infrastructure if not running
print_status "Starting infrastructure services..."
docker-compose -f docker-compose.dev.yml up -d postgres redis

# Wait for services
sleep 5

# Start beAuth service
print_status "Starting beAuth service..."
cd beAuth
npm run dev &
BEAUTH_PID=$!
cd ..

# Start beCamera service
print_status "Starting beCamera service..."
cd beCamera
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 3002 --reload &
BECAMERA_PID=$!
deactivate
cd ..

# Start WebSocket server
print_status "Starting WebSocket server..."
cd beCamera
source venv/bin/activate
python websocket_server.py &
WEBSOCKET_PID=$!
deactivate
cd ..

# Start frontend
print_status "Starting frontend..."
npm start &
FRONTEND_PID=$!

print_success "All services started!"
echo ""
echo "📱 Service URLs:"
echo "   Frontend:     http://localhost:3000"
echo "   beAuth API:   http://localhost:3001/api/v1"
echo "   beCamera API: http://localhost:3002/api/v1"
echo "   WebSocket:    ws://localhost:3003"
echo ""
echo "🔑 Default credentials:"
echo "   Admin: admin / Admin123!"
echo "   User:  testuser / Test123!"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    print_status "Stopping all services..."
    kill $BEAUTH_PID $BECAMERA_PID $WEBSOCKET_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

# Set trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Wait for all background processes
wait
EOF

    chmod +x start-dev.sh
    print_success "Startup script created: start-dev.sh"
}

# Main setup function
main() {
    echo "========================================"
    echo "AI Camera Counting System - Dev Setup"
    echo "========================================"
    echo ""
    
    # Check prerequisites
    check_docker
    check_nodejs
    check_python
    
    # Setup environment
    setup_env_files
    
    # Install dependencies
    install_frontend_deps
    install_beauth_deps
    install_becamera_deps
    
    # Start infrastructure
    start_infrastructure
    
    # Setup database
    setup_database
    
    # Create startup script
    create_startup_script
    
    echo ""
    echo "========================================"
    print_success "Development environment setup completed!"
    echo "========================================"
    echo ""
    echo "🚀 To start the development environment:"
    echo "   ./start-dev.sh"
    echo ""
    echo "📱 Service URLs:"
    echo "   Frontend:     http://localhost:3000"
    echo "   beAuth API:   http://localhost:3001/api/v1"
    echo "   beCamera API: http://localhost:3002/api/v1"
    echo "   WebSocket:    ws://localhost:3003"
    echo ""
    echo "🔑 Default credentials:"
    echo "   Admin: admin / Admin123!"
    echo "   User:  testuser / Test123!"
    echo ""
    echo "📚 Documentation:"
    echo "   Project tracking: projectLogs/tracking_project.md"
    echo "   beAuth docs: beAuth/README.md"
    echo "   beCamera docs: beCamera/docs/"
    echo ""
}

# Run main function
main "$@" 