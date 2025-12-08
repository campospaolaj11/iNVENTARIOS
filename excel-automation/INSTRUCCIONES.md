# INSTRUCCIONES DE USO - AUTOMATIZACIÓN DE INVENTARIOS
# =========================================================

## 📁 ARCHIVOS CREADOS

1. **automatizacion_completa.py**
   - Genera Excel desde JSON
   - Importa Excel a JSON
   - Exporta KPIs a Excel
   - Formato profesional con estilos

2. **automatizacion_programada.py**
   - Calcula KPIs automáticamente
   - Genera reportes diarios
   - Sistema de logs
   - Ideal para ejecución programada

3. **configurar_tarea_programada.ps1**
   - Script PowerShell para Windows Task Scheduler
   - Programa 3 ejecuciones diarias (8 AM, 2 PM, 6 PM)

## 🚀 CÓMO USAR

### Opción 1: Ejecución Manual
```powershell
cd "C:\Users\ASis2\Desktop\01.-MIS PROYECTOS\INVENTARIOS\excel-automation"
& "C:\Users\ASis2\Desktop\01.-MIS PROYECTOS\INVENTARIOS\.venv\Scripts\python.exe" automatizacion_completa.py
```

### Opción 2: Programar Automáticamente

1. **Abrir PowerShell como Administrador**
   - Click derecho en PowerShell
   - "Ejecutar como Administrador"

2. **Ejecutar el configurador**
   ```powershell
   cd "C:\Users\ASis2\Desktop\01.-MIS PROYECTOS\INVENTARIOS\excel-automation"
   .\configurar_tarea_programada.ps1
   ```

3. **Verificar la tarea creada**
   ```powershell
   Get-ScheduledTask -TaskName "InventarioAutomatico"
   ```

4. **Probar manualmente**
   ```powershell
   Start-ScheduledTask -TaskName "InventarioAutomatico"
   ```

## 📊 ARCHIVOS GENERADOS

Después de ejecutar, encontrarás:

- `inventario_completo.xlsx` - Excel con 4 hojas (Inventario, Stock Crítico, Resumen, KPIs)
- `productos_importados.json` - JSON generado desde Excel
- `kpis_dashboard.xlsx` - KPIs exportados
- `reporte_diario_YYYY-MM-DD.xlsx` - Reportes diarios automáticos
- `kpis_calculados.json` - KPIs en formato JSON
- `automation_log.txt` - Log de todas las ejecuciones

## ⚙️ CONFIGURACIÓN

### Cambiar horarios de ejecución

Edita `configurar_tarea_programada.ps1` y modifica:

```powershell
$Trigger1 = New-ScheduledTaskTrigger -Daily -At "08:00"  # 8:00 AM
$Trigger2 = New-ScheduledTaskTrigger -Daily -At "14:00"  # 2:00 PM
$Trigger3 = New-ScheduledTaskTrigger -Daily -At "18:00"  # 6:00 PM
```

### Ejecutar cada hora

```powershell
$Trigger = New-ScheduledTaskTrigger -Once -At "00:00" -RepetitionInterval (New-TimeSpan -Hours 1)
```

### Ejecutar solo días laborables

```powershell
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At "08:00"
```

## 🔍 MONITOREO

### Ver logs de ejecución
```powershell
type automation_log.txt
```

### Ver últimas 20 líneas del log
```powershell
Get-Content automation_log.txt -Tail 20
```

### Ver historial de la tarea programada
```powershell
Get-ScheduledTaskInfo -TaskName "InventarioAutomatico"
```

### Ver si la tarea está corriendo
```powershell
Get-ScheduledTask -TaskName "InventarioAutomatico" | Select-Object TaskName,State,LastRunTime,NextRunTime
```

## 🛠️ SOLUCIÓN DE PROBLEMAS

### Error: "Cannot be loaded because running scripts is disabled"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "Access Denied"
- Ejecutar PowerShell como Administrador

### La tarea no se ejecuta
1. Verificar que Python está en la ruta correcta
2. Verificar que el script existe
3. Ver logs: `Get-ScheduledTask -TaskName "InventarioAutomatico" | Get-ScheduledTaskInfo`

### Eliminar tarea
```powershell
Unregister-ScheduledTask -TaskName "InventarioAutomatico" -Confirm:$false
```

## 📧 PRÓXIMOS PASOS SUGERIDOS

1. **Integrar con Base de Datos SQL Server**
   - Conectar automatización a base de datos real
   - Sincronizar datos entre Excel y SQL

2. **Envío de Reportes por Email**
   - Agregar funcionalidad para enviar reportes automáticos

3. **Notificaciones de Alertas**
   - Enviar emails cuando stock esté crítico
   - Alertas de productos a reabastecer

4. **Dashboard Web en Tiempo Real**
   - Conectar frontend Netlify con backend Railway
   - Actualización automática desde scripts

## 🎯 COMANDOS RÁPIDOS

```powershell
# Ejecutar ahora
Start-ScheduledTask -TaskName "InventarioAutomatico"

# Ver estado
Get-ScheduledTask -TaskName "InventarioAutomatico"

# Deshabilitar temporalmente
Disable-ScheduledTask -TaskName "InventarioAutomatico"

# Habilitar de nuevo
Enable-ScheduledTask -TaskName "InventarioAutomatico"

# Abrir Programador de Tareas (GUI)
taskschd.msc
```

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [x] Scripts Python creados
- [x] Automatización funcionando manualmente
- [ ] Tarea programada configurada
- [ ] Verificar ejecución automática
- [ ] Configurar SQL Server
- [ ] Desplegar backend a Railway
- [ ] Conectar frontend con backend
- [ ] Configurar emails de alertas
