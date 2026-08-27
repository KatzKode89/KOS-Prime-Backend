[CmdletBinding()]
param(
    [string] $SourcePath = (Join-Path $PSScriptRoot "..\builds\steam-windows-x64"),
    [string] $InstallPath = (Join-Path $env:LOCALAPPDATA "KatzStarterForSteam"),
    [switch] $CreateDesktopShortcut,
    [switch] $Launch
)

$ErrorActionPreference = "Stop"
$executable = Join-Path $SourcePath "KatzStarterForSteam.exe"

if (-not (Test-Path -LiteralPath $executable -PathType Leaf)) {
    throw "KatzStarterForSteam.exe was not found at $executable. Build the Unity Windows x64 player first; the repository source ZIP is not a playable installer."
}

$manifestPath = Join-Path $SourcePath "crystalseekers-steam-beta.json"
if (Test-Path -LiteralPath $manifestPath -PathType Leaf) {
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    if ($manifest.package -ne "K@tz-0$-St@rt3r-F0r-St3@m" -or $manifest.data_mode -ne "fake-local") {
        throw "Build manifest does not match the K@tz-0$-St3@m-St@rt3r fake-local package."
    }
}

New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
Copy-Item -Path (Join-Path $SourcePath "*") -Destination $InstallPath -Recurse -Force

if ($CreateDesktopShortcut) {
    $desktop = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktop "KatzStarterForSteam.lnk"
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = (Join-Path $InstallPath "KatzStarterForSteam.exe")
    $shortcut.WorkingDirectory = $InstallPath
    $shortcut.Description = "CrystalSeekers: Echoes of Destiny Starter Demo"
    $shortcut.Save()
}

Write-Output "Installed K@tz-0$-St3@m-St@rt3r to $InstallPath"
if ($CreateDesktopShortcut) {
    Write-Output "Desktop shortcut created."
}
if ($Launch) {
    Start-Process -FilePath (Join-Path $InstallPath "KatzStarterForSteam.exe") -WorkingDirectory $InstallPath
}