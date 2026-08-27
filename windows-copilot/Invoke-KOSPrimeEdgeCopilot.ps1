[CmdletBinding(DefaultParameterSetName = "File")]
param(
    [Parameter(Mandatory = $true, ParameterSetName = "File")]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string] $InputPath,

    [Parameter(Mandatory = $true, ParameterSetName = "Json")]
    [string] $Json,

    [switch] $UseWsl,
    [switch] $OpenEdge,
    [string] $OutputPath = (Join-Path (Get-Location) "kos-prime-edge-handoff.json"),
    [string] $Distribution = "Ubuntu",
    [string] $LinuxRepoPath = "/home/$env:USERNAME/kos-prime",
    [string] $PythonCommand = "python"
)

$ErrorActionPreference = "Stop"
$inputJson = if ($PSCmdlet.ParameterSetName -eq "File") {
    Get-Content -LiteralPath $InputPath -Raw
}
else {
    $Json
}

try {
    $inputObject = $inputJson | ConvertFrom-Json
}
catch {
    throw "Input is not valid JSON: $($_.Exception.Message)"
}

if ($null -eq $inputObject -or $inputObject -is [array]) {
    throw "Input must be a JSON object packet."
}

$launcherPath = if ($UseWsl) {
    Join-Path $PSScriptRoot "Invoke-KOSPrimeWsl.ps1"
}
else {
    Join-Path $PSScriptRoot "Invoke-KOSPrimeCopilot.ps1"
}

$launcherArguments = @{}
if ($PSCmdlet.ParameterSetName -eq "File") {
    $launcherArguments["InputPath"] = $InputPath
}
else {
    $launcherArguments["Json"] = $Json
}

if ($UseWsl) {
    $launcherArguments["Distribution"] = $Distribution
    $launcherArguments["LinuxRepoPath"] = $LinuxRepoPath
}
else {
    $launcherArguments["PythonCommand"] = $PythonCommand
}

$responseText = & $launcherPath @launcherArguments | Out-String
if ($null -ne $LASTEXITCODE -and $LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

try {
    $response = $responseText | ConvertFrom-Json
}
catch {
    throw "KOS-Prime returned invalid JSON: $($_.Exception.Message)"
}

$responseText.Trim() | Set-Content -LiteralPath $OutputPath -Encoding UTF8

if ($OpenEdge) {
    $edge = Get-Command "msedge.exe" -ErrorAction SilentlyContinue
    if ($null -ne $edge) {
        Start-Process -FilePath $edge.Source -ArgumentList "https://copilot.microsoft.com/"
    }
    else {
        Start-Process "https://copilot.microsoft.com/"
    }
    Write-Verbose "Opened Microsoft Copilot in Edge. Handoff saved to $OutputPath"
}

$responseText.Trim()