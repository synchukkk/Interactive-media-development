# Відкриває local index.html у Google Chrome (PowerShell)
# Збережіть цей файл поруч з index.html і запустіть: правий клік -> Run with PowerShell

$indexPath = Join-Path $PSScriptRoot 'index.html'
$fullPath = Convert-Path $indexPath

$chromeCandidates = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
)

$chrome = $chromeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if ($chrome) {
    Start-Process -FilePath $chrome -ArgumentList "--new-window", $fullPath
} else {
    # Спробуємо відкрити за назвою (якщо Chrome додано в PATH)
    try {
        Start-Process -FilePath 'chrome' -ArgumentList "--new-window", $fullPath -ErrorAction Stop
    } catch {
        Write-Host "Google Chrome не знайдено. Відкриваю файл у браузері за замовчуванням..."
        Start-Process $fullPath
    }
}
