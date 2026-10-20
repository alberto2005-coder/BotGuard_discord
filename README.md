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

---

# English Version

# Discord Ticketing and Moderation Bot

## Description
A complete Discord bot with an interactive ticket system and moderation commands for programming and cybersecurity servers.

## Implemented Features

### Ticket System
- ✅ Interactive panel with buttons to create tickets
- ✅ 7 ticket categories:
  - 💻 Programming Support
  - 🔒 Cybersecurity Support
  - 🚨 Report a User
  - 💡 Suggestions
  - 👨‍💼 Staff Application
  - 🏷️ Request Roles
  - 🤝 Alliances
- ✅ Automatic creation of private channels
- ✅ Ticket closing system with confirmation
- ✅ Automatic logs of creation and closing

### Moderation Slash Commands
- ✅ `/ban` - Ban users
- ✅ `/kick` - Kick users
- ✅ `/timeout` - Temporarily mute users
- ✅ `/untimeout` - Remove mute from users
- ✅ `/clear` - Delete messages from the channel

### Additional Features
- ✅ `/embed` - Create custom embed messages
- ✅ `/panel_tickets` - Create the interactive ticket panel
- ✅ `/config` - Configure staff roles, categories and log channels
- ✅ `/config_welcome` - Configure the automatic welcome system

### Welcome System
- ✅ Automatic welcome message with custom embed
- ✅ Automatic role assignment to new members
- ✅ Logs of new members in the moderation channel
- ✅ Full configuration via the `/config_welcome` command

## Project Status
- **Bot Status**: ⚠️ REQUIRES CONFIGURATION
- **Synced Commands**: ✅ 9 slash commands (including the welcome system)
- **Discord Connection**: ⚠️ Requires enabling "Server Members Intent"

## Required Configuration

### For Server Administrators
1. **Configure the bot using `/config`**:
   - Set the staff role for ticket access
   - Define the category where tickets are created
   - Configure the log channel for moderation

2. **Enable Privileged Intents** (REQUIRED for the welcome system):
   - Go to https://discord.com/developers/applications/
   - Select your bot application
   - In the "Bot" section, enable:
     - **Server Members Intent** (MANDATORY for welcomes)
     - Message Content Intent (recommended for commands)
   - Without "Server Members Intent" the welcome system will NOT work

3. **Configure the welcome system using `/config_welcome`**:
   - Set the welcome channel: `/config_welcome welcome_channel:#bienvenidas`
   - Enable the system: `/config_welcome enable:True`
   - Auto role (optional): `/config_welcome welcome_role:@NewMember`

### Using the Ticket System
1. Run `/panel_tickets` in the desired channel
2. Users can click the buttons to create tickets
3. Private channels are created automatically
4. Staff can close tickets using the "🔒 Close Ticket" button

## Technologies Used
- Python 3.11
- discord.py 2.6.3
- python-dotenv
- Slash Commands (Interactions API)
- Discord UI Components (Buttons, Views)

## Technical Notes
- The bot uses basic intents by default (no special privileges required)
- **For the welcome system:** Requires enabling "Server Members Intent"
- All commands include permission checks
- Automatic logging system for auditing
- Error handling and informative messages
- Interface fully in Spanish

