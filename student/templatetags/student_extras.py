from django import template
import re

register = template.Library()

@register.filter
def youtube_embed_url(url):
    """
    Converts a YouTube URL to an embed URL.
    
    Example:
        https://www.youtube.com/watch?v=dQw4w9WgXcQ -> https://www.youtube.com/embed/dQw4w9WgXcQ
        https://youtu.be/dQw4w9WgXcQ -> https://www.youtube.com/embed/dQw4w9WgXcQ
    """
    # Standard YouTube URL (https://www.youtube.com/watch?v=VIDEO_ID)
    match = re.search(r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)', url)
    if match:
        return f'https://www.youtube.com/embed/{match.group(1)}'
    
    # Shortened YouTube URL (https://youtu.be/VIDEO_ID)
    match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
    if match:
        return f'https://www.youtube.com/embed/{match.group(1)}'
    
    # If no match, return the original URL
    return url 