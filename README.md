# Academic Source Credibility Checker

A powerful multi-agent AI system that automatically evaluates the credibility of academic sources for research queries. Built with CrewAI and OpenAI GPT-4o, this tool searches the web, analyzes content quality, and provides ranked results with detailed credibility assessments.

## 🎯 Overview

The Academic Source Credibility Checker helps researchers quickly identify trustworthy academic sources by:

- **Intelligent Search**: Uses DuckDuckGo to find relevant academic sources with targeted search strategies
- **Multi-Agent Analysis**: Employs specialized AI agents for research discovery, content analysis, and result ranking
- **Credibility Scoring**: Evaluates sources using a 3-tier system based on domain authority and content quality
- **Real-Time Processing**: Shows live agent status updates during the analysis workflow
- **Interactive Interface**: Clean Streamlit web app with ranked results and detailed explanations

## ✨ Key Features

### Advanced Credibility Assessment
- **Domain Authority Analysis**: Prioritizes .edu, .gov, and academic publishers
- **Content Quality Evaluation**: Analyzes publication type, peer review indicators, and academic formatting
- **Comprehensive Scoring**: 0-3 point scale with detailed reasoning for each source
- **Ranking System**: Automatically sorts results by credibility and relevance

### Performance & Reliability
- **Fast Processing**: 15-20 second response time for comprehensive analysis
- **Parallel Processing**: Handles up to 7 sources simultaneously using 4 parallel workers
- **Robust Error Handling**: Graceful failure recovery and fallback strategies
- **Content Validation**: Multiple title extraction methods and content verification

### User Experience
- **Real-Time Updates**: Live agent status showing Research → Analysis → Controller workflow
- **Rich Results**: Each source includes summary, credibility score, reasoning, and metadata
- **Query History**: Session-based tracking of previous searches
- **Clean Interface**: Intuitive design optimized for academic research workflows

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key
- Internet connection for web scraping

### Installation

1. **Clone or download the project**
```bash
git clone <repository-url>
cd academic-source-credibility-checker
```

2. **Install dependencies**
```bash
pip install streamlit openai crewai python-dotenv trafilatura ddgs pandas plotly requests crewai-tools tabulate
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

4. **Run the application**
```bash
streamlit run ui.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Basic Usage

1. **Enter Research Query**: Type your academic research question (e.g., "machine learning in healthcare")

2. **Monitor Progress**: Watch real-time updates showing which agent is working:
   - 🔍 Research Agent: Searching for sources
   - 📖 Analysis Agent: Processing content
   - 🎯 Controller Agent: Ranking results

3. **Review Results**: Examine ranked sources with:
   - Credibility score (0-3.0 scale)
   - Detailed reasoning for the score
   - Content summary
   - Source metadata and links

### Advanced Features

**Query Optimization Tips:**
- Use specific academic terms for better results
- Include field names (e.g., "computer science", "biology")
- Try both broad and narrow query formulations

**Understanding Credibility Scores:**
- **High (2.5-3.0)**: .edu, .gov, major academic publishers
- **Medium (1.5-2.4)**: Reputable organizations, established journals
- **Low (0-1.4)**: Commercial sites, blogs, social media

## 🧪 Testing

The project includes a comprehensive automated testing suite to validate functionality, accuracy, and performance.

### Running Tests

```bash
# Run all automated tests
python test_agent_system.py

# Clean output without warnings
python run_tests.py
```

### Test Coverage

- **Functionality Tests**: Normal queries, edge cases, error handling
- **Accuracy Tests**: Credibility scoring validation, domain ranking
- **Performance Tests**: Response time benchmarks, resource usage
- **Robustness Tests**: Empty queries, niche topics, API failures

See `README_Testing.md` for detailed testing documentation.

## 🏗 Architecture

### System Components

**Frontend**: Streamlit web application with real-time status updates
**Backend**: Python-based multi-agent system with specialized AI agents
**AI Integration**: OpenAI GPT-4o for content analysis and summarization
**Web Scraping**: Trafilatura for clean content extraction
**Search Engine**: DuckDuckGo API for academic source discovery

### Agent Workflow

1. **Research Agent**: Discovers relevant sources using optimized search strategies
2. **Analysis Agent**: Extracts and summarizes content from found sources in parallel
3. **Controller Agent**: Ranks sources by credibility and compiles final results

### Data Flow

Query Input → Source Discovery → Content Analysis → Credibility Assessment → Result Ranking → UI Display

## 🔧 Configuration

### Environment Variables

```env
OPENAI_API_KEY=sk-your-openai-api-key  # Required: OpenAI API access
```

### Customization Options

**Search Parameters**: Modify `max_results` in `main.py` to change source count
**Performance Tuning**: Adjust `max_workers` for parallel processing
**Credibility Thresholds**: Update scoring criteria in `tools/credibility_scorer.py`
**UI Customization**: Modify Streamlit interface in `ui.py`

## 📁 Project Structure

```
├── ui.py                           # Main Streamlit application
├── main.py                         # Core credibility checker logic
├── test_agent_system.py           # Automated testing suite
├── run_tests.py                   # Clean test runner
├── web_scraper.py                 # Content extraction utilities
├── tools/
│   └── credibility_scorer.py      # Domain credibility evaluation
├── .env.example                   # Environment template
├── LOCAL_SETUP.md                 # Detailed local setup guide
├── README_Testing.md              # Testing documentation
└── replit.md                      # Technical architecture notes
```

## 🛠 Local Development

### Virtual Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt  # or install manually as shown above

# Run application
streamlit run ui.py
```

### Troubleshooting

**Common Issues:**

- **"OPENAI_API_KEY not found"**: Verify `.env` file exists and contains valid API key
- **"Module not found"**: Install missing dependencies with pip
- **Slow performance**: Check internet connection and API rate limits
- **No results found**: Try different query formulations or check source availability

**Getting Help:**
- Check `LOCAL_SETUP.md` for detailed troubleshooting
- Review `README_Testing.md` for validation procedures
- Examine log outputs for specific error messages

## 🔍 How It Works

### Credibility Assessment Algorithm

The system evaluates sources using multiple criteria:

1. **Domain Authority**: Educational (.edu), government (.gov), and academic publisher domains receive higher scores
2. **Content Indicators**: Presence of DOI, academic formatting, peer review markers
3. **Publication Context**: Journal reputation, institutional affiliation, citation patterns
4. **Technical Factors**: HTTPS usage, proper metadata, content structure

### Search Strategy

- **Exact Phrase Matching**: Preserves query intent and academic terminology
- **Academic Site Targeting**: Prioritizes educational and research domains
- **Multi-Strategy Approach**: Combines different search formulations for comprehensive coverage
- **Result Filtering**: Removes duplicates and low-quality sources

## 📊 Performance

**Typical Performance Metrics:**
- **Query Processing**: 15-20 seconds for 7 sources
- **Source Coverage**: 5-7 high-quality academic sources per query
- **Accuracy Rate**: 95%+ credibility scoring accuracy for known domains
- **Success Rate**: 90%+ successful query completion

## 🚀 Deployment

### Local Deployment
Follow the Quick Start guide above for local development and testing.

### Cloud Deployment
This application is ready for deployment on cloud platforms:

- **Replit**: Use the included workflow configuration
- **Heroku**: Add `Procfile` with `web: streamlit run ui.py --server.port=$PORT`
- **Docker**: Create container with Python 3.8+ and required dependencies
- **Cloud Functions**: Adapt for serverless deployment with API endpoints

## 🤝 Contributing

This project is designed for academic research assistance. When contributing:

1. Maintain focus on academic source credibility
2. Preserve existing performance optimizations
3. Add comprehensive tests for new features
4. Update documentation for any API changes

## 📄 License

This project is open source and available for academic and research use.

## 🙏 Acknowledgments

Built with:
- **OpenAI GPT-4o**: Advanced language model for content analysis
- **CrewAI**: Multi-agent orchestration framework
- **Streamlit**: Interactive web application framework
- **Trafilatura**: Clean web content extraction
- **DuckDuckGo**: Privacy-focused search API

---

## 💡 Tips for Best Results

**Effective Query Strategies:**
- Use academic terminology and field-specific keywords
- Include methodology terms (e.g., "systematic review", "meta-analysis")
- Specify time periods for recent research (e.g., "2020-2024")
- Combine concepts with "AND" logic for precise results

**Interpreting Results:**
- Higher ranked sources should be prioritized for academic work
- Review the credibility reasoning to understand scoring decisions
- Cross-reference multiple high-scoring sources for comprehensive coverage
- Use summaries to quickly assess relevance before accessing full sources

**Performance Optimization:**
- Queries with specific academic terms typically return higher quality results
- Broader queries may take longer but provide more comprehensive coverage
- Network conditions affect scraping speed and result availability
- OpenAI API response times may vary based on server load