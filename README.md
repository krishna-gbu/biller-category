# 📄 PDF to Excel Converter

A FastAPI application that converts credit card statements from PDF to Excel using LLM processing.

## 🚀 Features

- **PDF Text Extraction**: Uses PyMuPDF for reliable text extraction
- **LLM Processing**: OpenAI GPT-4 for intelligent transaction categorization
- **Excel Output**: Structured Excel files with multiple sheets
- **REST API**: FastAPI endpoints for easy integration
- **File Management**: Upload, download, and manage processed files
- **Comprehensive Categories**: 15+ transaction categories with subcategories

## 📋 Prerequisites

- Python 3.9+
- [`uv`](https://github.com/astral-sh/uv) package manager
- OpenAI API key

## 🛠️ Setup & Installation

### 1. Install uv (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

### 2. Create Virtual Environment
```bash
uv venv .venv
```

### 3. Install Dependencies
```bash
uv pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
# Create .env file
echo "OPENAI_API_KEY=your-actual-api-key-here" > .env

# Edit the .env file and replace with your real API key
nano .env
# or
code .env
```

## 🚀 Usage

### Start the FastAPI Server
```bash
# Activate virtual environment and start server
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Access the Application
- **Main API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

### Upload PDF
```bash
curl -X POST "http://localhost:8000/api/v1/upload-pdf" \
     -F "file=@your_statement.pdf"
```

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/upload-pdf` | POST | Upload and process PDF |
| `/api/v1/download/{filename}` | GET | Download Excel file |
| `/api/v1/files` | GET | List processed files |
| `/docs` | GET | Interactive API documentation |

## 🧪 Testing

### Manual Testing with curl
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Upload PDF
curl -X POST "http://localhost:8000/api/v1/upload-pdf" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@statement.pdf"

# List files
curl http://localhost:8000/api/v1/files
```

## 📊 Output Format

The application generates Excel files with three sheets:

1. **Transactions**: All parsed transactions with columns:
   - Date
   - Merchant
   - Amount
   - Category

2. **Summary**: Key statistics:
   - Total transactions
   - Total amount
   - Average transaction
   - Date range
   - Unique categories/merchants

3. **Category Breakdown**: Spending analysis by category

## 🏷️ Transaction Categories

The system categorizes transactions into 15+ categories:

- **🏠 Housing & Utilities**: Rent, electricity, internet, etc.
- **🍽️ Food & Dining**: Restaurants, delivery, groceries
- **🚗 Transportation**: Fuel, ride-sharing, public transport
- **🛍️ Shopping & Retail**: Clothing, electronics, online shopping
- **🏥 Healthcare**: Medical bills, pharmacy, insurance
- **🎮 Entertainment & Leisure**: Movies, streaming, gaming
- **💼 Business & Professional**: Office supplies, software
- **💰 Financial Services**: Banking fees, investments
- **🎓 Education**: Tuition, courses, books
- **💅 Personal Care**: Salons, grooming, beauty
- **🏠 Home & Living**: Furniture, appliances, decor
- **🎁 Gifts & Donations**: Gifts, charity, religious
- **📱 Technology & Digital**: Software, cloud services
- **🌍 Travel & Tourism**: Hotels, travel, international
- **📞 Communication**: Mobile, internet bills
- **🎯 Miscellaneous**: Government, legal, consulting

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)

### File Limits
- Maximum PDF size: 50MB
- Supported formats: PDF only

## 📁 Project Structure

```
bill-project/
├── .venv/                    # Virtual environment
├── .env                      # Environment variables
├── requirements.txt          # Dependencies
├── pyproject.toml           # Project configuration
├── uv.lock                  # Locked dependencies
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── __init__.py          # Package initialization
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints.py # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── pdf_extractor.py # PDF text extraction
│   │   ├── llm_client.py    # OpenAI API client
│   │   └── excel_writer.py  # Excel file generation
│   ├── models/              # Pydantic models (empty)
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── enhanced_prompt.py # LLM prompt template
│   ├── utils/               # Utility functions (empty)
│   └── outputs/             # Generated Excel files
└── README.md               # This file
```

## 🐛 Troubleshooting

### Virtual Environment Issues
```bash
# If you get import errors, make sure you're in the virtual environment
source .venv/bin/activate
```

### API Key Issues
```bash
# Check if API key is loaded
source .venv/bin/activate
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('OPENAI_API_KEY'))"
```

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Common Errors

1. **API Key Not Set**
   ```
   ❌ Please set OPENAI_API_KEY environment variable
   ```
   Solution: Set your OpenAI API key in the .env file

2. **PDF Not Found**
   ```
   ❌ PDF file not found: statement.pdf
   ```
   Solution: Upload a PDF file via the API or place it in the correct location

3. **Server Connection Error**
   ```
   ❌ Cannot connect to server
   ```
   Solution: Make sure the FastAPI server is running on port 8000

4. **File Too Large**
   ```
   ❌ File too large. Maximum size is 50MB
   ```
   Solution: Use a smaller PDF file or compress it

### Debug Mode
```bash
# Run with debug logging
uvicorn app.main:app --reload --log-level debug
```

## 📊 Current Working Versions

| Package | Version | Status |
|---------|---------|--------|
| openai | >=1.0.0 | ✅ Working |
| pandas | 2.1.4 | ✅ Working |
| PyMuPDF | 1.23.8 | ✅ Working |
| FastAPI | 0.104.1 | ✅ Working |
| uvicorn | 0.24.0 | ✅ Working |
| httpx | >=0.25.0 | ✅ Working |
| python-dotenv | 1.0.0 | ✅ Working |
| openpyxl | 3.1.2 | ✅ Working |
| python-multipart | 0.0.6 | ✅ Working |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section
2. Review the API documentation at `http://localhost:8000/docs`
3. Check the logs for error messages
4. Create an issue with detailed information

## 🎯 Example Workflow

1. **Start the server**:
   ```bash
   source .venv/bin/activate
   uvicorn app.main:app --reload
   ```

2. **Upload a PDF**:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/upload-pdf" \
        -F "file=@credit_card_statement.pdf"
   ```

3. **Download the Excel file**:
   ```bash
   curl -L "http://localhost:8000/api/v1/download/credit_card_statement_20231201_143022.xlsx" \
        -o "credit_card_statement_20231201_143022.xlsx"
   ```

4. **View results**:
   - Open the Excel file
   - Check the Transactions sheet for parsed data
   - Review the Summary for statistics
   - Analyze Category Breakdown for spending patterns

---

**Happy processing! 🎉** # biller-category
