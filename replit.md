# Academic Source Credibility Checker - replit.md

## Overview

This is a multi-agent AI system built with CrewAI that evaluates the credibility of academic sources. The application takes research queries, searches for relevant sources, analyzes their content using multiple specialized AI agents, and presents ranked results with credibility scores and reasoning. The system combines web scraping, AI-powered analysis, and an interactive Streamlit interface to provide researchers with quality-assessed academic sources.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a multi-agent orchestration pattern using CrewAI as the core framework:

- **Frontend**: Streamlit web application with real-time status updates and interactive visualizations
- **Backend**: Python-based multi-agent system with specialized AI agents for different tasks
- **AI Integration**: OpenAI GPT models for content analysis and summarization
- **Web Scraping**: Trafilatura for content extraction from academic sources
- **Search**: DuckDuckGo search API for finding relevant sources

The architecture prioritizes modularity and real-time user feedback, with each agent having specific responsibilities in the research workflow.

## Key Components

### Latest Improvements (Current Version)
- **Enhanced Credibility Scoring**: 3-tier system with comprehensive domain analysis and detailed reasoning
- **Improved Title Extraction**: Multiple fallback strategies to eliminate "No title found" issues
- **Increased Source Coverage**: Processing 7 sources (up from 3-5) with 4 parallel workers
- **Agent Status Display**: Clear indication of which agent is working (Research → Analysis → Controller)
- **Better Content Handling**: Robust error handling and content validation
- **Performance**: Maintained 15-20 second response time despite processing more sources

### Core Agents (Enhanced)
- **Research Agent**: DuckDuckGo search with exact phrase matching and academic site targeting
- **Analysis Agent**: Parallel content extraction, summarization, and credibility evaluation
- **Controller Agent**: Source ranking, final processing, and result aggregation

### Tools and Utilities
- **Credibility Scorer**: Custom tool that evaluates source authority based on domain (.edu/.gov vs .com) and provides detailed reasoning
- **Web Scraper**: Safe content extraction using trafilatura with error handling and content length limits
- **Search Tool**: DuckDuckGo integration for academic source discovery

### User Interface
- **Streamlit App**: Interactive web interface with real-time agent status updates
- **Query Interface**: Input system for research queries
- **Results Display**: Ranked source presentation with scores, summaries, and credibility reasoning
- **History Tracking**: Session-based query history management

## Data Flow

1. **User Input**: Research query submitted through Streamlit interface
2. **Agent Orchestration**: Controller agent initiates workflow and delegates tasks
3. **Source Discovery**: Research agent searches for relevant academic sources
4. **Content Analysis**: Analysis agent extracts and summarizes content from found sources
5. **Credibility Assessment**: Custom scoring tool evaluates each source's reliability
6. **Result Aggregation**: Controller agent compiles ranked results with scores and reasoning
7. **UI Presentation**: Real-time status updates and final results displayed to user

The system emphasizes transparency by showing users which agent is currently working and what task they're performing.

## External Dependencies

### AI Services
- **OpenAI API**: GPT models for content analysis and summarization (configured for gpt-4o)
- **CrewAI Framework**: Multi-agent orchestration and task management

### Data Sources
- **DuckDuckGo Search API**: Web search for academic source discovery
- **Web Content**: Direct extraction from academic websites and repositories

### Python Libraries
- **Streamlit**: Web application framework for user interface
- **Trafilatura**: Web content extraction and text processing
- **Plotly**: Data visualization for results presentation
- **Requests**: HTTP client for web scraping operations

## Deployment Strategy

The application is designed for simple deployment with minimal infrastructure requirements:

- **Environment**: Python-based application suitable for cloud platforms
- **Configuration**: Environment variable-based API key management
- **Dependencies**: Standard Python package management via pip
- **Scaling**: Stateless design allows for horizontal scaling if needed

The system uses session state management in Streamlit for user interaction history and doesn't require persistent database storage, making it suitable for serverless or container-based deployment.

Key deployment considerations:
- Requires OpenAI API key configuration
- Web scraping capabilities need internet access
- Streamlit port configuration for web access
- Memory management for content processing and agent operations