"""
Custom credibility scoring tool for academic sources.
Evaluates URLs based on domain authority and provides reasoning.
"""

import re
from urllib.parse import urlparse
def credibility_scorer(url: str) -> dict:
    """
    Enhanced credibility evaluation based on comprehensive domain analysis,
    content indicators, and academic authority metrics.
    
    Args:
        url: The URL to evaluate
        
    Returns:
        dict: Contains 'score' (float 0-3) and 'reason' (str) explaining the score
    """
    
    if not url or not isinstance(url, str):
        return {
            'score': 0.0,
            'reason': 'Invalid URL provided'
        }
    
    try:
        parsed = urlparse(url.lower())
        domain = parsed.netloc.lower()
        
        # Remove www prefix if present
        if domain.startswith('www.'):
            domain = domain[4:]
            
    except Exception:
        return {
            'score': 0.5,
            'reason': 'Unable to parse domain from URL'
        }
    
    score = 1.0  # Base score
    reasons = []
    
    # Tier 1: Highest credibility - Academic and government institutions
    tier1_domains = {
        '.edu': 'Educational institution',
        '.gov': 'Government source',
        'arxiv.org': 'Academic preprint repository',
        'pubmed.ncbi.nlm.nih.gov': 'Medical literature database',
        'scholar.google': 'Academic search engine',
        'ieee.org': 'Professional engineering society',
        'acm.org': 'Computing machinery association',
        'nature.com': 'Premier science journal',
        'science.org': 'AAAS Science journal',
        'cell.com': 'Life sciences journal',
        'nejm.org': 'Medical journal',
        'thelancet.com': 'Medical journal'
    }
    
    # Tier 2: High credibility - Academic publishers and research institutions
    tier2_domains = {
        'springer.com': 'Academic publisher',
        'sciencedirect.com': 'Scientific database',
        'jstor.org': 'Academic archive',
        'plos.org': 'Open access publisher',
        'wiley.com': 'Academic publisher',
        'tandfonline.com': 'Academic publisher',
        'cambridge.org': 'University press',
        'oup.com': 'Oxford University Press',
        'researchgate.net': 'Academic network',
        'semanticscholar.org': 'AI-powered research tool',
        'osti.gov': 'Science and technology info',
        'nist.gov': 'National Institute of Standards'
    }
    
    # Tier 3: Medium credibility - Reputable organizations and institutions
    tier3_domains = {
        '.org': 'Non-profit organization',
        'who.int': 'World Health Organization',
        'nih.gov': 'National Institutes of Health',
        'cdc.gov': 'Centers for Disease Control',
        'nasa.gov': 'NASA',
        'unesco.org': 'UNESCO',
        'oecd.org': 'OECD',
        'worldbank.org': 'World Bank',
        'reuters.com': 'News agency',
        'bbc.com': 'Public broadcaster',
        'npr.org': 'Public radio'
    }
    
    # Low credibility indicators
    low_credibility = {
        'blog': 'Personal blog',
        'wordpress': 'Blog platform',
        'medium.com': 'Publishing platform',
        'facebook.com': 'Social media',
        'twitter.com': 'Social media',
        'instagram.com': 'Social media',
        'tiktok.com': 'Social media',
        'reddit.com': 'Forum',
        'quora.com': 'Q&A platform',
        'yahoo.com': 'Web portal',
        'answers.com': 'Q&A site'
    }
    
    # Check credibility tiers
    domain_matched = False
    
    # Tier 1 check (highest credibility)
    for indicator, description in tier1_domains.items():
        if indicator in domain:
            score += 2.0
            reasons.append(f"Tier 1: {description}")
            domain_matched = True
            break
    
    # Tier 2 check (high credibility)
    if not domain_matched:
        for indicator, description in tier2_domains.items():
            if indicator in domain:
                score += 1.5
                reasons.append(f"Tier 2: {description}")
                domain_matched = True
                break
    
    # Tier 3 check (medium credibility)
    if not domain_matched:
        for indicator, description in tier3_domains.items():
            if indicator in domain:
                score += 0.8
                reasons.append(f"Tier 3: {description}")
                domain_matched = True
                break
    
    # Check for low credibility indicators
    for indicator, description in low_credibility.items():
        if indicator in domain:
            score -= 1.2
            reasons.append(f"Low tier: {description}")
            break
    
    # Additional scoring factors
    if 'https' in url:
        score += 0.1
        reasons.append("Secure connection")
    
    # Path analysis for academic content
    path = parsed.path.lower()
    academic_indicators = ['paper', 'article', 'research', 'study', 'journal', 'publication', 'doi', 'abstract']
    if any(term in path for term in academic_indicators):
        score += 0.3
        reasons.append("Academic content path")
    
    # File type analysis
    if any(ext in path for ext in ['.pdf', '.doc', '.docx']):
        score += 0.2
        reasons.append("Document format")
    
    # DOI presence (Digital Object Identifier)
    if 'doi' in url or 'dx.doi.org' in url:
        score += 0.4
        reasons.append("DOI identifier present")
    
    # Subdomain analysis for institutional content
    if any(sub in domain for sub in ['research.', 'library.', 'academic.', 'scholar.']):
        score += 0.2
        reasons.append("Academic subdomain")
    
    # Ensure score is within bounds
    score = max(0.0, min(3.0, score))
    
    # Generate detailed explanation
    if score >= 2.5:
        credibility_level = "High"
        emoji = "🟢"
    elif score >= 1.5:
        credibility_level = "Medium"
        emoji = "🟡"
    else:
        credibility_level = "Low"
        emoji = "🔴"
    
    reason = f"{emoji} {credibility_level} credibility ({score:.1f}/3.0): {', '.join(reasons) if reasons else 'Standard web source'}"
    
    return {
        'score': round(score, 1),
        'reason': reason
    }