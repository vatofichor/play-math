# Server Setup & Integration Specification

This specification outlines the server architecture, deployment options, and integration procedures for the **Play-Math** platform. It is designed for system administrators deploying the workspace on standard Linux servers (Debian/Ubuntu) running Apache/Nginx (LAMP/LEMP stack) or standalone Python environments.

---

## 1. System Architecture Overview

The frontend interacts with the server in two ways:
1. **Static Assets**: HTML, CSS, JS, images, and canvas scripts are served directly from the filesystem.
2. **Roadmap API**: The main explorer queries `/api/roadmap` to scan the subfolders of the `content/` directory in real-time, verifying which subtopics are "live" (i.e. containing an `index.html` entrypoint).

We support **three server deployment configurations** depending on the production environment.

---

## 2. Option A: Native Apache + PHP (Recommended for LAMP)

In standard PHP-enabled Apache environments, **no Python background process is required**. The server runs 100% natively using Apache rewrites and a lightweight PHP backend script to simulate the API.

### Step 1: Create the PHP Endpoint
Create a folder named `api/` in the project root and add [api/roadmap.php](file:///d:/Dev/play-math/api/roadmap.php):

```php
<?php
header('Content-Type: application/json');
header('Cache-Control: no-cache, no-store, must-revalidate');

$directory = dirname(__DIR__);
$content_dir = $directory . '/content';

// Load manifest.json for custom formatting
$manifest_path = $directory . '/manifest.json';
$manifest = [];
if (file_exists($manifest_path)) {
    $manifest = json_decode(file_get_contents($manifest_path), true);
}

function format_subtopic_name($name, $manifest) {
    $subtopic_names = isset($manifest['subtopic_names']) ? $manifest['subtopic_names'] : [];
    if (isset($subtopic_names[strtolower($name)])) {
        return $subtopic_names[strtolower($name)];
    }
    
    $words = explode(' ', str_replace('_', ' ', $name));
    $formatted = [];
    foreach ($words as $idx => $w) {
        if ($idx > 0 && in_array(strtolower($w), ['and', 'of', 'by', 'with', 'to', 'for'])) {
            $formatted[] = strtolower($w);
        } else {
            $formatted[] = ucfirst(strtolower($w));
        }
    }
    return implode(' ', $formatted);
}

$data = [];
if (is_dir($content_dir)) {
    $entries = scandir($content_dir);
    sort($entries);
    foreach ($entries as $entry) {
        if ($entry === '.' || $entry === '..') continue;
        $entry_path = $content_dir . '/' . $entry;
        if (is_dir($entry_path) && is_numeric(substr($entry, 0, 2)) && strpos($entry, '_') !== false) {
            $subtopics = [];
            $sub_entries = scandir($entry_path);
            sort($sub_entries);
            foreach ($sub_entries as $sub) {
                if ($sub === '.' || $sub === '..') continue;
                $sub_path = $entry_path . '/' . $sub;
                if (is_dir($sub_path)) {
                    $is_live = file_exists($sub_path . '/index.html');
                    $subtopics[] = [
                        "id" => $sub,
                        "name" => format_subtopic_name($sub, $manifest),
                        "live" => $is_live,
                        "path" => $is_live ? "/$entry/$sub/index.html" : null
                    ];
                }
            }
            $data[$entry] = $subtopics;
        }
    }
}

echo json_encode($data);
```

### Step 2: Configure `.htaccess` Rewrites
Ensure Apache's `mod_rewrite` is enabled. Place this [.htaccess](file:///d:/Dev/play-math/.htaccess) file in your project root:

```apache
RewriteEngine On

# Route the roadmap API endpoint to the PHP script
RewriteRule ^api/roadmap$ api/roadmap.php [L]

# Route folders starting with 01_ through 07_ to content/
RewriteCond %{REQUEST_URI} !^/content/ [NC]
RewriteRule ^(0[1-7]_.*)$ content/$1 [L]
```

---

## 3. Option B: Standalone Python Server (Local / Development)

If the server does not have Apache/PHP, but has Python installed, run the system using the built-in HTTP server:

```bash
python app.py
```

### Run as a systemd service (Production Daemon)
To keep the Python process running continuously on Ubuntu/Debian:

1. Create a service file `/etc/systemd/system/play-math.service`:
```ini
[Unit]
Description=Play-Math Python Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/web/play-math
ExecStart=/usr/bin/python3 app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
2. Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable play-math.service
sudo systemctl start play-math.service
```

3. Configure Apache Reverse Proxy (optional, to serve on port 80/443):
```apache
<VirtualHost *:80>
    ServerName playmath.domain.com
    ProxyPreserveHost On
    ProxyPass /api/roadmap http://localhost:8090/api/roadmap
    ProxyPassReverse /api/roadmap http://localhost:8090/api/roadmap
    
    DocumentRoot /var/web/play-math
</VirtualHost>
```

---

## 4. Option C: Completely Static Deployments

If the destination hosting provider allows static files only (e.g. GitHub Pages), dynamic folder scanning is unavailable. 

In this case:
1. Run `python app.py` locally.
2. Fetch `http://localhost:8090/api/roadmap` and save the resulting JSON payload as a static file: `/api/roadmap` (or `/api/roadmap.json`).
3. Commit this file to the repository. The client side will query this static file directly.

---
# Copyright (c) 2026:
# vatofichor - Sebastian Mass     [>_<]
# & Assisted By Gemini Antigravity /|\
