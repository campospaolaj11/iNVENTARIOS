# Script para crear tarea programada en Windows
# Ejecutar este archivo con PowerShell como Administrador

$TaskName = "InventarioAutomatico"
$ScriptPath = "C:\Users\ASis2\Desktop\01.-MIS PROYECTOS\INVENTARIOS\excel-automation\automatizacion_programada.py"
$PythonExe = "C:\Users\ASis2\Desktop\01.-MIS PROYECTOS\INVENTARIOS\.venv\Scripts\python.exe"
$WorkingDir = "C:\Users\ASis2\Desktop\01.-MIS PROYECTOS\INVENTARIOS\excel-automation"

Write-Host "🔧 Configurando tarea programada de inventario..." -ForegroundColor Cyan

# Verificar si la tarea ya existe
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "⚠️  La tarea ya existe. Eliminando..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Crear acción (ejecutar Python script)
$Action = New-ScheduledTaskAction -Execute $PythonExe `
    -Argument $ScriptPath `
    -WorkingDirectory $WorkingDir

# Crear triggers (horarios de ejecución)
Write-Host "`n📅 Configurando horarios de ejecución:" -ForegroundColor Green

# Trigger 1: Todos los días a las 8:00 AM
$Trigger1 = New-ScheduledTaskTrigger -Daily -At "08:00"
Write-Host "  ✅ Lunes a Domingo: 8:00 AM" -ForegroundColor Gray

# Trigger 2: Todos los días a las 2:00 PM
$Trigger2 = New-ScheduledTaskTrigger -Daily -At "14:00"
Write-Host "  ✅ Lunes a Domingo: 2:00 PM" -ForegroundColor Gray

# Trigger 3: Todos los días a las 6:00 PM
$Trigger3 = New-ScheduledTaskTrigger -Daily -At "18:00"
Write-Host "  ✅ Lunes a Domingo: 6:00 PM" -ForegroundColor Gray

# Configuración de la tarea
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable:$false

# Principal (usuario que ejecuta la tarea)
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive

# Registrar la tarea con múltiples triggers
Register-ScheduledTask -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger1,$Trigger2,$Trigger3 `
    -Settings $Settings `
    -Principal $Principal `
    -Description "Automatización de inventarios - Actualiza KPIs y genera reportes 3 veces al día"

Write-Host "`n✅ Tarea programada creada exitosamente!" -ForegroundColor Green
Write-Host "`n📋 Información de la tarea:" -ForegroundColor Cyan
Write-Host "  Nombre: $TaskName" -ForegroundColor Gray
Write-Host "  Script: $ScriptPath" -ForegroundColor Gray
Write-Host "  Frecuencia: 3 veces al día (8:00 AM, 2:00 PM, 6:00 PM)" -ForegroundColor Gray
Write-Host "`n🔍 Para ver la tarea creada, ejecuta:" -ForegroundColor Yellow
Write-Host "  Get-ScheduledTask -TaskName '$TaskName' | Format-List *" -ForegroundColor White
Write-Host "`n▶️  Para ejecutar manualmente:" -ForegroundColor Yellow
Write-Host "  Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor White
Write-Host "`n🗑️  Para eliminar la tarea:" -ForegroundColor Yellow
Write-Host "  Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false" -ForegroundColor White
Write-Host "`n✨ Para abrir el Programador de Tareas:" -ForegroundColor Yellow
Write-Host "  taskschd.msc" -ForegroundColor White
