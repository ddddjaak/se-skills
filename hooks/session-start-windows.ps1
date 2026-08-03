# Windows SessionStart launcher for the plugin's bash hook.
# Codex runs Windows hooks through cmd.exe; resolve Git Bash explicitly and
# never fail the session when bash or the meta-skill is unavailable.

$ErrorActionPreference = "Continue"

$pluginRoot = $env:PLUGIN_ROOT
if ([string]::IsNullOrWhiteSpace($pluginRoot)) { exit 0 }

$hookScript = Join-Path $pluginRoot "hooks\session-start.sh"
if (-not (Test-Path -LiteralPath $hookScript -PathType Leaf)) { exit 0 }

$bash = $null
$candidates = @()
if (-not [string]::IsNullOrWhiteSpace($env:ProgramFiles)) {
    $candidates += (Join-Path $env:ProgramFiles "Git\bin\bash.exe")
}
$programFilesX86 = ${env:ProgramFiles(x86)}
if (-not [string]::IsNullOrWhiteSpace($programFilesX86)) {
    $candidates += (Join-Path $programFilesX86 "Git\bin\bash.exe")
}
foreach ($candidate in $candidates) {
    if (Test-Path -LiteralPath $candidate -PathType Leaf) {
        $bash = $candidate
        break
    }
}
if ($null -eq $bash) {
    $onPath = Get-Command bash -CommandType Application -ErrorAction SilentlyContinue
    if ($null -ne $onPath -and $onPath.Source -notlike "*\Windows\System32\*") {
        $bash = @($onPath)[0].Source
    }
}
if ($null -eq $bash) {
    Write-Output '{"priority":"INFO","message":"Plugin SessionStart hook: Git Bash is required but was not found on PATH. Plugin skills remain available individually."}'
    exit 0
}

$bashHook = $hookScript.Replace("\", "/")
& $bash -lc "'$bashHook'"
exit 0
