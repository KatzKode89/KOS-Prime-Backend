[CmdletBinding(DefaultParameterSetName = "File")]
param(
    [Parameter(Mandatory = $true, ParameterSetName = "File")]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string] $InputPath,

    [Parameter(Mandatory = $true, ParameterSetName = "Json")]
    [string] $Json,

    [string] $Distribution = "Ubuntu",
    [string] $LinuxRepoPath = "/home/$env:USERNAME/kos-prime"
)

$ErrorActionPreference = "Stop"
$agentPath = "$LinuxRepoPath/gemini_omni_agent.py"

if (-not (Get-Command wsl.exe -ErrorAction SilentlyContinue)) {
    throw "wsl.exe was not found. Enable WSL2 on Windows before using this launcher."
}

if ($PSCmdlet.ParameterSetName -eq "File") {
    $inputJson = Get-Content -LiteralPath $InputPath -Raw
}
else {
    $inputJson = $Json
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

$inputJson | & wsl.exe -d $Distribution --exec python3 $agentPath
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}