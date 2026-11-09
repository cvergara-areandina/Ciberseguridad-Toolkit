<#
.SYNOPSIS
    Utilidades de analisis para Windows.
.DESCRIPTION
    Funciones de reconocimiento local: hashes, cabeceras de correo, procesos,
    conexiones de red, archivos sospechosos, persistencia y reporte.
    Solo lectura: no modifica el sistema.

---
id: TOOL-GES-002
type: tool
title: security_tools
summary: Funciones PowerShell de reconocimiento local en Windows (hashes, procesos, red, persistencia).
tags: [windows, powershell, forensics, triage]
network: none
version: 1.0.0
status: stable
---
#>

function Get-FileHashes {
    <#
    .SYNOPSIS
        Calcula hashes MD5, SHA1 y SHA256 de un archivo.
    #>
    param([Parameter(Mandatory)] [string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        Write-Error "Archivo no encontrado: $Path"
        return
    }

    [PSCustomObject]@{
        File   = (Resolve-Path -LiteralPath $Path).Path
        MD5    = (Get-FileHash -LiteralPath $Path -Algorithm MD5).Hash
        SHA1   = (Get-FileHash -LiteralPath $Path -Algorithm SHA1).Hash
        SHA256 = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
    }
}

function Test-EmailHeader {
    <#
    .SYNOPSIS
        Busca patrones sospechosos en cabeceras de correo.
    #>
    param([Parameter(ValueFromPipeline)] [string]$HeaderContent)

    begin { $content = @() }
    process { $content += $_ }
    end {
        $fullText = $content -join "`n"
        $patterns = @(
            @{ Name = "SPF fail";    Pattern = "spf=(fail|softfail)" }
            @{ Name = "DKIM fail";   Pattern = "dkim=fail" }
            @{ Name = "DMARC fail";  Pattern = "dmarc=fail" }
            @{ Name = "Sin auth";    Pattern = "(?i)^(?!.*Authentication-Results)" }
        )

        foreach ($item in $patterns) {
            if ($fullText -match $item.Pattern) {
                [PSCustomObject]@{ Finding = $item.Name; Severity = "Warning" }
            }
        }
    }
}

function Get-NetworkConnections {
    <#
    .SYNOPSIS
        Lista conexiones TCP activas con el proceso propietario.
    #>
    Get-NetTCPConnection -ErrorAction SilentlyContinue | ForEach-Object {
        $proc = Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue
        [PSCustomObject]@{
            LocalAddress  = $_.LocalAddress
            LocalPort     = $_.LocalPort
            RemoteAddress = $_.RemoteAddress
            RemotePort    = $_.RemotePort
            State         = $_.State
            ProcessName   = if ($proc) { $proc.ProcessName } else { "Unknown" }
            PID           = $_.OwningProcess
        }
    } | Sort-Object State, RemoteAddress
}

function Find-SuspiciousFiles {
    <#
    .SYNOPSIS
        Busca archivos con extensiones de riesgo en ubicaciones habituales.
    #>
    param(
        [string[]]$Paths = @("$env:TEMP", "$env:USERPROFILE\Downloads", "$env:USERPROFILE\Desktop"),
        [switch]$Recurse
    )

    $extensions = @(".exe", ".scr", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".jar", ".hta", ".iso", ".dll")

    foreach ($path in $Paths) {
        if (Test-Path -LiteralPath $path) {
            Get-ChildItem -LiteralPath $path -Recurse:$Recurse -ErrorAction SilentlyContinue |
                Where-Object { $_.Extension -in $extensions } |
                Select-Object FullName, Length, CreationTime, LastWriteTime, Extension
        }
    }
}

function Get-PersistencePoints {
    <#
    .SYNOPSIS
        Enumera puntos de persistencia comunes en Windows.
    #>
    $persistence = @()

    $runPaths = @(
        "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run",
        "HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce",
        "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run",
        "HKCU:\Software\Microsoft\Windows\CurrentVersion\RunOnce"
    )
    foreach ($path in $runPaths) {
        if (Test-Path -LiteralPath $path) {
            $props = Get-ItemProperty -LiteralPath $path -ErrorAction SilentlyContinue
            foreach ($prop in $props.PSObject.Properties) {
                if ($prop.Name -notlike "PS*") {
                    $persistence += [PSCustomObject]@{
                        Type = "Registry Run"; Path = $path; Name = $prop.Name; Value = $prop.Value
                    }
                }
            }
        }
    }

    Get-ScheduledTask -ErrorAction SilentlyContinue |
        Where-Object { $_.State -ne "Disabled" } |
        ForEach-Object {
            $persistence += [PSCustomObject]@{
                Type = "Scheduled Task"; Path = $_.TaskPath; Name = $_.TaskName; Value = $_.State
            }
        }

    $startup = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
    if (Test-Path -LiteralPath $startup) {
        Get-ChildItem -LiteralPath $startup -ErrorAction SilentlyContinue | ForEach-Object {
            $persistence += [PSCustomObject]@{
                Type = "Startup Folder"; Path = $startup; Name = $_.Name; Value = $_.Length
            }
        }
    }

    return $persistence
}

function Export-SecurityReport {
    <#
    .SYNOPSIS
        Genera un reporte de reconocimiento local en texto.
    #>
    param([string]$OutputPath = ".\security_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt")

    $report = @"
========================================
SECURITY REPORT
Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
Host: $env:COMPUTERNAME
========================================

1. NETWORK CONNECTIONS
$(Get-NetworkConnections | Format-Table -AutoSize | Out-String)

2. SUSPICIOUS FILES
$(Find-SuspiciousFiles | Format-Table -AutoSize | Out-String)

3. PERSISTENCE POINTS
$(Get-PersistencePoints | Format-Table -AutoSize | Out-String)

4. TOP PROCESSES BY CPU
$(Get-Process | Sort-Object CPU -Descending | Select-Object -First 20 Name, CPU, WorkingSet, Id | Format-Table -AutoSize | Out-String)

========================================
END OF REPORT
========================================
"@

    $directory = Split-Path -Path $OutputPath -Parent
    if ($directory -and -not (Test-Path -LiteralPath $directory)) {
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
    }

    $report | Out-File -FilePath $OutputPath -Encoding utf8
    Write-Host "Reporte guardado en: $OutputPath"
}
