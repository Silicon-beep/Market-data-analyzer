# Makefile for Market Data Analyzer
# Builds both Python and OCaml components

.PHONY: all clean install build-ocaml test demo help run

# Default target
all: install build-ocaml

# Install Python dependencies
install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✓ Python dependencies installed"

# Build OCaml module
build-ocaml:
	@echo "🔨 Building OCaml analytics module..."
	cd ocaml_analytics && chmod +x build.sh && ./build.sh
	@echo "✓ OCaml module built"

# Run comprehensive demo
demo:
	@echo "🎬 Running comprehensive demo..."
	python3 demo.py

# Run basic test
test:
	@echo "🧪 Running tests..."
	@echo ""
	@echo "Test 1: Data Fetcher"
	@python3 -c "from src.data_fetcher import MarketDataFetcher; f=MarketDataFetcher(); df=f.generate_stock_prices('TEST',days=10); print(f'✓ Generated {len(df)} rows')"
	@echo ""
	@echo "Test 2: Analytics"
	@python3 -c "from src.data_fetcher import MarketDataFetcher; from src.analytics import MarketAnalytics; f=MarketDataFetcher(); df=f.generate_stock_prices('TEST',days=50); a=MarketAnalytics(); r=a.generate_summary_report(df,'TEST'); print(f'✓ Mean: \$${r[\"mean_price\"]:.2f}, Volatility: {r[\"volatility_annual\"]:.2%}')"
	@echo ""
	@echo "Test 3: OCaml Module"
	@cd ocaml_analytics && ./analytics.exe > /dev/null && echo "✓ OCaml module working"
	@echo ""
	@echo "✅ All tests passed!"

# Run basic analysis
run:
	@echo "📊 Running basic analysis..."
	python3 main.py --symbol DEMO --days 100 --no-plot

# Run with visualization
run-viz:
	@echo "📊 Running analysis with visualization..."
	python3 main.py --symbol DEMO --days 100

# Run multi-stock comparison
run-multi:
	@echo "📊 Comparing multiple stocks..."
	python3 main.py --symbols AAPL GOOGL MSFT --days 100 --no-plot

# Run with OCaml integration
run-ocaml:
	@echo "📊 Running with OCaml integration..."
	python3 main.py --symbol DEMO --days 50 --no-plot --use-ocaml

# Create dashboard
dashboard:
	@echo "📊 Creating comprehensive dashboard..."
	python3 main.py --symbol DEMO --dashboard

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf ocaml_analytics/_build
	rm -f ocaml_analytics/*.exe
	rm -f ocaml_analytics/*.cmi
	rm -f ocaml_analytics/*.cmx
	rm -f ocaml_analytics/*.o
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Cleaned"

# Help target
help:
	@echo "Market Data Analyzer - Makefile Commands"
	@echo "=========================================="
	@echo ""
	@echo "Setup & Build:"
	@echo "  make all          - Install dependencies and build OCaml module"
	@echo "  make install      - Install Python dependencies"
	@echo "  make build-ocaml  - Build OCaml analytics module"
	@echo ""
	@echo "Run & Test:"
	@echo "  make demo         - Run comprehensive demonstration"
	@echo "  make test         - Run test suite"
	@echo "  make run          - Run basic analysis (no plots)"
	@echo "  make run-viz      - Run analysis with visualization"
	@echo "  make run-multi    - Compare multiple stocks"
	@echo "  make run-ocaml    - Run with OCaml integration"
	@echo "  make dashboard    - Create comprehensive dashboard"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean        - Remove build artifacts"
	@echo "  make help         - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make all          # Setup everything"
	@echo "  make demo         # Quick demo"
	@echo "  make test         # Verify installation"
