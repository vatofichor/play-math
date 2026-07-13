# Routing & Topic Resolution Specification

This document details the routing architecture, server-side rewrite configs, directory resolution systems, and frontend module navigation options for the Mathematical Mastery Roadmap project.

---

## 1. Main Router for the Roadmap (Server-Side Resolution)

The project supports three backend environments to resolve clean URLs to nested filesystem paths:

### 1.1 Apache HTTP Server Rewrite Engine (`.htaccess`)
In production environments, Apache maps requests dynamically using `mod_rewrite`. It intercepts requests to the `01_` through `07_` domains and rewrites them internally to the `content/` folder without altering the browser URL.

```apache
RewriteEngine On

# Route the roadmap API endpoint to the PHP script
RewriteRule ^api/roadmap$ api/roadmap.php [L]

# Prepend /content/ to any domain request (Step 01 - 07)
RewriteCond %{REQUEST_URI} !^/content/ [NC]
RewriteRule ^(0[1-7]_.*)$ content/$1 [L]

# Route clean category redirects
RewriteRule ^arithmetic/?$ content/01_arithmetic_number_sense/index.html [L]
RewriteRule ^algebra/?$ content/02_algebra/index.html [L]
RewriteRule ^geometry/?$ content/03_geometry_measurement/index.html [L]
RewriteRule ^trig/?$ content/04_trigonometry/index.html [L]
RewriteRule ^calculus/?$ content/05_calculus/index.html [L]
RewriteRule ^data/?$ content/06_data_science_statistics/index.html [L]
RewriteRule ^compmath/?$ content/07_computational_math/index.html [L]
```

### 1.2 PHP Development Server Router (`index.php` / `dev/router.php`)
For local PHP-driven environments, `index.php` integrates the development router logic. Running the CLI server with either file as the router script mimics Apache's rewrite rules, handling directory index resolving and asset content-typing.

To run the server locally:
```bash
php -S localhost:8090 index.php
```

Under the hood, the router maps endpoints:
```php
// 1. Rewrite api/roadmap to api/roadmap.php
if ($uri === '/api/roadmap') {
    serve_file($baseDir . '/api/roadmap.php');
}

// 2. Rewrite 01_... to 07_... categories under content/
if (preg_match('/^\/(0[1-7]_[^\/]+)(.*)$/', $uri, $matches)) {
    $targetPath = $baseDir . '/content/' . $matches[1] . $matches[2];
    if (is_dir($targetPath)) {
        $targetPath = rtrim($targetPath, '/') . '/index.html';
    }
    if (file_exists($targetPath)) {
        serve_file($targetPath);
    }
}
```

### 1.3 Python HTTP Server Development Engine (`app.py`)
For Python-only mock setups, `app.py` acts as a static file server and returns dynamic roadmap data for local simulation.
- `GET /` serves the root `index.html`.
- `GET /api/roadmap` intercepts the lookup and returns dynamically scanned workspace categories as JSON.

### 1.4 Dynamic Roadmap API (`api/roadmap.php`)
Acts as the central API endpoint that returns JSON catalog mappings of all domains and active subtopics by verifying the existence of `index.html` within child directories.

---

## 2. Directory Naming & Ordering Rules

To maintain structured progression, domains and subtopics must adhere to the following filesystem conventions:

1. **Domain Folders**:
   - Must reside in the project root.
   - Must be prefixed with a two-digit step index followed by an underscore: `\d{2}_[a-z0-9_]+` (e.g., `01_arithmetic_number_sense`).
   - Sorted alphabetically/numerically by directory name to ensure domain flow ordering (Step 1 to Step 7).

2. **Subtopic Folders**:
   - Reside inside their parent domain folder.
   - Named using snake_case (e.g., `basic_operations`, `decimal_place_value`).
   - Labeled dynamically using the dictionary mapping in [manifest.json](file:///d:/Dev/play-math/manifest.json) (`subtopic_names`). If not defined in the manifest, fallback capitalization is applied by replacing underscores with spaces.

3. **Liveness Check**:
   - A subtopic is designated as **live** (active) if it contains an `index.html` file. 
   - Non-live directories are scanned but displayed as disabled/unlinked modules on the dashboard.

---

## 3. Frontend Module Routing Paradigms

Individual modules can implement section navigation in one of two ways based on module complexity:

### 3.1 Multi-Page Filesystem Routing
For complex modules with extensive sub-sections (e.g., *Algebraic Identities* or *Measurement Basics*), sections are split into discrete physical files.
- **Menu Config**: Navigation objects specify relative file links:
  ```javascript
  window.PAGE_CONFIG = {
      navigation: [
          { label: "Early Learners Basics", desc: "Compare tall & heavy", href: "index.html" },
          { label: "Common Unit Types", desc: "Dimensions game", href: "common_types.html" }
      ]
  };
  ```
- **Context Preservation**: Entry links from the dashboard always specify `/index.html` explicitly. This ensures relative paths resolve against the subfolder path rather than the domain root.

### 3.2 Single-Page Hash-Based Routing
For simple modules with local sub-sections or quizzes contained within one document, navigation toggles tabs without loading a new page.
- **Menu Config**: Navigation objects specify target hashes:
  ```javascript
  window.PAGE_CONFIG = {
      navigation: [
          { label: "Interactive Clock", desc: "Read analog time", href: "#section1" },
          { label: "Time Quiz", desc: "Test clock reading", href: "#sectionQuiz" }
      ]
  };
  ```
- **View Controller**: The page registers a `hashchange` listener to display active elements and synchronize active CSS styles on the dynamic sidebar menu.

```javascript
function handleRouting() {
    const hash = window.location.hash;
    const secBasics = document.getElementById('sectionBasics');
    const secQuiz = document.getElementById('sectionQuiz');
    
    if (hash === '#sectionQuiz') {
        secBasics.style.display = 'none';
        secQuiz.style.display = 'block';
    } else {
        secBasics.style.display = 'block';
        secQuiz.style.display = 'none';
    }
}
window.addEventListener('hashchange', handleRouting);
```

---

## 4. Frontend Dynamic Dashboard Rendering

On dashboard initialization:
1. `loadDynamicSubtopics()` makes an asynchronous fetch request to `/api/roadmap`.
2. Iterates over domains returned in the JSON payload.
3. Targets elements matching the query `[data-domain-id="${domainKey}"]` (e.g., `<ul data-domain-id="01_arithmetic_number_sense">`).
4. Injects list items:
   - **Live Topic**: Wraps element in an `active-module` class, binds `onclick="window.location.href='${sub.path}'"`, and appends an animated `<span class="orange-dot"></span>`.
   - **Inactive Topic**: Renders static text with muted colors to indicate future implementation paths.

---
# Copyright (c) 2026:
# vatofichor - Sebastian Mass     [>_<]
# & Assisted By Gemini Antigravity /|\
