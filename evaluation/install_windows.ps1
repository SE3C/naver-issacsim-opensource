#requires -Version 5.0
[CmdletBinding()]
param(
    [string]$Destination = 'C:\NCRC',
    [switch]$Preview
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($Destination)) {
    throw 'Destination must be an absolute ASCII Windows path.'
}
if ($Destination -match '[^\x00-\x7F]') {
    throw 'Destination must contain ASCII characters only.'
}
if ($Destination -notmatch '^(?:[A-Za-z]:\\|\\\\)') {
    throw 'Destination must be an absolute drive or UNC path.'
}

try {
    $destinationRoot = [System.IO.Path]::GetFullPath($Destination)
}
catch {
    throw "Destination is not a valid path: $Destination"
}

$copyPlan = @(
    [pscustomobject]@{ SourceName = 'go2_6terrain_video.bat'; RelativeDestination = 'go2_6terrain_video.bat' }
    [pscustomobject]@{ SourceName = 'go2_6terrain_video.ps1'; RelativeDestination = 'go2_6terrain_video.ps1' }
    [pscustomobject]@{ SourceName = 'compare_policies.bat'; RelativeDestination = 'compare_policies.bat' }
    [pscustomobject]@{ SourceName = 'compare_policies.ps1'; RelativeDestination = 'compare_policies.ps1' }
    [pscustomobject]@{ SourceName = 'h1_6terrain_video.bat'; RelativeDestination = 'h1_6terrain_video.bat' }
    [pscustomobject]@{ SourceName = 'h1_6terrain_video.ps1'; RelativeDestination = 'h1_6terrain_video.ps1' }
    [pscustomobject]@{ SourceName = 'eval_core.py'; RelativeDestination = 'go2-video-evaluator\eval_core.py' }
    [pscustomobject]@{ SourceName = 'isaac_runner.py'; RelativeDestination = 'go2-video-evaluator\isaac_runner.py' }
    [pscustomobject]@{ SourceName = 'compare_cli.py'; RelativeDestination = 'go2-video-evaluator\compare_cli.py' }
    [pscustomobject]@{ SourceName = 'windows_bundle_manifest.json'; RelativeDestination = 'go2-video-evaluator\bundle_manifest.json' }
    [pscustomobject]@{ SourceName = 'eval_core.py'; RelativeDestination = 'h1-video-evaluator\eval_core.py' }
    [pscustomobject]@{ SourceName = 'isaac_runner.py'; RelativeDestination = 'h1-video-evaluator\isaac_runner.py' }
    [pscustomobject]@{ SourceName = 'compare_cli.py'; RelativeDestination = 'h1-video-evaluator\compare_cli.py' }
    [pscustomobject]@{ SourceName = 'windows_bundle_manifest.json'; RelativeDestination = 'h1-video-evaluator\bundle_manifest.json' }
)

$missingSources = @()
foreach ($item in $copyPlan) {
    $sourcePath = Join-Path -Path $PSScriptRoot -ChildPath $item.SourceName
    if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
        $missingSources += $item.SourceName
    }
}
if ($missingSources.Count -gt 0) {
    throw ('Missing required installer sources: ' + ($missingSources -join ', '))
}

$manifestPath = Join-Path -Path $PSScriptRoot -ChildPath 'windows_bundle_manifest.json'
try {
    $bundleManifest = [System.IO.File]::ReadAllText($manifestPath) | ConvertFrom-Json -ErrorAction Stop
}
catch {
    throw "Could not parse windows_bundle_manifest.json: $($_.Exception.Message)"
}
if ($null -eq $bundleManifest.file_sha256) {
    throw 'windows_bundle_manifest.json must contain a file_sha256 object.'
}

$sourceHashes = @{}
foreach ($item in $copyPlan) {
    $sourcePath = Join-Path -Path $PSScriptRoot -ChildPath $item.SourceName
    $sourceHashes[$item.SourceName] = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
}

foreach ($pythonName in @('eval_core.py', 'isaac_runner.py', 'compare_cli.py')) {
    $manifestHashProperty = $bundleManifest.file_sha256.PSObject.Properties[$pythonName]
    if ($null -eq $manifestHashProperty) {
        throw "windows_bundle_manifest.json has no file_sha256 entry for $pythonName."
    }

    $declaredHash = [string]$manifestHashProperty.Value
    if ($declaredHash -notmatch '^[A-Fa-f0-9]{64}$') {
        throw "windows_bundle_manifest.json has an invalid SHA-256 for $pythonName."
    }
    if ($sourceHashes[$pythonName] -ne $declaredHash.ToLowerInvariant()) {
        throw "SHA-256 mismatch for $pythonName against windows_bundle_manifest.json."
    }
}

foreach ($powerShellName in @('go2_6terrain_video.ps1', 'h1_6terrain_video.ps1', 'compare_policies.ps1')) {
    $sourcePath = Join-Path -Path $PSScriptRoot -ChildPath $powerShellName
    $tokens = $null
    $parseErrors = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile(
        $sourcePath,
        [ref]$tokens,
        [ref]$parseErrors
    )
    if ($parseErrors.Count -gt 0) {
        $parseMessages = ($parseErrors | ForEach-Object { $_.Message }) -join '; '
        throw "PowerShell parse failed for ${powerShellName}: $parseMessages"
    }
}

if (Test-Path -LiteralPath $destinationRoot -PathType Leaf) {
    throw 'Destination points to an existing file.'
}

$plannedFiles = @()
foreach ($item in $copyPlan) {
    $sourcePath = Join-Path -Path $PSScriptRoot -ChildPath $item.SourceName
    $destinationPath = Join-Path -Path $destinationRoot -ChildPath $item.RelativeDestination
    $parentPath = Split-Path -Parent $destinationPath
    if (Test-Path -LiteralPath $parentPath -PathType Leaf) {
        throw "A destination parent path is an existing file: $parentPath"
    }
    if (Test-Path -LiteralPath $destinationPath -PathType Container) {
        throw "A destination file path is an existing directory: $destinationPath"
    }

    $destinationExists = Test-Path -LiteralPath $destinationPath -PathType Leaf
    if ($destinationExists) {
        $destinationHash = (Get-FileHash -LiteralPath $destinationPath -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($destinationHash -eq $sourceHashes[$item.SourceName]) {
            $operation = 'SKIP (identical)'
        }
        else {
            $operation = 'BACKUP and COPY'
        }
    }
    else {
        $destinationHash = $null
        $operation = 'COPY'
    }

    $plannedFiles += [pscustomobject]@{
        SourceName = $item.SourceName
        RelativeDestination = $item.RelativeDestination
        SourcePath = $sourcePath
        DestinationPath = $destinationPath
        DestinationExists = $destinationExists
        DestinationHash = $destinationHash
        Operation = $operation
        SourceHash = $sourceHashes[$item.SourceName]
    }
}

$backupRunPath = $null
if (@($plannedFiles | Where-Object { $_.Operation -eq 'BACKUP and COPY' }).Count -gt 0) {
    $backupRoot = Join-Path -Path $destinationRoot -ChildPath 'go2-video-suite-backups'
    if (Test-Path -LiteralPath $backupRoot -PathType Leaf) {
        throw "Backup root is an existing file: $backupRoot"
    }
    do {
        $backupRunPath = Join-Path -Path $backupRoot -ChildPath ('install-' + [Guid]::NewGuid().ToString('N'))
    } while (Test-Path -LiteralPath $backupRunPath)
}

Write-Output "Destination: $destinationRoot"
if ($null -ne $backupRunPath) {
    Write-Output "Backup directory for differing files: $backupRunPath"
}
if ($Preview) {
    Write-Output 'Preview only: no files or directories will be created or changed.'
    foreach ($file in $plannedFiles) {
        Write-Output ("{0}: {1}" -f $file.Operation, (Join-Path -Path $destinationRoot -ChildPath $file.RelativeDestination))
    }
    return
}

foreach ($file in $plannedFiles) {
    if ($file.Operation -eq 'SKIP (identical)') {
        Write-Output "Skipped identical file: $($file.RelativeDestination)"
        continue
    }

    if ($file.Operation -eq 'BACKUP and COPY') {
        $backupPath = Join-Path -Path $backupRunPath -ChildPath $file.RelativeDestination
        $backupParent = Split-Path -Parent $backupPath
        [void][System.IO.Directory]::CreateDirectory($backupParent)
        Copy-Item -LiteralPath $file.DestinationPath -Destination $backupPath -ErrorAction Stop
        $backupHash = (Get-FileHash -LiteralPath $backupPath -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($backupHash -ne $file.DestinationHash) {
            throw "Backup verification failed for $($file.RelativeDestination); original was left in place."
        }
    }

    $destinationParent = Split-Path -Parent $file.DestinationPath
    [void][System.IO.Directory]::CreateDirectory($destinationParent)
    Copy-Item -LiteralPath $file.SourcePath -Destination $file.DestinationPath -Force -ErrorAction Stop
    $installedHash = (Get-FileHash -LiteralPath $file.DestinationPath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($installedHash -ne $file.SourceHash) {
        throw "Copied-file verification failed for $($file.RelativeDestination)."
    }
    Write-Output "Installed and verified: $($file.RelativeDestination)"
}
