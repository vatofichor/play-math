# play-math — Mathematical Mastery Roadmap

```
    ____  __                 __  ___      __  __
   / __ \/ /___ ___  __     /  |/  /___ _/ /_/ /_
  / /_/ / / __ `/ / / /___ / /|_/ / __ `/ __/ __ \
 / ____/ / /_/ / /_/ /____/ /  / / /_/ / /_/ / / /
/_/   /_/\__,_/\__/_/ /_/    /_/  /_/\__,_/\__/_/ 
              /____/                             
```

An interactive, high-density dashboard mapping core domains of mathematics to real-time HTML5 Canvas physical sandbox simulators. This playground teaches mathematical quantities, spatial relationships, and formulas through interactive visual models.

---

# PART 1: Parent & Educator Guide (Quick Start)

This section is designed to get the math playground running on your home computer or classroom machine.

## How to Run Locally

### 1. Launching on Windows (Recommended)
1. Double-click the file [run_server.bat](run_server.bat) in this folder.
2. A window will open, and your web browser should automatically open to the dashboard.
3. The launcher will automatically detect if you have Python 3+ installed. If not, it will fall back to using the prepackaged portable Python environment included in this repository under `assets/lib/python/`.
4. If both your system Python and the prepackaged local Python are missing, the launcher window will stop and show you a clean step-by-step instruction guide on how to download it.

> [!TIP]
> **If you need to install Python manually**:
> 1. Open your web browser and go to [https://www.python.org/downloads/](https://www.python.org/downloads/).
> 2. Click the yellow button to download the latest version for Windows.
> 3. Run the downloaded installer.
> 4. **CRITICAL STEP**: On the very first screen of the installer, check the box at the bottom that says **"Add Python.exe to PATH"** before clicking Install.
> 5. After the installation finishes, double-click [run_server.bat](run_server.bat) again.

### 2. Launching on macOS / Linux / Terminal
1. Open your Terminal program.
2. Navigate to this folder and type:
   ```bash
   python3 app.py
   ```
3. Open your browser and go to: [http://localhost:8090](http://localhost:8090)

### 3. Stopping the Server
- On Windows, double-click [stop_server.bat](stop_server.bat) or press `Ctrl + C` inside the running server terminal window.

---

## Pedagogy & US Grade Alignments

Use this table to find the appropriate math topics for your child or student. There are **55 completed modules** ready to play:

| Domain | Path | US Grade Levels | Core Simulator Concepts |
| :--- | :--- | :--- | :--- |
| **01. Arithmetic & Numbers** | `/01_arithmetic_number_sense` | **Grades 3 – 7** | Fraction pieces, decimal place values, decimal operators, PEMDAS priority trees, and directed number lines. |
| **02. Algebraic Structures** | `/02_algebra` | **Grades 6 – College** | Balance scale equations, linear slopes, parabolas, asymptotes, and algebraic area identities. |
| **03. Geometry & Space** | `/03_geometry_measurement` | **Grades 3 – High School** | 2D shape perimeters, rotatable 3D solids, protractor angles, and similarity shadow projection. |
| **04. Trigonometry & Waves** | `/04_trigonometry` | **High School – College** | SOH CAH TOA right-triangle ratios and sine/cosine wave amplitude controllers. |
| **05. Calculus & Limits** | `/05_calculus` | **High School – College** | Zeno's paradox slice packaging towards 1 and continuous vector flow fields. |
| **06. Data Science & Stats** | `/06_data_science_statistics` | **Grades 6 – High School** | Box plots, scatter correlations, Venn sorting lenses, and combination dial lock permutations. |
| **07. Computational Math** | `/07_computational_math` | **High School – College** | Dijkstra truck route routers, plotting consoles, and programming dataframes. |

---

# PART 2: Developer Specifications & Server Deployment

This section is for developers hosting the playground on production web servers or integrating modules into Learning Management Systems (LMS).

## Pythonic Dependencies & Environment

The local python tools (the development server `app.py` and diagnostic checker scripts under `dev/`) run natively using Python 3+ standard libraries.
- **Required Packages**: None (zero external pip packages required).
- **Core Standard Modules**: `http.server`, `socketserver`, `webbrowser`, `threading`, `json`, `html.parser`, `re`.
- **Portable Setup**: A pre-packaged, portable Python installation is located at `assets/lib/python/` for plug-and-play execution on Windows without system-wide python installations.

## Production Hosting Setup

Depending on your production environment, we support **three deployment options** for hosting the math roadmap platform.

### Option A: Native Apache + PHP (Recommended for standard LAMP stacks)
If your server runs Apache with PHP, **no background Python process is required**. The server runs natively by mapping `/api/roadmap` to a lightweight PHP script that scans directories in real-time.

1. Create a file named `api/roadmap.php` to handle real-time directory listing (see the full script in [dev/specs/server_setup_spec.md](dev/specs/server_setup_spec.md)).
2. Place this [.htaccess](.htaccess) file in your project root to handle routing rewrites:
```apache
RewriteEngine On
RewriteRule ^api/roadmap$ api/roadmap.php [L]
RewriteCond %{REQUEST_URI} !^/content/ [NC]
RewriteRule ^(0[1-7]_.*)$ content/$1 [L]
```

### Option B: Standalone Python systemd Daemon
For hosting environments without PHP, run `app.py` continuously as a Linux service:

1. Create a service file `/etc/systemd/system/play-math.service`:
```ini
[Unit]
Description=Play-Math Python Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/play-math
ExecStart=/usr/bin/python3 app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
2. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable play-math.service
sudo systemctl start play-math.service
```

### Option C: Fully Static Nginx Hosting
For static environments (like GitHub Pages), dynamic folder scanning is unavailable. You can pre-compile the roadmap API:
1. Fetch the JSON roadmap payload from `http://localhost:8090/api/roadmap` locally.
2. Save this static payload to a file named `roadmap` under an `api/` directory (making it serve at `/api/roadmap`).
3. Deploy this file alongside static files and use Nginx to map domain directories:
```nginx
server {
    listen 80;
    server_name play-math.yourdomain.com;
    root /var/www/play-math;
    index index.html;

    # Rewrite math domains to content folder internally (keeps browser URLs clean)
    location ~ ^/(0[1-7]_[a-zA-Z0-9_-]+)(/.*)?$ {
        if ($request_uri !~ "/$") {
            rewrite ^/(0[1-7]_[a-zA-Z0-9_-]+.*)$ /$1/ permanent;
        }
        rewrite ^/(0[1-7]_[a-zA-Z0-9_-]+)(/.*)?$ /content/$1$2 break;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
```

---

## LMS Iframe Integration

All sandbox modules are fully LMS-ready. The layouts automatically adapt to iframe dimensions.

### Embedding Snippet
Copy this code block to insert an activity (e.g., Dijkstra route puzzle) inside your course module:

```html
<iframe 
  src="https://play-math.yourdomain.com/07_computational_math/graph_theory_networks/index.html" 
  width="100%" 
  height="720px" 
  style="border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; background: #050608;" 
  allow="fullscreen" 
  loading="lazy">
</iframe>
```
- **State Management**: Sidebar toggle collapse states are stored in the client browser's `localStorage` (`sidebar-collapsed`), allowing students to hide navigation menus and maximize their canvas workspace across sessions.

---

## Architecture Principles (Vatofichor MVC)

- **Zero-Dependency Simulators**: All math visualizers utilize native HTML5 Canvas 2D Context (`canvas.getContext('2d')`). Heavy libraries (Three.js, p5.js, PixiJS) or math formula parsers are bypassed for layout speed.
- **Content Segmentation**: All math modules reside under [content/](content/), leaving the project root clean of local course layouts. Global UI wraps are injected dynamically at runtime via [shared.js](assets/shared.js).

---
# Copyright (c) 2026:
# vatofichor - Sebastian Mass     [>_<]
# & Assisted By Gemini Antigravity /|\
