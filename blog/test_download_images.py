#!/usr/bin/env python3
"""
Quick test: Download LinkedIn images from a single article
"""

import re
import urllib.request
from pathlib import Path

# Test with the ai-first-organizations article
ARTICLE_PATH = Path(__file__).parent / "ai-philosophy" / "ai-first-organizations-a-new-dna.html"
TEST_OUTPUT_DIR = Path(__file__).parent / "test_images"

# Create test output directory
TEST_OUTPUT_DIR.mkdir(exist_ok=True)

def extract_linkedin_images(html_content):
    """Extract all LinkedIn CDN image URLs from HTML"""
    pattern = r'src="(https://media\.licdn\.com/dms/image[^"]+)"'
    return re.findall(pattern, html_content)

def download_image(url, output_path):
    """Download image from URL"""
    try:
        print(f"\n🔽 Attempting to download:")
        print(f"   URL: {url[:100]}...")

        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            print(f"   Status: {response.status}")
            print(f"   Content-Type: {response.headers.get('Content-Type')}")
            print(f"   Content-Length: {response.headers.get('Content-Length')} bytes")

            if response.status == 200:
                content = response.read()
                with open(output_path, 'wb') as f:
                    f.write(content)
                print(f"   ✅ Saved to: {output_path}")
                return True
            else:
                print(f"   ❌ HTTP {response.status}")
                return False

    except urllib.error.HTTPError as e:
        print(f"   ❌ HTTP Error {e.code}: {e.reason}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

# Read the article
print(f"📄 Reading article: {ARTICLE_PATH.name}")
with open(ARTICLE_PATH, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Extract LinkedIn images
image_urls = extract_linkedin_images(html_content)
print(f"\n✨ Found {len(image_urls)} LinkedIn image(s)\n")

if not image_urls:
    print("No LinkedIn images found in this article")
    exit(0)

# Try downloading each image
for idx, url in enumerate(image_urls, 1):
    output_path = TEST_OUTPUT_DIR / f"test-image-{idx}.jpg"
    print(f"\n{'='*70}")
    print(f"Image {idx} of {len(image_urls)}")
    print(f"{'='*70}")

    success = download_image(url, output_path)

    if success:
        file_size = output_path.stat().st_size
        print(f"   📊 File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")

print(f"\n{'='*70}")
print("TEST COMPLETE")
print(f"{'='*70}")
print(f"Images saved to: {TEST_OUTPUT_DIR}")
