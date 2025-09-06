# Makefile for easy testing and development

.PHONY: help start test test-api test-curl clean logs

help:
	@echo "Available commands:"
	@echo "  start      - Start the full system (docker-compose up)"
	@echo "  test       - Start test environment and run all tests"  
	@echo "  test-api   - Run Python API tests"
	@echo "  test-curl  - Run curl-based tests"
	@echo "  clean      - Stop and remove all containers"
	@echo "  logs       - View logs from all services"

start:
	@echo "🚀 Starting storytelling memory system..."
	docker-compose up -d
	@echo "✅ System started!"
	@echo "📍 Memory API: http://localhost:8000"
	@echo "📍 n8n Interface: http://localhost:5678 (admin/admin)"
	@echo "📍 Database: localhost:5432"

test:
	@echo "🧪 Starting test environment..."
	docker-compose -f docker-compose.test.yml up -d
	@echo "⏳ Waiting for services to be ready..."
	sleep 10
	@echo "🔬 Running API tests..."
	python3 test_api.py
	@echo "✅ Tests completed!"

test-api:
	@echo "🔬 Running Python API tests..."
	python3 test_api.py

test-curl:
	@echo "🔬 Running curl API tests..."
	./test_with_curl.sh

clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	docker-compose -f docker-compose.test.yml down -v
	@echo "✅ Cleanup complete!"

logs:
	@echo "📋 Viewing logs..."
	docker-compose logs -f

# Quick development cycle
dev: clean start
	@echo "🔄 Development environment ready!"
	@echo "Run 'make test-api' to validate functionality"