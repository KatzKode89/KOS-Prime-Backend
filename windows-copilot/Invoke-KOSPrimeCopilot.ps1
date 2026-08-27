[CmdletBinding(DefaultParameterSetName = "File")]
param(
    [Parameter(Mandatory = $true, ParameterSetName = "File")]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string] $InputPath,

    [Parameter(Mandatory = $true, ParameterSetName = "Json")]
    [string] $Json,

    [string] $PythonCommand = "python"
)

$ErrorActionPreference = "Stop"
$agentPath = Join-Path $PSScriptRoot "..\gemini_omni_agent.py"

if (-not (Test-Path -LiteralPath $agentPath -PathType Leaf)) {
    throw "KOS-Prime agent not found at $agentPath"
}

if (-not (Get-Command $PythonCommand -ErrorAction SilentlyContinue)) {
    throw "Python command '$PythonCommand' was not found. Install Python or pass -PythonCommand with its executable path."
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

$inputJson | & $PythonCommand $agentPath
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}