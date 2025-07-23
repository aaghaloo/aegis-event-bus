# scripts/use-local-env.ps1
# Loads .env.local into current PowerShell session (process scope).

$envFile = ".env.local"
if (-not (Test-Path $envFile)) {
    Write-Error "File $envFile not found. Create it first."
    exit 1
}

Get-Content $envFile |
    Where-Object { $_ -match '^[A-Za-z_][A-Za-z0-9_]*=' } |
    ForEach-Object {
        $line = $_.Trim()
        if ($line.StartsWith("#")) { return }
        $parts = $line -split '=', 2
        $name  = $parts[0].Trim()
        $val   = $parts[1].Trim().Trim('"')
        Set-Item -Path "Env:$name" -Value $val
    }

Write-Host "Loaded .env.local. Example: `n  DATABASE_URL = $($env:DATABASE_URL)"
