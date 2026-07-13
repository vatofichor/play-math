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

// Calculate base path relative to document root to ensure correct subdirectory pathing
$docRoot = rtrim(str_replace('\\', '/', $_SERVER['DOCUMENT_ROOT'] ?? ''), '/');
$appDir = rtrim(str_replace('\\', '/', dirname(__DIR__)), '/');
$basePath = '';
if (!empty($docRoot) && stripos($appDir, $docRoot) === 0) {
    $basePath = substr($appDir, strlen($docRoot));
}
$basePath = '/' . trim(str_replace('\\', '/', $basePath), '/');
if ($basePath === '/') $basePath = '';

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
                        "path" => $is_live ? "$basePath/content/$entry/$sub/index.html" : null
                    ];
                }
            }
            $data[$entry] = $subtopics;
        }
    }
}

echo json_encode($data);
/*
Copyright (c) 2026:
vatofichor - Sebastian Mass     [>_<]
& Assisted By Gemini Antigravity /|\
*/
