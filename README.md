# Discord Bot de Tickets y Moderación

## Descripción
Bot de Discord completo con sistema de tickets interactivo y comandos de moderación para servidores de programación y ciberseguridad.

## Características Implementadas

### Sistema de Tickets
- ✅ Panel interactivo con botones para crear tickets
- ✅ 7 categorías de tickets:
  - 💻 Soporte Programación
  - 🔒 Soporte Ciberseguridad  
  - 🚨 Reportar Usuario
  - 💡 Sugerencias
  - 👨‍💼 Postulación Staff
  - 🏷️ Solicitar Roles
  - 🤝 Alianzas
- ✅ Creación automática de canales privados
- ✅ Sistema de cierre de tickets con confirmación
- ✅ Logs automáticos de creación y cierre

### Comandos Slash de Moderación
- ✅ `/ban` - Banear usuarios
- ✅ `/kick` - Expulsar usuarios
- ✅ `/timeout` - Silenciar temporalmente usuarios
- ✅ `/untimeout` - Quitar silencio a usuarios
- ✅ `/clear` - Eliminar mensajes del canal

### Funcionalidades Adicionales
- ✅ `/embed` - Crear mensajes embed personalizados
- ✅ `/panel_tickets` - Crear panel de tickets interactivo
- ✅ `/config` - Configurar roles de staff, categorías y canales de logs
- ✅ `/config_welcome` - Configurar sistema de bienvenidas automático

### Sistema de Bienvenidas
- ✅ Mensaje automático de bienvenida con embed personalizado
- ✅ Asignación automática de roles a nuevos miembros
- ✅ Logs de nuevos miembros en canal de moderación
- ✅ Configuración completa a través de comando `/config_welcome`

## Estado del Proyecto
- **Bot Status**: ⚠️ REQUIERE CONFIGURACIÓN
- **Comandos Sincronizados**: ✅ 9 comandos slash (incluye sistema de bienvenidas)
- **Conexión Discord**: ⚠️ Requiere habilitar "Server Members Intent"

## Configuración Requerida

### Para Administradores del Servidor
1. **Configurar el bot usando `/config`**:
   - Establecer rol de staff para acceso a tickets
   - Definir categoría donde crear tickets
   - Configurar canal de logs para moderación

2. **Habilitar Intents Privilegiados** (REQUERIDO para sistema de bienvenidas):
   - Ve a https://discord.com/developers/applications/
   - Selecciona tu aplicación bot
   - En la sección "Bot", habilita:
     - **Server Members Intent** (OBLIGATORIO para bienvenidas)
     - Message Content Intent (recomendado para comandos)
   - Sin "Server Members Intent" el sistema de bienvenidas NO funcionará

3. **Configurar el sistema de bienvenidas usando `/config_welcome`**:
   - Establecer canal de bienvenidas: `/config_welcome welcome_channel:#bienvenidas`
   - Activar el sistema: `/config_welcome enable:True`
   - Rol automático (opcional): `/config_welcome welcome_role:@NuevoMiembro`

### Uso del Sistema de Tickets
1. Ejecuta `/panel_tickets` en el canal deseado
2. Los usuarios podrán hacer clic en los botones para crear tickets
3. Se crearán canales privados automáticamente
4. El staff puede cerrar tickets usando el botón "🔒 Cerrar Ticket"

## Tecnologías Utilizadas
- Python 3.11
- discord.py 2.6.3
- python-dotenv
- Slash Commands (Interactions API)
- Discord UI Components (Buttons, Views)

## Notas Técnicas
- El bot usa intents básicos por defecto (no requiere privilegios especiales)
- **Para el sistema de bienvenidas:** Requiere habilitar "Server Members Intent"
- Todos los comandos incluyen verificación de permisos
- Sistema de logs automático para auditoría
- Manejo de errores y mensajes informativos
- Interfaz completamente en español