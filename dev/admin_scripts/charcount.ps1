# charcount.ps1 - Paste text, get character count
# Copyright (c) 2026:
# vatofichor - Sebastian Mass     [>_<]
# & Assisted By Gemini Antigravity /|\

Write-Host ""
Write-Host "=== Character Counter ===" -ForegroundColor Cyan
Write-Host "Paste text below (press Enter twice to finish):" -ForegroundColor Gray
Write-Host ""

$lines = @()
$emptyCount = 0

while ($true) {
    $line = Read-Host
    if ($line -eq "") {
        $emptyCount++
        if ($emptyCount -ge 1) { break }
        $lines += $line
    } else {
        $emptyCount = 0
        $lines += $line
    }
}

$text = $lines -join "`n"

$total      = $text.Length
$noSpaces   = ($text -replace '\s','').Length
$noNewlines = ($text -replace "`n",'').Length
$words      = ($text -split '\s+' | Where-Object { $_ -ne '' }).Count
$lineCount  = $lines.Count

Write-Host ""
Write-Host "--- Results ---" -ForegroundColor Yellow
Write-Host "Characters (total):      $total"
Write-Host "Characters (no spaces):  $noSpaces"
Write-Host "Characters (no newlines): $noNewlines"
Write-Host "Words:                   $words"
Write-Host "Lines:                   $lineCount"
Write-Host ""
