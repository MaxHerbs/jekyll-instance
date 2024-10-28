import re
import base64
import requests
from urllib.parse import urljoin

def fetch_content(url):
    """Fetch content from a URL and return text or binary data."""
    response = requests.get(url)
    response.raise_for_status()
    return response.content if "image" in response.headers["Content-Type"] else response.text

def inline_css(html, base_url):
    """Inline CSS content into HTML."""
    css_links = re.findall(r'<link\s+[^>]*href=["\'](.*?\.css)["\']', html)
    for css_link in css_links:
        css_url = urljoin(base_url, css_link)
        try:
            css_content = fetch_content(css_url)
            css_block = f"<style>{css_content}</style>"
            html = re.sub(r'<link\s+[^>]*href=["\'].*?\.css["\'][^>]*>', css_block, html, count=1)
        except requests.RequestException:
            print(f"Warning: Failed to fetch CSS file {css_url}")
    return html

def inline_js(html, base_url):
    """Inline JavaScript content into HTML, escaping special characters."""
    js_links = re.findall(r'<script\s+[^>]*src=["\'](.*?\.js)["\']', html)
    for js_link in js_links:
        js_url = urljoin(base_url, js_link)
        try:
            js_content = fetch_content(js_url)
            js_block = f"<script>{re.escape(js_content)}</script>"
            html = re.sub(r'<script\s+[^>]*src=["\'].*?\.js["\'][^>]*></script>', js_block, html, count=1)
        except requests.RequestException:
            print(f"Warning: Failed to fetch JavaScript file {js_url}")
    return html

def embed_images(html, base_url):
    """Convert image URLs to Base64 and embed them."""
    img_tags = re.findall(r'<img\s+[^>]*src=["\'](.*?)["\']', html)
    for img_tag in img_tags:
        img_url = urljoin(base_url, img_tag)
        try:
            img_data = fetch_content(img_url)
            img_extension = img_url.split(".")[-1]
            img_data_uri = f"data:image/{img_extension};base64,{base64.b64encode(img_data).decode('utf-8')}"
            html = html.replace(img_tag, img_data_uri)
        except requests.RequestException:
            print(f"Warning: Failed to fetch image {img_url}")
    return html

def export_to_single_html(web_url):
    """Fetch HTML with inlined resources from an arbitrary URL and export to a single file."""
    # Fetch the main HTML content
    html = fetch_content(web_url)
    
    # Inline CSS and JavaScript
    html = inline_css(html, web_url)
    html = inline_js(html, web_url)
    
    # Embed images
    html = embed_images(html, web_url)

    # Write to a single HTML file
    output_path = "exported_single_file.html"
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(html)
    
    print(f"Exported HTML to {output_path}")

# Usage
web_url = input("Enter the URL of the page to export: ")
export_to_single_html(web_url)
