"""
CrewAI-powered Academic Source Credibility Checker
Multi-agent system for evaluating academic source credibility with real-time updates
"""

import os
import json
import time
import concurrent.futures
from typing import List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from crewai import Agent, Task, Crew, Process
from ddgs import DDGS
from openai import OpenAI
import streamlit as st

from tools.credibility_scorer import credibility_scorer
from web_scraper import safe_extract_content


class CredibilityChecker:
    def __init__(self):
        # Initialize OpenAI client
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        # Get API key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")
        
        self.openai_client = OpenAI(api_key=api_key)
        
        # Initialize search tool  
        self.search_tool = DDGS()
        
        # Initialize agents
        self._setup_agents()
        
        # Status tracking for UI updates
        self.status_updates = []
        
    def _setup_agents(self):
        """Initialize all CrewAI agents with their roles and tools."""
        
        # Controller Agent - orchestrates workflow
        self.controller_agent = Agent(
            role='Research Controller',
            goal='Orchestrate the academic source credibility checking process and aggregate results',
            backstory="""You are an experienced academic research coordinator who manages 
            the entire workflow of evaluating source credibility. You delegate tasks to 
            specialized agents and ensure high-quality, comprehensive results.""",
            verbose=True,
            allow_delegation=True
        )
        
        # Research Agent - finds relevant URLs
        self.research_agent = Agent(
            role='Academic Researcher',
            goal='Find relevant and diverse academic sources for research queries',
            backstory="""You are a skilled academic researcher who excels at finding 
            high-quality, relevant sources across various academic domains. You use 
            advanced search techniques to locate the most credible and comprehensive sources.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Analysis Agent - summarizes and evaluates content
        self.analysis_agent = Agent(
            role='Content Analyst',
            goal='Analyze content quality, generate summaries, and evaluate source credibility',
            backstory="""You are an expert content analyst with deep knowledge of academic 
            standards and source evaluation. You excel at summarizing complex content and 
            assessing the credibility of academic sources based on multiple criteria.""",
            verbose=True,
            allow_delegation=False
        )

    def _update_status(self, message: str):
        """Add status update for UI tracking."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status = f"[{timestamp}] {message}"
        self.status_updates.append(status)
        
        # Update Streamlit UI if available
        if hasattr(st, 'session_state') and 'status_container' in st.session_state:
            st.session_state.status_container.text("\n".join(self.status_updates[-5:]))

    def search_academic_sources(self, query: str, max_results: int = 7) -> List[Dict[str, str]]:
        """Search for academic sources using DuckDuckGo with optimized strategies."""
        try:
            results = []
            # Prioritize most effective search strategies for speed
            search_queries = [
                f'"{query}" academic research',  # Exact phrase search first
                f'{query} site:arxiv.org OR site:ieee.org OR site:acm.org',  # Academic sites
                f'{query} filetype:pdf academic',  # Academic PDFs
            ]
            
            seen_urls = set()
            
            # Try top strategies only for speed
            for i, search_query in enumerate(search_queries):
                if len(results) >= max_results:
                    break
                    
                try:
                    search_results = self.search_tool.text(
                        search_query,
                        max_results=max_results - len(results)
                    )
                    
                    for result in search_results:
                        url = result.get('href', '')
                        if url and url not in seen_urls:
                            seen_urls.add(url)
                            results.append({
                                'url': url,
                                'title': result.get('title', ''),
                                'snippet': result.get('body', ''),
                                'source': f'Strategy {i+1}'
                            })
                            
                except Exception:
                    continue
                    
            # Quick fallback if needed
            if not results:
                try:
                    fallback_results = self.search_tool.text(query, max_results=max_results)
                    for result in fallback_results:
                        results.append({
                            'url': result.get('href', ''),
                            'title': result.get('title', ''),
                            'snippet': result.get('body', ''),
                            'source': 'Fallback'
                        })
                except Exception:
                    pass
                    
            return results[:max_results]
            
        except Exception as e:
            self._update_status(f"❌ Search error: {str(e)}")
            return []

    def summarize_content(self, content: str, title: str = "") -> str:
        """Summarize content using OpenAI GPT-4o."""
        try:
            prompt = f"""Please provide a concise, academic summary of the following content.
            Focus on the main arguments, key findings, and relevance to academic research.
            
            Title: {title}
            Content: {content[:2000]}"""  # Limit content length
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            return content.strip() if content else "No summary available"
            
        except Exception as e:
            return f"Summary unavailable: {str(e)}"

    def create_tasks(self, query: str) -> List[Task]:
        """Create tasks for the crew based on the research query."""
        
        # Task 1: Research - Find relevant URLs
        research_task = Task(
            description=f"""Find 5-7 relevant and diverse academic sources for the research query: "{query}"
            
            Focus on:
            - Academic papers and journals
            - Educational institution resources
            - Government and official organization reports
            - Reputable research organizations
            
            For each source found, provide:
            - URL
            - Brief description/snippet
            - Source type (academic, government, organization, etc.)
            
            Return results in a structured format that can be easily processed by the analysis agent.""",
            expected_output="List of 5-7 relevant URLs with descriptions and source types",
            agent=self.research_agent
        )
        
        # Task 2: Analysis - Content extraction and credibility evaluation
        analysis_task = Task(
            description=f"""For each URL provided by the research agent:
            
            1. Extract and analyze the content quality
            2. Generate a concise academic summary
            3. Evaluate credibility using the credibility_scorer tool
            4. Assess relevance to the query: "{query}"
            
            Provide structured output with:
            - URL
            - Title
            - Summary (2-3 sentences)
            - Credibility score and reasoning
            - Relevance assessment
            
            Focus on academic rigor and source reliability.""",
            expected_output="Detailed analysis of each source with summaries, credibility scores, and reasoning",
            agent=self.analysis_agent,
            context=[research_task]
        )
        
        # Task 3: Controller - Aggregate and rank results
        controller_task = Task(
            description=f"""Aggregate and rank the analyzed sources based on:
            
            1. Credibility score (primary factor)
            2. Relevance to query: "{query}"
            3. Content quality and depth
            4. Source diversity
            
            Provide final ranking with:
            - Top 5 most credible and relevant sources
            - Clear explanation of ranking criteria
            - Summary of overall source landscape for this topic
            
            Format the output for presentation to academic researchers.""",
            expected_output="Ranked list of top 5 sources with detailed explanations and overall assessment",
            agent=self.controller_agent,
            context=[research_task, analysis_task]
        )
        
        return [research_task, analysis_task, controller_task]

    def process_query(self, query: str) -> dict:
        """Process a research query with direct search implementation for speed."""
        
        self._update_status("🚀 Starting academic source credibility check...")
        self.status_updates = []  # Reset status updates
        
        try:
            # Direct processing without CrewAI agents to avoid delegation loops
            processed_results = self._process_crew_results(None, query)
            
            self._update_status("🎉 Academic source credibility check completed!")
            
            return {
                'success': True,
                'query': query,
                'results': processed_results,
                'timestamp': datetime.now().isoformat(),
                'status_updates': self.status_updates
            }
            
        except Exception as e:
            error_message = f"Error processing query: {str(e)}"
            self._update_status(f"❌ Error: {error_message}")
            
            return {
                'success': False,
                'query': query,
                'error': error_message,
                'timestamp': datetime.now().isoformat(),
                'status_updates': self.status_updates
            }

    def _process_crew_results(self, crew_result, query: str) -> List[Dict[str, Any]]:
        """Process and structure the crew results for UI display."""
        
        # Agent 1: Research Agent - Academic Source Discovery
        self._update_status(f"🔍 Research Agent: Searching for '{query}'...")
        search_results = self.search_academic_sources(query, max_results=7)
        
        self._update_status(f"✅ Research Agent: Found {len(search_results)} potential sources")
        
        # Agent 2: Analysis Agent - Content Processing & Evaluation
        self._update_status(f"📖 Analysis Agent: Processing {len(search_results)} sources for credibility...")
        
        if not search_results:
            self._update_status("❌ No search results found")
            return []
        
        processed_sources = []
        
        # Process sources in parallel for speed
        import concurrent.futures
        
        def process_single_source(result_with_index):
            i, result = result_with_index
            url = result['url']
            
            # Get credibility score first (fast)
            cred_result = credibility_scorer(url)
            
            # Extract content (potentially slow)
            content_data = safe_extract_content(url)
            
            # Generate summary using OpenAI (fast with shorter content)
            content_to_summarize = content_data['content'][:1500] if content_data['content'] else "No content available for summarization"
            summary = self.summarize_content(
                content_to_summarize,
                content_data['title']
            )
            
            return {
                'rank': i + 1,
                'title': content_data['title'] if content_data['title'] != "Error" else result['title'],
                'url': url,
                'summary': summary,
                'credibility_score': cred_result['score'],
                'credibility_reason': cred_result['reason'],
                'content_available': content_data['success']
            }
        
        # Process up to 7 sources in parallel for comprehensive results
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            results_with_index = [(i, result) for i, result in enumerate(search_results[:7])]
            processed_sources = list(executor.map(process_single_source, results_with_index))
        
        # Agent 3: Controller Agent - Ranking & Final Processing  
        self._update_status(f"🎯 Controller Agent: Ranking {len(processed_sources)} sources by credibility...")
        
        # Sort by credibility score (descending)
        processed_sources.sort(key=lambda x: x['credibility_score'], reverse=True)
        
        # Update ranks after sorting
        for i, source in enumerate(processed_sources):
            source['rank'] = i + 1
        
        self._update_status(f"✅ Controller Agent: Analysis complete! Top source: {processed_sources[0]['credibility_score']:.1f}/3.0" if processed_sources else "❌ No sources processed successfully")
        
        return processed_sources

    def _extract_urls_from_text(self, text: str) -> List[str]:
        """Extract URLs from text using regex."""
        import re
        
        # Pattern to match URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, text)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_urls = []
        for url in urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)
        
        return unique_urls


# Global instance for Streamlit
if 'credibility_checker' not in st.session_state:
    st.session_state.credibility_checker = CredibilityChecker()
