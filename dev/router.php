<?php
/**
 * PHP Development Server & Apache Router for Mathematical Mastery Roadmap
 * Handles rewriting equivalent to Apache .htaccess rules.
 */

// Normalize paths to use forward slashes
$docRoot = rtrim(str_replace('\\', '/', $_SERVER['DOCUMENT_ROOT']), '/');
$appDir = rtrim(str_replace('\\', '/', dirname(__DIR__)), '/');

// Calculate base path relative to document root
$basePath = '';
if (stripos($appDir, $docRoot) === 0) {
    $basePath = substr($appDir, strlen($docRoot));
}
$basePath = '/' . trim(str_replace('\\', '/', $basePath), '/');

// Get request URI and parse path
$requestUri = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);

// Strip basePath from requestUri to get clean application URI
$uri = '/';
if ($basePath !== '/' && stripos($requestUri, $basePath) === 0) {
    $uri = '/' . ltrim(substr($requestUri, strlen($basePath)), '/');
} else {
    $uri = '/' . ltrim($requestUri, '/');
}
$uri = urldecode($uri);

$baseDir = dirname(__DIR__);

// Helper function to serve file with correct Content-Type
function serve_file($file) {
    if (!file_exists($file)) {
        header("HTTP/1.1 404 Not Found");
        echo "404 Not Found";
        exit;
    }
    
    $ext = pathinfo($file, PATHINFO_EXTENSION);
    $mimes = [
        'html' => 'text/html',
        'css' => 'text/css',
        'js' => 'application/javascript',
        'json' => 'application/json',
        'png' => 'image/png',
        'jpg' => 'image/jpeg',
        'jpeg' => 'image/jpeg',
        'gif' => 'image/gif',
        'svg' => 'image/svg+xml',
        'ico' => 'image/x-icon'
    ];
    
    if (isset($mimes[$ext])) {
        header("Content-Type: " . $mimes[$ext]);
    }
    readfile($file);
    exit;
}

// 1. Rewrite api/roadmap to api/roadmap.php
if ($uri === '/api/roadmap') {
    require $baseDir . '/api/roadmap.php';
    exit;
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

// 3. Clean category redirect mapping
$categories = [
    '/arithmetic' => '/content/01_arithmetic_number_sense/index.html',
    '/algebra' => '/content/02_algebra/index.html',
    '/geometry' => '/content/03_geometry_measurement/index.html',
    '/trig' => '/content/04_trigonometry/index.html',
    '/calculus' => '/content/05_calculus/index.html',
    '/data' => '/content/06_data_science_statistics/index.html',
    '/compmath' => '/content/07_computational_math/index.html',
    '/tags' => '/content/tags/index.html'
];

if (isset($categories[$uri])) {
    serve_file($baseDir . $categories[$uri]);
}

$trimmedUri = rtrim($uri, '/');
if (isset($categories[$trimmedUri])) {
    serve_file($baseDir . $categories[$trimmedUri]);
}

// 4. Default static file server fallback
if ($uri !== '/' && file_exists($baseDir . $uri)) {
    return false; // let built-in server handle standard static assets
}

// 5. Default to main index.html dashboard
serve_file($baseDir . '/index.html');
