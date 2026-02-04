import httpx
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

# Common headers to mimic a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
}

def clean_text(text: str) -> str:
    """Helper to clean whitespace."""
    if not text:
        return ""
    # Replace multiple newlines with single
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n\n".join(lines)

def fetch_article_content(url: str) -> str:
    """
    Fetches the HTML content of a URL and extracts the main article text using BeautifulSoup.
    Returns the cleaned text content or empty string if failed.
    """
    try:
        # verify=False to bypass SSL errors (WRONG_VERSION_NUMBER) caused by proxies or legacy servers
        with httpx.Client(timeout=15.0, follow_redirects=True, verify=False) as client:
            resp = client.get(url, headers=HEADERS)
            resp.raise_for_status()
            html = resp.text
            
        soup = BeautifulSoup(html, "html.parser")
        
        # Remove unwanted elements
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "iframe", "noscript"]):
            tag.decompose()
            
        # Strategy 1: Look for semantic <article> tag
        article = soup.find("article")
        if article:
            text = article.get_text(separator="\n")
            return clean_text(text)
            
        # Strategy 2: Look for common class names for content
        # This is a heuristic and may need tuning for specific sites
        potential_classes = [
            "article-body", "story-body", "content-body", "article-content", 
            "post-content", "entry-content", "main-content"
        ]
        
        for cls in potential_classes:
            div = soup.find("div", class_=cls)
            if div:
                text = div.get_text(separator="\n")
                return clean_text(text)
                
        # Strategy 3: Fallback - find all <p> tags and join them if they look like paragraphs
        paragraphs = soup.find_all("p")
        valid_paras = []
        for p in paragraphs:
            txt = p.get_text().strip()
            # Filter out short snippets like "Advertisement" or "Read more"
            if len(txt) > 50: 
                valid_paras.append(txt)
                
        if len(valid_paras) > 3: # If we found enough paragraphs, assume it's the article
            return clean_text("\n\n".join(valid_paras))
            
        return ""

    except Exception as e:
        logger.warning(f"Error fetching content for {url}: {e}")
        return ""
