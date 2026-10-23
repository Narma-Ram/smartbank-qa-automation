param(
    [Parameter(Mandatory = $true)]
    [string[]]$Paths
)

foreach ($path in $Paths) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        Write-Warning "File not found: $path"
        continue
    }

    $content = [System.IO.File]::ReadAllText($path)
    $cleaned = [regex]::Replace($content, '(?m)[ \t]+(?=\r?$)', '')

    if ($cleaned -ne $content) {
        [System.IO.File]::WriteAllText(
            $path,
            $cleaned,
            [System.Text.UTF8Encoding]::new($false)
        )

        Write-Output "Cleaned: $path"
    }
    else {
        Write-Output "Already clean: $path"
    }
}
