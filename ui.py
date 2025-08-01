"""
Streamlit UI for Academic Source Credibility Checker
Interactive web interface with real-time updates
"""

import streamlit as st
import time
import json
from datetime import datetime
import plotly.express as px
import pandas as pd

from main import CredibilityChecker


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'credibility_checker' not in st.session_state:
        st.session_state.credibility_checker = CredibilityChecker()
    
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []
    
    if 'current_results' not in st.session_state:
        st.session_state.current_results = None
    
    if 'processing' not in st.session_state:
        st.session_state.processing = False


def display_header():
    """Display the main header and description."""
    st.set_page_config(
        page_title="Academic Source Credibility Checker",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("🎓 Academic Source Credibility Checker")
    st.markdown("""
    **AI-Powered Multi-Agent System for Academic Research**
    
    This tool uses CrewAI orchestration to evaluate the credibility of academic sources. 
    Enter your research query below and watch as our specialized agents work together to 
    find, analyze, and rank the most credible sources for your research.
    """)


def display_query_interface():
    """Display the query input interface."""
    st.subheader("🔍 Research Query")
    
    # Query input
    query = st.text_input(
        "Enter your research topic or question:",
        placeholder="e.g., 'Impact of AI on Education', 'Climate Change Effects on Agriculture'",
        help="Be specific about your research topic for better results"
    )
    
    # Search button
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        search_clicked = st.button("🚀 Start Analysis", type="primary", disabled=st.session_state.processing)
    
    with col2:
        if st.button("📚 Example Query"):
            st.session_state.example_query = "Impact of artificial intelligence on higher education"
            st.rerun()
    
    # Handle example query
    if hasattr(st.session_state, 'example_query'):
        query = st.session_state.example_query
        delattr(st.session_state, 'example_query')
        st.rerun()
    
    return query, search_clicked


def display_real_time_status():
    """Display real-time status updates during processing."""
    if st.session_state.processing:
        st.subheader("⚡ Real-Time Agent Execution")
        
        # Create containers for status updates
        status_container = st.empty()
        progress_bar = st.progress(0)
        
        # Store containers in session state for access from main.py
        st.session_state.status_container = status_container
        
        return status_container, progress_bar
    
    return None, None


def display_results(results_data):
    """Display the ranked results in an attractive format."""
    if not results_data or not results_data.get('success'):
        if results_data and 'error' in results_data:
            st.error(f"❌ Error: {results_data['error']}")
        return
    
    results = results_data.get('results', [])
    query = results_data.get('query', '')
    
    if not results:
        st.warning("No sources found for your query. Please try a different search term.")
        return
    
    st.subheader(f"📊 Top {len(results)} Credible Sources for: '{query}'")
    
    # Display credibility score chart
    if len(results) > 1:
        display_credibility_chart(results)
    
    # Display individual source cards
    for i, source in enumerate(results):
        display_source_card(source, i)
    
    # Display summary statistics
    display_summary_stats(results)


def display_credibility_chart(results):
    """Display a bar chart of credibility scores."""
    st.subheader("📈 Credibility Score Comparison")
    
    # Prepare data for chart
    chart_data = pd.DataFrame({
        'Source': [f"#{source['rank']} {source['title'][:30]}..." if len(source['title']) > 30 
                  else f"#{source['rank']} {source['title']}" for source in results],
        'Credibility Score': [source['credibility_score'] for source in results],
        'Rank': [source['rank'] for source in results]
    })
    
    # Create bar chart
    fig = px.bar(
        chart_data, 
        x='Credibility Score', 
        y='Source',
        orientation='h',
        title="Source Credibility Scores",
        color='Credibility Score',
        color_continuous_scale='RdYlGn',
        range_color=[0, 3]
    )
    
    fig.update_layout(
        height=max(300, len(results) * 60),
        yaxis={'categoryorder': 'total ascending'}
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_source_card(source, index):
    """Display an individual source card."""
    # Determine credibility level and color
    score = source['credibility_score']
    if score >= 2.5:
        credibility_level = "HIGH"
        score_color = "🟢"
    elif score >= 1.5:
        credibility_level = "MEDIUM"
        score_color = "🟡"
    else:
        credibility_level = "LOW"
        score_color = "🔴"
    
    # Create expandable card
    with st.expander(f"#{source['rank']} {source['title']}", expanded=(index < 3)):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**URL:** [{source['url']}]({source['url']})")
            st.markdown(f"**Summary:** {source['summary']}")
            st.markdown(f"**Credibility Analysis:** {source['credibility_reason']}")
            
        with col2:
            st.metric(
                label="Credibility Score",
                value=f"{score}/3.0",
                delta=credibility_level
            )
            st.markdown(f"{score_color} **{credibility_level}**")
            
            if not source.get('content_available', True):
                st.warning("⚠️ Content extraction limited")


def display_summary_stats(results):
    """Display summary statistics about the results."""
    st.subheader("📋 Analysis Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_score = sum(r['credibility_score'] for r in results) / len(results)
        st.metric("Average Score", f"{avg_score:.2f}/3.0")
    
    with col2:
        high_cred = len([r for r in results if r['credibility_score'] >= 2.5])
        st.metric("High Credibility", f"{high_cred}/{len(results)}")
    
    with col3:
        med_cred = len([r for r in results if 1.5 <= r['credibility_score'] < 2.5])
        st.metric("Medium Credibility", f"{med_cred}/{len(results)}")
    
    with col4:
        low_cred = len([r for r in results if r['credibility_score'] < 1.5])
        st.metric("Low Credibility", f"{low_cred}/{len(results)}")


def display_query_history():
    """Display previous queries in sidebar."""
    if st.session_state.query_history:
        st.sidebar.subheader("📚 Recent Queries")
        
        for i, hist_item in enumerate(reversed(st.session_state.query_history[-5:])):
            query = hist_item['query']
            timestamp = hist_item['timestamp']
            
            if st.sidebar.button(f"🔄 {query[:30]}..." if len(query) > 30 else f"🔄 {query}", 
                               key=f"hist_{i}"):
                st.session_state.current_results = hist_item
                st.rerun()


def save_to_history(query, results_data):
    """Save query and results to history."""
    history_item = {
        'query': query,
        'results': results_data,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    st.session_state.query_history.append(history_item)
    
    # Keep only last 10 queries
    if len(st.session_state.query_history) > 10:
        st.session_state.query_history = st.session_state.query_history[-10:]


def main():
    """Main Streamlit application."""
    initialize_session_state()
    display_header()
    
    # Sidebar with additional information
    st.sidebar.title("ℹ️ About This Tool")
    st.sidebar.markdown("""
    **How it works:**
    1. 🔍 **Search** uses multiple strategies for precise results
    2. 📖 **Analysis** evaluates content & credibility  
    3. 🎯 **Ranking** sorts by credibility scores
    
    **Search Tips:**
    - Use specific technical terms (e.g., "two tower models")
    - Try academic concepts (e.g., "transformer architecture")
    - Research topics work best (e.g., "climate change impacts")
    
    **Credibility Scoring:**
    - 🟢 **High (2.5-3.0):** .edu, .gov, academic publishers
    - 🟡 **Medium (1.5-2.4):** .org, news outlets, established sites
    - 🔴 **Low (0-1.4):** Blogs, social media, unverified sources
    """)
    
    display_query_history()
    
    # Main interface
    query, search_clicked = display_query_interface()
    
    # Handle search
    if search_clicked and query.strip():
        st.session_state.processing = True
        st.session_state.current_results = None
        st.rerun()
    
    # Process query if needed
    if st.session_state.processing and query.strip():
        status_container, progress_bar = display_real_time_status()
        
        try:
            # Update progress
            if progress_bar:
                progress_bar.progress(20)
            
            # Process the query
            results_data = st.session_state.credibility_checker.process_query(query)
            
            if progress_bar:
                progress_bar.progress(100)
            
            # Save results
            st.session_state.current_results = results_data
            save_to_history(query, results_data)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            results_data = {
                'success': False,
                'error': str(e),
                'query': query
            }
            st.session_state.current_results = results_data
        
        finally:
            st.session_state.processing = False
            time.sleep(1)  # Brief pause before rerun
            st.rerun()
    
    # Display results
    if st.session_state.current_results:
        display_results(st.session_state.current_results)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **🎓 Academic Source Credibility Checker** - Powered by CrewAI Multi-Agent System & OpenAI GPT-4o
    
    *This tool helps researchers evaluate source credibility but should not replace critical thinking and manual verification.*
    """)


if __name__ == "__main__":
    main()
