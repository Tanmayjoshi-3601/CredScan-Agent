import trafilatura
import requests
import re
from urllib.parse import urljoin, urlparse, unquote
import time


def get_website_text_content(url: str) -> str:
    """
    This function takes a url and returns the main text content of the website.
    The text content is extracted using trafilatura and easier to understand.
    The results is not directly readable, better to be summarized by LLM before consume
    by the user.
    """
    try:
        # Send a request to the website
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded)
            return text if text else "No content could be extracted from this URL"
        else:
            return "Failed to fetch content from URL"
    except Exception as e:
        return f"Error extracting content: {str(e)}"


def get_page_title(url: str) -> str:
    """
    Extract the title of a webpage with multiple fallback strategies.
    """
    try:
        # Strategy 1: Use trafilatura for content extraction
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            # Try to extract title using trafilatura metadata
            metadata = trafilatura.extract_metadata(downloaded)
            if metadata and metadata.title and metadata.title.strip():
                return metadata.title.strip()
            
            # Strategy 2: Look for title tag in HTML
            title_patterns = [
                r'<title[^>]*>([^<]+)</title>',
                r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']',
                r'<meta[^>]*name=["\']title["\'][^>]*content=["\']([^"\']+)["\']',
                r'<h1[^>]*>([^<]+)</h1>'
            ]
            
            for pattern in title_patterns:
                title_match = re.search(pattern, downloaded, re.IGNORECASE | re.DOTALL)
                if title_match:
                    title = title_match.group(1).strip()
                    if title and len(title) > 5:  # Ensure meaningful title
                        return title
        
        # Strategy 3: Try requests with headers for better access
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                title_match = re.search(r'<title[^>]*>([^<]+)</title>', response.text, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1).strip()
                    if title and len(title) > 5:
                        return title
        except:
            pass
            
        # Strategy 4: Extract from URL path as last resort
        parsed = urlparse(url)
        if parsed.path:
            path_parts = parsed.path.strip('/').split('/')
            if path_parts and path_parts[-1]:
                # Clean up the last path component
                filename = unquote(path_parts[-1])
                # Remove file extensions and clean up
                title = re.sub(r'\.[a-z]{2,4}$', '', filename, flags=re.IGNORECASE)
                title = re.sub(r'[-_]', ' ', title)
                if len(title) > 5:
                    return title.title()
                    
        return "Document from " + urlparse(url).netloc
        
    except Exception as e:
        return f"Content from {urlparse(url).netloc if url else 'unknown source'}"


def safe_extract_content(url: str, max_length: int = 3000) -> dict:
    """
    Safely extract content from a URL with error handling and length limits.
    
    Returns:
        dict: Contains 'title', 'content', 'url', and 'success' status
    """
    try:
        # Add delay to be respectful to websites
        time.sleep(0.5)
        
        title = get_page_title(url)
        content = get_website_text_content(url)
        
        # Limit content length for processing
        if content and len(content) > max_length:
            content = content[:max_length] + "... [content truncated]"
        
        return {
            'title': title,
            'content': content if content else "No content available",
            'url': url,
            'success': True
        }
        
    except Exception as e:
        return {
            'title': "Error",
            'content': f"Failed to extract content: {str(e)}",
            'url': url,
            'success': False
        }
