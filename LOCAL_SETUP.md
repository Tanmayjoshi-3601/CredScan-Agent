# Local Setup Guide

## Prerequisites

- Python 3.8 or higher
- Git (optional, for cloning)

## Installation Steps

### 1. Download the Project
```bash
# Option A: Clone from repository
git clone <your-repo-url>
cd academic-source-credibility-checker

# Option B: Download and extract the files manually
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install all required packages
pip install streamlit openai crewai python-dotenv trafilatura ddgs pandas plotly requests crewai-tools
```

### 4. Set Up Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your actual API key
# On Windows: notepad .env
# On macOS: open .env
# On Linux: nano .env
```

**Add your OpenAI API key to the .env file:**
```
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

### 5. Run the Application
```bash
# Start the Streamlit app
streamlit run ui.py --server.port 8501
```

The app will open in your browser at `http://localhost:8501`

## Getting OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and paste it in your `.env` file

## Troubleshooting

### Common Issues:

**1. "OPENAI_API_KEY not found" error:**
- Make sure your `.env` file exists in the project root
- Verify the API key is correctly set without quotes
- Restart the application after updating the .env file

**2. Module not found errors:**
- Ensure you're in the correct directory
- Activate your virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

**3. Port already in use:**
- Try a different port: `streamlit run ui.py --server.port 8502`
- Or kill the existing process

**4. Search not working:**
- Check your internet connection
- Some corporate networks may block web scraping

### Alternative Ports:
If port 8501 is busy, try:
```bash
streamlit run ui.py --server.port 8502
streamlit run ui.py --server.port 8503
```

## Project Structure
```
academic-source-credibility-checker/
├── ui.py                 # Main Streamlit interface
├── main.py              # Core credibility checker logic
├── web_scraper.py       # Web content extraction
├── tools/               # Custom tools directory
│   └── credibility_scorer.py
├── .env                 # Your environment variables (create this)
├── .env.example         # Example environment file
└── LOCAL_SETUP.md       # This setup guide
```

## Usage Tips

1. **Search Terms**: Use specific academic terms like "machine learning", "climate change", "quantum computing"
2. **Technical Queries**: Try precise terms like "transformer architecture", "BERT model", "neural networks"
3. **Best Results**: Academic concepts and research topics work best
4. **Wait Time**: Processing takes 15-20 seconds per query

## Performance Notes

- The app uses OpenAI's GPT-4o for content analysis
- Web scraping speed depends on your internet connection
- Processing is optimized with parallel execution
- Results are limited to top 3-5 sources for speed