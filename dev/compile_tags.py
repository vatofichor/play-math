# Copyright (c) 2026:
# vatofichor - Sebastian Mass     [>_<]
# & Assisted By Gemini Antigravity /|\

import os
import re
import urllib.parse

DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(DIRECTORY, "content")
OUTPUT_PATH = os.path.join(CONTENT_DIR, "tags", "index.html")

tag_pattern = re.compile(r'class=["\']section-tag["\'][^>]*>([^<]+)</', re.IGNORECASE)
title_pattern = re.compile(r'<title>([^<]+)</title>', re.IGNORECASE)

def clean_tag(tag):
    return tag.strip()

def compile_tags():
    tags_map = {} # tag_name -> set of subtopic paths
    
    for root, dirs, files in os.walk(CONTENT_DIR):
        # Skip tags folder itself and build script
        if "tags" in root or "dev" in root:
            continue
            
        for file in files:
            if file == "index.html":
                file_path = os.path.join(root, file)
                
                # Check if this is a subtopic index or category dashboard index
                # Category dashboards are located directly under content/0X_xxx/index.html (depth 2)
                # Subtopics are at content/0X_xxx/subtopic_name/index.html (depth 3)
                relative_path = os.path.relpath(file_path, CONTENT_DIR)
                parts = relative_path.replace('\\', '/').split('/')
                
                if len(parts) < 3:
                    # Category dashboard index, skip tags scanning
                    continue
                    
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        html_content = f.read()
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    continue
                
                found_tags = tag_pattern.findall(html_content)
                if found_tags:
                    # Get clean title
                    title_match = title_pattern.search(html_content)
                    title = title_match.group(1).replace(' - play-math', '').strip() if title_match else parts[-2].replace('_', ' ').capitalize()
                    
                    subtopic_path = f"/{parts[0]}/{parts[1]}/index.html"
                    
                    for tag in found_tags:
                        t_clean = clean_tag(tag)
                        if t_clean:
                            if t_clean not in tags_map:
                                tags_map[t_clean] = []
                            tags_map[t_clean].append({
                                "title": title,
                                "path": subtopic_path
                            })

    # Sort tags alphabetically
    sorted_tags = sorted(tags_map.keys(), key=lambda s: s.lower())

    # Build Tags Listing HTML
    tags_html = ""
    for tag in sorted_tags:
        # Encode tag query for URL
        encoded_query = urllib.parse.quote(tag)
        tags_html += f"""
        <div class="tag-card">
            <h3 class="tag-title">
                <a href="../../index.html?search={encoded_query}" data-clean-route="/?search={encoded_query}" class="tag-link">{tag}</a>
            </h3>
            <ul class="tag-subtopics">
        """
        # Deduplicate and sort subtopics
        seen = set()
        for sub in tags_map[tag]:
            if sub["path"] not in seen:
                seen.add(sub["path"])
                tags_html += f'                <li><a href="..{sub["path"]}" class="subtopic-tag-link">{sub["title"]}</a></li>\n'
                
        tags_html += """            </ul>
        </div>"""

    # Template for Tags page
    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Keywords & Tags - play-math</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../assets/shared.css">
    <style>
        :root {{
            --bg-color: #050608;
            --grid-color: rgba(255, 255, 255, 0.02);
            --card-bg: rgba(13, 16, 23, 0.65);
            --card-border: rgba(255, 255, 255, 0.06);
            --card-border-hover: rgba(255, 176, 0, 0.3);
            --text-color: #e2e8f0;
            --text-muted: #6b7c93;
            --color-amber: #ffb000;
            --transition-speed: 0.3s;
        }}

        body {{
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-color);
            background-image:
                radial-gradient(var(--grid-color) 1px, transparent 1px),
                radial-gradient(var(--grid-color) 1px, transparent 1px);
            background-size: 40px 40px;
            background-position: 0 0, 20px 20px;
            color: var(--text-color);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 4rem 2rem;
        }}

        .bg-glow {{
            position: absolute;
            top: 20%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 650px;
            height: 650px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(255, 176, 0, 0.04) 0%, transparent 70%);
            z-index: -1;
            pointer-events: none;
            filter: blur(50px);
        }}

        header {{
            text-align: center;
            max-width: 800px;
            margin-bottom: 4rem;
        }}

        header h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #ffffff 40%, var(--color-amber) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        header p {{
            font-size: 1.1rem;
            color: var(--text-muted);
            line-height: 1.6;
        }}

        .tags-container {{
            width: 100%;
            max-width: 900px;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 1.5rem;
        }}

        .tag-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.5rem;
            backdrop-filter: blur(16px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            transition: all var(--transition-speed) ease;
        }}

        .tag-card:hover {{
            border-color: var(--card-border-hover);
            transform: translateY(-2px);
        }}

        .tag-title {{
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
            color: var(--color-amber);
        }}

        .tag-link {{
            color: inherit;
            text-decoration: none;
            transition: color var(--transition-speed) ease;
        }}

        .tag-link:hover {{
            color: #ffffff;
        }}

        .tag-subtopics {{
            list-style: none;
            padding-left: 0;
            font-size: 0.85rem;
        }}

        .tag-subtopics li {{
            margin-bottom: 6px;
            position: relative;
            padding-left: 12px;
        }}

        .tag-subtopics li::before {{
            content: '•';
            position: absolute;
            left: 0;
            color: var(--text-muted);
        }}

        .subtopic-tag-link {{
            color: var(--text-muted);
            text-decoration: none;
            transition: color var(--transition-speed) ease;
        }}

        .subtopic-tag-link:hover {{
            color: var(--text-color);
        }}

        footer {{
            margin-top: 6rem;
            text-align: center;
            font-size: 0.85rem;
            color: var(--text-muted);
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <div class="bg-glow"></div>

    <div class="dashboard-card-wrapper" style="max-width: 900px;">
        <div class="btn-back-container">
            <a href="../../index.html" class="btn-back" id="btnBackHome">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
                Back to Roadmap
            </a>
        </div>

        <header>
            <h1>Domain Keywords &amp; Tags</h1>
            <p>Explore index tags and keywords compiling interactive visualizers, sandboxes, and simulation modules across the curriculum.</p>
        </header>

        <div class="tags-container">
            {tags_html}
        </div>
    </div>

    <footer>
        play-math • Powered by HTML5 Canvas & CSS3<br>
        Copyright (c) 2026: vatofichor - Sebastian Mass [>_<] <br>& Assisted By Gemini Antigravity /|\
    </footer>

    <script>
        function initializeTagsPage() {{
            const isLocalFile = window.location.protocol === 'file:';
            const endsWithHtml = window.location.pathname.endsWith('.html');
            const supportsRewriting = !isLocalFile && !endsWithHtml;

            if (supportsRewriting) {{
                document.getElementById('btnBackHome').href = '/';
                document.querySelectorAll('.tag-link').forEach(link => {{
                    const cleanRoute = link.getAttribute('data-clean-route');
                    if (cleanRoute) {{
                        link.href = cleanRoute;
                    }}
                }});
                
                // Adjust subtopic links dynamically on server hosting
                document.querySelectorAll('.subtopic-tag-link').forEach(link => {{
                    // Strip the leading "/content" or relative dots inside paths
                    const path = link.getAttribute('href');
                    if (path && path.includes('/content/')) {{
                        link.href = path.substring(path.indexOf('/content/') + 8);
                    }}
                }});
            }}
        }}

        window.addEventListener('DOMContentLoaded', initializeTagsPage);
    </script>
</body>
</html>
<!--
Copyright (c) 2026:
vatofichor - Sebastian Mass     [>_<]
& Assisted By Gemini Antigravity /|\
-->"""

    # Create directories if they do not exist
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(template)
        
    print(f"Tags successfully compiled to {OUTPUT_PATH}")

if __name__ == "__main__":
    compile_tags()
