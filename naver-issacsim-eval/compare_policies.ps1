param(
    [Parameter(Position = 0)][string]$A,
    [Parameter(Position = 1)][string]$B,
    [ValidateSet("go2", "h1")][string]$Robot = "go2",
    [ValidateRange(1, 4096)][int]$NumEnvs = 128,
    [string]$Seeds = "4201,4202,4203",
    [ValidateSet("scenario7", "terrain6")][string]$Suite = "scenario7",
    [switch]$PolicyA,
    [switch]$PolicyB,
    [switch]$Preview,
    [string]$Calibration,
    [string]$Output,
    [string]$EvalRoot,
    [string]$LabRoot = "C:\NCRC\IsaacLab",
    [string]$TaskRoot
)

$ErrorActionPreference = "Stop"
try {
    if ($env:ISSACSIMZ_MODE -and $env:ISSACSIMZ_MODE.Trim().ToLowerInvariant() -ne "personal") {
        throw "This comparison CLI is PERSONAL only."
    }
    Write-Host "PERSONAL policy comparison - A=candidate, B=reference" -ForegroundColor Cyan
    Write-Host "Two full sequential evaluations / camera off / no training, publish, or shutdown."
    if ([string]::IsNullOrWhiteSpace($A)) { $A = Read-Host "Candidate A .pt (or completed evaluation folder)" }
    if ([string]::IsNullOrWhiteSpace($B)) { $B = Read-Host "Reference B .pt (or completed evaluation folder)" }
    $A = $A.Trim().Trim('"').Trim("'")
    $B = $B.Trim().Trim('"').Trim("'")
    if ([string]::IsNullOrWhiteSpace($A) -or [string]::IsNullOrWhiteSpace($B)) { throw "Both paths are required." }
    foreach ($InputPath in @($A, $B)) {
        if (-not (Test-Path -LiteralPath $InputPath)) { throw ("Input does not exist: " + $InputPath) }
    }
    if (-not $EvalRoot) {
        $EvalRoot = $PSScriptRoot
        if (-not (Test-Path -LiteralPath (Join-Path $EvalRoot "compare_cli.py"))) {
            $EvalRoot = Join-Path $PSScriptRoot "naver-issacsim-eval"
        }
    }
    if (-not $TaskRoot) {
        $TaskRoot = if ($Robot -eq "h1") { "C:\NCRC\naver-issacsim-nvidia\training\humanoid" }
                    else { "C:\NCRC\naver-issacsim-nvidia\training\quadruped" }
    }
    $SavedEvaluations = (Test-Path -LiteralPath $A -PathType Container) -and
                        (Test-Path -LiteralPath $B -PathType Container)
    $PythonPrefix = @()
    if ($SavedEvaluations) {
        $Python = Get-Command py.exe -ErrorAction SilentlyContinue
        if ($Python) { $PythonPrefix = @("-3") }
        else { $Python = Get-Command python.exe -ErrorAction SilentlyContinue }
        if (-not $Python) { throw "Saved evaluation comparison requires Python 3 (py.exe or python.exe)." }
        $Launcher = $Python.Source
    }
    else { $Launcher = Join-Path $LabRoot "_isaac_sim\python.bat" }
    $Driver = Join-Path $EvalRoot "compare_cli.py"
    foreach ($Required in @($Launcher, $Driver)) {
        if (-not (Test-Path -LiteralPath $Required -PathType Leaf)) { throw ("Missing: " + $Required) }
    }
    $RunnerArgs = $PythonPrefix + @("-u", $Driver, "--a", $A, "--b", $B, "--robot", $Robot,
        "--isaaclab-root", $LabRoot, "--task-root", $TaskRoot,
        "--num-envs", [string]$NumEnvs, "--seeds", $Seeds, "--suite", $Suite)
    if ($PolicyA) { $RunnerArgs += "--policy-a" }
    if ($PolicyB) { $RunnerArgs += "--policy-b" }
    if ($Calibration) { $RunnerArgs += @("--calibration", $Calibration) }
    if ($Output) { $RunnerArgs += @("--output", $Output) }
    if ($Preview) {
        Write-Host "[PREVIEW] No process launched; no output directory created."
        Write-Host ("[LAUNCHER] " + $Launcher)
        Write-Host ($RunnerArgs | ConvertTo-Json)
        exit 0
    }
    if (-not $SavedEvaluations -and (Get-Process kit -ErrorAction SilentlyContinue)) {
        throw "Kit is running. Finish the video render before starting evaluation."
    }
    $OldEnvironment = @{}
    foreach ($Key in @("OMNI_CONFIG_PATH", "ISAACLAB_PATH", "WARP_CACHE_PATH")) {
        $OldEnvironment[$Key] = [Environment]::GetEnvironmentVariable($Key, "Process")
    }
    try {
        if (-not $SavedEvaluations) {
            $env:OMNI_CONFIG_PATH = "C:\ov-config"
            $env:ISAACLAB_PATH = $LabRoot
            $env:WARP_CACHE_PATH = "C:\ov\warp-cache"
            New-Item -ItemType Directory -Force $env:WARP_CACHE_PATH | Out-Null
        }
        & $Launcher @RunnerArgs
        $ExitCode = $LASTEXITCODE
        if ($ExitCode -ne 0) { throw ("Comparison failed, exit=" + $ExitCode) }
        Write-Host "Comparison finished. Open comparison.html in the reported output directory." -ForegroundColor Green
    }
    finally {
        foreach ($Key in $OldEnvironment.Keys) {
            [Environment]::SetEnvironmentVariable($Key, $OldEnvironment[$Key], "Process")
        }
    }
    exit 0
}
catch {
    Write-Host ("COMPARISON FAILED: " + $_.Exception.Message) -ForegroundColor Red
    exit 1
}
