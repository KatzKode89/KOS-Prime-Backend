[CmdletBinding()]
param(
    [string] $SourcePath = (Join-Path $PSScriptRoot "..\publish\win-x64"),
    [string] $InstallPath = (Join-Path $env:LOCALAPPDATA "KOS-Prime\bin"),
    [switch] $AddToUserPath
)

$ErrorActionPreference = "Stop"
$executable = Join-Path $SourcePath "KOSPrime.Runner.exe"
if (-not (Test-Path -LiteralPath $executable -PathType Leaf)) {
    throw "Windows executable not found at $executable. Run the publish command in docs/windows-exe.md first."
}

New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
Copy-Item -Path (Join-Path $SourcePath "*") -Destination $InstallPath -Recurse -Force

if ($AddToUserPath) {
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $entries = @($currentPath -split ";" | Where-Object { $_ })
    if ($entries -notcontains $InstallPath) {
        [Environment]::SetEnvironmentVariable("Path", (($entries + $InstallPath) -join ";"), "User")
    }
}

Write-Output "Installed KOS-Prime to $InstallPath"
Write-Output "Run: $(Join-Path $InstallPath 'KOSPrime.Runner.exe') --health 85"