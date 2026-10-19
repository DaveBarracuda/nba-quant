# Registra dos tareas de Windows que conectan el modelo con el NBA Odds Tracker:
#   "NBA Quant Snapshot": 10:00 y 17:00 -> proyecta los partidos de las próximas 36 h y guarda el
#                         número del modelo junto a la línea que ve el tracker en ese momento.
#   "NBA Quant Report":   09:00         -> trae resultados, califica los picks y mide si el mercado
#                         se movió a favor o en contra del modelo (data\reports\tracker_*.csv); regenera
#                         ledger\LEDGER.md y, si cambió, hace commit + push de ledger\ a GitHub.
# Uso:    powershell -ExecutionPolicy Bypass -File scripts\register_model_tasks.ps1
# Quitar: Unregister-ScheduledTask -TaskName "NBA Quant Snapshot","NBA Quant Report" -Confirm:$false
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$python = (Get-Command python).Source
$pythonw = Join-Path (Split-Path $python) "pythonw.exe"   # sin ventana de consola
if (Test-Path $pythonw) { $python = $pythonw }
$runner = Join-Path $root "scripts\run_job.py"
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 45)

$snap = New-ScheduledTaskAction -Execute $python -Argument "`"$runner`" track-snapshot --hours 36" -WorkingDirectory $root
$snapTriggers = @((New-ScheduledTaskTrigger -Daily -At 10:00), (New-ScheduledTaskTrigger -Daily -At 17:00))
Register-ScheduledTask -TaskName "NBA Quant Snapshot" -Action $snap -Trigger $snapTriggers -Settings $settings `
    -Description "Número del modelo vs línea del NBA Odds Tracker" -Force | Out-Null

$rep = New-ScheduledTaskAction -Execute $python -Argument "`"$runner`" track-report --publish-ledger" -WorkingDirectory $root
Register-ScheduledTask -TaskName "NBA Quant Report" -Action $rep -Trigger (New-ScheduledTaskTrigger -Daily -At 09:00) `
    -Settings $settings -Description "WR de los picks y movimiento de mercado vs modelo" -Force | Out-Null
Write-Host "Tareas registradas. Reportes en $root\data\reports\tracker_*.csv"
