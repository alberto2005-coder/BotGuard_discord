import discord
from discord.ext import commands
from discord import app_commands, File
import io
import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional
from openai import OpenAI

load_dotenv()

intents = discord.Intents.default()
intents.members = True  

bot = commands.Bot(command_prefix='!', intents=intents)
# Configurar cliente de Groq
groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


# Variables globales para el sistema de tickets
TICKET_CATEGORIES = {
    'programacion': {'name': 'Soporte Programación', 'emoji': '💻'},
    'cyber': {'name': 'Soporte Ciberseguridad', 'emoji': '🔒'},
    'reportar': {'name': 'Reportar Usuario', 'emoji': '🚨'},
    'sugerencias': {'name': 'Sugerencias', 'emoji': '💡'},
    'staff': {'name': 'Postulación Staff', 'emoji': '👨‍💼'},
    'roles': {'name': 'Solicitar Roles', 'emoji': '🏷️'},
    'alianzas': {'name': 'Alianzas', 'emoji': '🤝'}
}


STAFF_ROLE_ID = None  # ID del rol de staff
TICKET_CATEGORY_ID = None  # ID de la categoría donde se crearán los tickets
LOG_CHANNEL_ID = None  # ID del canal de logs

# Variables para el sistema de bienvenidas
WELCOME_CHANNEL_ID = None  # ID del canal de bienvenidas
WELCOME_ROLE_ID = None  # ID del rol que se asigna automáticamente a nuevos miembros
WELCOME_ENABLED = False  # Si el sistema de bienvenidas está activado

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='💻 Soporte Programación', style=discord.ButtonStyle.primary, custom_id='ticket_programacion')
    async def programacion_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, 'programacion')

    @discord.ui.button(label='🔒 Soporte Ciberseguridad', style=discord.ButtonStyle.primary, custom_id='ticket_cyber')
    async def cyber_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, 'cyber')

    @discord.ui.button(label='🚨 Reportar Usuario', style=discord.ButtonStyle.danger, custom_id='ticket_reportar')
    async def reportar_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, 'reportar')

    @discord.ui.button(label='💡 Sugerencias', style=discord.ButtonStyle.secondary, custom_id='ticket_sugerencias')
    async def sugerencias_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, 'sugerencias')

    @discord.ui.button(label='👨‍💼 Postulación Staff', style=discord.ButtonStyle.success, custom_id='ticket_staff')
    async def staff_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, 'staff')

    @discord.ui.button(label='🏷️ Solicitar Roles', style=discord.ButtonStyle.secondary, custom_id='ticket_roles', row=1)
    async def roles_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, 'roles')

    @discord.ui.button(label='🤝 Alianzas', style=discord.ButtonStyle.success, custom_id='ticket_alianzas', row=1)
    async def alianzas_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, 'alianzas')

    async def create_ticket(self, interaction: discord.Interaction, ticket_type: str):
        guild = interaction.guild
        user = interaction.user
        
        # Verificar si el usuario ya tiene un ticket abierto
        existing_ticket = discord.utils.get(guild.channels, name=f'ticket-{user.name.lower()}-{ticket_type}')
        if existing_ticket:
            await interaction.response.send_message(
                f"❌ Ya tienes un ticket abierto del tipo **{TICKET_CATEGORIES[ticket_type]['name']}**: {existing_ticket.mention}",
                ephemeral=True
            )
            return

        # Crear el canal del ticket
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        # Agregar permisos para el staff si está configurado
        if STAFF_ROLE_ID:
            staff_role = guild.get_role(STAFF_ROLE_ID)
            if staff_role:
                overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        category = None
        if TICKET_CATEGORY_ID:
            category = guild.get_channel(TICKET_CATEGORY_ID)

        ticket_channel = await guild.create_text_channel(
            name=f'ticket-{user.name.lower()}-{ticket_type}',
            overwrites=overwrites,
            category=category,
            topic=f'Ticket de {TICKET_CATEGORIES[ticket_type]["name"]} - {user.display_name}'
        )

        # Embed de bienvenida al ticket
        embed = discord.Embed(
            title=f"{TICKET_CATEGORIES[ticket_type]['emoji']} {TICKET_CATEGORIES[ticket_type]['name']}",
            description=f"¡Hola {user.mention}! Gracias por crear un ticket.\n\n"
                       f"**Tipo de ticket:** {TICKET_CATEGORIES[ticket_type]['name']}\n"
                       f"**Creado:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
                       f"Por favor, describe tu consulta con el mayor detalle posible. "
                       f"Un miembro del staff te atenderá lo antes posible.",
            color=0x00ff00,
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Ticket ID: {ticket_channel.id}")
        embed.set_thumbnail(url=user.display_avatar.url)

        close_view = CloseTicketView()
        await ticket_channel.send(embed=embed, view=close_view)

        await interaction.response.send_message(
            f"✅ Ticket creado exitosamente: {ticket_channel.mention}",
            ephemeral=True
        )

        # Log del ticket creado
        if LOG_CHANNEL_ID:
            log_channel = guild.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                log_embed = discord.Embed(
                    title="📝 Nuevo Ticket Creado",
                    description=f"**Usuario:** {user.mention}\n"
                               f"**Tipo:** {TICKET_CATEGORIES[ticket_type]['name']}\n"
                               f"**Canal:** {ticket_channel.mention}",
                    color=0x00ff00,
                    timestamp=datetime.now()
                )
                await log_channel.send(embed=log_embed)

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='🔒 Cerrar Ticket', style=discord.ButtonStyle.danger, custom_id='close_ticket')
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🔒 Cerrar Ticket",
            description="¿Estás seguro de que deseas cerrar este ticket?\n\n"
                       "Esta acción no se puede deshacer.",
            color=0xff0000
        )
        
        confirm_view = ConfirmCloseView()
        await interaction.response.send_message(embed=embed, view=confirm_view, ephemeral=True)

class ConfirmCloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)

    @discord.ui.button(label='✅ Confirmar', style=discord.ButtonStyle.danger)
    async def confirm_close(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel
        
        # Log del ticket cerrado
        if LOG_CHANNEL_ID:
            log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                log_embed = discord.Embed(
                    title="🔒 Ticket Cerrado",
                    description=f"**Canal:** {channel.name}\n"
                               f"**Cerrado por:** {interaction.user.mention}\n"
                               f"**Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                    color=0xff0000,
                    timestamp=datetime.now()
                )
                await log_channel.send(embed=log_embed)

        await interaction.response.send_message("🔒 Cerrando ticket en 5 segundos...")
        await asyncio.sleep(5)
        await channel.delete()

    @discord.ui.button(label='❌ Cancelar', style=discord.ButtonStyle.secondary)
    async def cancel_close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("❌ Cierre de ticket cancelado.", ephemeral=True)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    
    await bot.change_presence(
        status=discord.Status.online,  # online, idle, dnd, invisible
        activity=discord.Activity(
            type=discord.ActivityType.playing,  # "Jugando"
            name="Building secure code, one line at a time 💻"
        )
    )
    # Sincronizar comandos slash
    try:
        synced = await bot.tree.sync()
        print(f'Sincronizados {len(synced)} comandos slash')
    except Exception as e:
        print(f'Error al sincronizar comandos: {e}')

# Evento para el sistema de bienvenidas
@bot.event
async def on_member_join(member):
    if not WELCOME_ENABLED or not WELCOME_CHANNEL_ID:
        return

    guild = member.guild
    welcome_channel = guild.get_channel(WELCOME_CHANNEL_ID)
    
    if not welcome_channel:
        return

    # Crear embed de bienvenida
    embed = discord.Embed(
        title="🎉 ¡Bienvenido al Servidor!",
        description=f"¡Hola {member.mention}! Bienvenido a **{guild.name}**\n\n"
                   f"🔹 **Miembro #{len(guild.members)}**\n"
                   f"🔹 **Se unió:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
                   f"📋 No olvides leer las reglas del servidor\n"
                   f"🎫 Puedes crear tickets para obtener ayuda\n"
                   f"💬 ¡Esperamos que disfrutes tu estancia aquí!",
        color=0x00ff00,
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"Servidor de Programación y Ciberseguridad", icon_url=guild.icon.url if guild.icon else None)

    try:
        await welcome_channel.send(embed=embed)
        
        # Asignar rol de bienvenida si está configurado
        if WELCOME_ROLE_ID:
            welcome_role = guild.get_role(WELCOME_ROLE_ID)
            if welcome_role:
                try:
                    await member.add_roles(welcome_role, reason="Rol de bienvenida automático")
                except discord.Forbidden:
                    print(f"Error: No se pudo asignar el rol de bienvenida a {member.name}")
                except Exception as e:
                    print(f"Error asignando rol de bienvenida: {e}")

        # Log de bienvenida
        if LOG_CHANNEL_ID:
            log_channel = guild.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                log_embed = discord.Embed(
                    title="👋 Nuevo Miembro",
                    description=f"**Usuario:** {member.mention}\n"
                               f"**Cuenta creada:** {member.created_at.strftime('%d/%m/%Y')}\n"
                               f"**ID:** {member.id}",
                    color=0x00ff00,
                    timestamp=datetime.now()
                )
                log_embed.set_thumbnail(url=member.display_avatar.url)
                await log_channel.send(embed=log_embed)
                
    except Exception as e:
        print(f"Error en sistema de bienvenidas: {e}")


@bot.tree.command(name="ia", description="Pregunta algo a la IA")
@app_commands.describe(prompt="Tu pregunta o instrucción")
async def ia(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()  # Muestra "pensando..."
    try:
        response = groq_client.responses.create(
            model="openai/gpt-oss-20b",
            input=prompt,
        )

        output = response.output_text

        if len(output) > 2000:
            # Crear archivo .txt en memoria
            buffer = io.BytesIO(output.encode("utf-8"))
            file = File(buffer, filename="respuesta_ia.txt")
            await interaction.followup.send("📄 La respuesta es demasiado larga, aquí tienes el archivo:", file=file)
        else:
            await interaction.followup.send(output)

    except Exception as e:
        await interaction.followup.send(f"⚠️ Error: {str(e)}")


# Comando para crear el panel de tickets
@bot.tree.command(name="panel_tickets", description="Crea el panel de tickets interactivo")
@app_commands.describe(channel="Canal donde enviar el panel de tickets")
async def panel_tickets(interaction: discord.Interaction, channel: discord.TextChannel = None):
    # Verificar permisos
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ No tienes permisos para usar este comando.", ephemeral=True)
        return

    target_channel = channel or interaction.channel

    embed = discord.Embed(
        title="🎫 Sistema de Tickets",
        description="¡Bienvenido al sistema de tickets!\n\n"
                   "Selecciona el tipo de ayuda que necesitas haciendo clic en uno de los botones de abajo:\n\n"
                   "💻 **Soporte Programación** - Ayuda con código, debugging y desarrollo\n"
                   "🔒 **Soporte Ciberseguridad** - Consultas sobre seguridad informática\n"
                   "🚨 **Reportar Usuario** - Reportar comportamiento inapropiado\n"
                   "💡 **Sugerencias** - Propuestas para mejorar el servidor\n"
                   "👨‍💼 **Postulación Staff** - Aplicar para ser parte del equipo\n"
                   "🏷️ **Solicitar Roles** - Pedir roles específicos\n"
                   "🤝 **Alianzas** - Propuestas de colaboración\n\n"
                   "*Los tickets son privados y solo tú y el staff pueden verlos.*",
        color=0x0099ff,
        timestamp=datetime.now()
    )
    embed.set_footer(text="Servidor de Programación y Ciberseguridad")

    view = TicketView()
    await target_channel.send(embed=embed, view=view)
    await interaction.response.send_message(f"✅ Panel de tickets enviado a {target_channel.mention}", ephemeral=True)

# Comandos de moderación
@bot.tree.command(name="ban", description="Banea a un usuario del servidor")
@app_commands.describe(user="Usuario a banear", reason="Razón del ban")
async def ban_user(interaction: discord.Interaction, user: discord.Member, reason: str = "No especificada"):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("❌ No tienes permisos para banear usuarios.", ephemeral=True)
        return

    try:
        await user.ban(reason=reason)
        
        embed = discord.Embed(
            title="🔨 Usuario Baneado",
            description=f"**Usuario:** {user.mention} ({user.name})\n"
                       f"**Moderador:** {interaction.user.mention}\n"
                       f"**Razón:** {reason}",
            color=0xff0000,
            timestamp=datetime.now()
        )
        
        await interaction.response.send_message(embed=embed)
        
        # Log de moderación
        if LOG_CHANNEL_ID:
            log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(embed=embed)
                
    except Exception as e:
        await interaction.response.send_message(f"❌ Error al banear usuario: {str(e)}", ephemeral=True)

@bot.tree.command(name="kick", description="Expulsa a un usuario del servidor")
@app_commands.describe(user="Usuario a expulsar", reason="Razón de la expulsión")
async def kick_user(interaction: discord.Interaction, user: discord.Member, reason: str = "No especificada"):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("❌ No tienes permisos para expulsar usuarios.", ephemeral=True)
        return

    try:
        await user.kick(reason=reason)
        
        embed = discord.Embed(
            title="👢 Usuario Expulsado",
            description=f"**Usuario:** {user.mention} ({user.name})\n"
                       f"**Moderador:** {interaction.user.mention}\n"
                       f"**Razón:** {reason}",
            color=0xffa500,
            timestamp=datetime.now()
        )
        
        await interaction.response.send_message(embed=embed)
        
        # Log de moderación
        if LOG_CHANNEL_ID:
            log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(embed=embed)
                
    except Exception as e:
        await interaction.response.send_message(f"❌ Error al expulsar usuario: {str(e)}", ephemeral=True)

@bot.tree.command(name="timeout", description="Silencia temporalmente a un usuario")
@app_commands.describe(user="Usuario a silenciar", duration="Duración en minutos", reason="Razón del timeout")
async def timeout_user(interaction: discord.Interaction, user: discord.Member, duration: int, reason: str = "No especificada"):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("❌ No tienes permisos para silenciar usuarios.", ephemeral=True)
        return

    try:
        timeout_duration = discord.utils.utcnow() + timedelta(minutes=duration)
        await user.timeout(timeout_duration, reason=reason)
        
        embed = discord.Embed(
            title="🔇 Usuario Silenciado",
            description=f"**Usuario:** {user.mention} ({user.name})\n"
                       f"**Moderador:** {interaction.user.mention}\n"
                       f"**Duración:** {duration} minutos\n"
                       f"**Razón:** {reason}",
            color=0xffff00,
            timestamp=datetime.now()
        )
        
        await interaction.response.send_message(embed=embed)
        
        # Log de moderación
        if LOG_CHANNEL_ID:
            log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(embed=embed)
                
    except Exception as e:
        await interaction.response.send_message(f"❌ Error al silenciar usuario: {str(e)}", ephemeral=True)

@bot.tree.command(name="untimeout", description="Quita el silencio a un usuario")
@app_commands.describe(user="Usuario al que quitar el silencio")
async def untimeout_user(interaction: discord.Interaction, user: discord.Member):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("❌ No tienes permisos para quitar silencio a usuarios.", ephemeral=True)
        return

    try:
        await user.timeout(None)
        
        embed = discord.Embed(
            title="🔊 Silencio Removido",
            description=f"**Usuario:** {user.mention} ({user.name})\n"
                       f"**Moderador:** {interaction.user.mention}",
            color=0x00ff00,
            timestamp=datetime.now()
        )
        
        await interaction.response.send_message(embed=embed)
        
        # Log de moderación
        if LOG_CHANNEL_ID:
            log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(embed=embed)
                
    except Exception as e:
        await interaction.response.send_message(f"❌ Error al quitar silencio: {str(e)}", ephemeral=True)

@bot.tree.command(name="clear", description="Elimina mensajes del canal")
@app_commands.describe(amount="Cantidad de mensajes a eliminar (máximo 100)")
async def clear_messages(interaction: discord.Interaction, amount: int):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ No tienes permisos para eliminar mensajes.", ephemeral=True)
        return

    if amount > 100:
        await interaction.response.send_message("❌ No puedes eliminar más de 100 mensajes a la vez.", ephemeral=True)
        return

    try:
        deleted = await interaction.channel.purge(limit=amount)
        
        embed = discord.Embed(
            title="🧹 Mensajes Eliminados",
            description=f"**Cantidad:** {len(deleted)} mensajes\n"
                       f"**Canal:** {interaction.channel.mention}\n"
                       f"**Moderador:** {interaction.user.mention}",
            color=0x00ff00,
            timestamp=datetime.now()
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # Log de moderación
        if LOG_CHANNEL_ID:
            log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(embed=embed)
                
    except Exception as e:
        await interaction.response.send_message(f"❌ Error al eliminar mensajes: {str(e)}", ephemeral=True)

# Comando para crear embeds personalizados
@bot.tree.command(name="embed", description="Crea un mensaje embed personalizado")
@app_commands.describe(
    title="Título del embed",
    description="Descripción del embed",
    color="Color en hexadecimal (ej: 0x00ff00)",
    channel="Canal donde enviar el embed"
)
async def create_embed(interaction: discord.Interaction, title: str, description: str, color: str = "0x0099ff", channel: discord.TextChannel = None):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ No tienes permisos para crear embeds.", ephemeral=True)
        return

    target_channel = channel or interaction.channel

    try:
        # Convertir color hexadecimal
        embed_color = int(color, 16) if color.startswith('0x') else int(f'0x{color}', 16)
        
        embed = discord.Embed(
            title=title,
            description=description,
            color=embed_color,
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Creado por {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)

        await target_channel.send(embed=embed)
        await interaction.response.send_message(f"✅ Embed enviado a {target_channel.mention}", ephemeral=True)
        
    except ValueError:
        await interaction.response.send_message("❌ Color inválido. Usa formato hexadecimal (ej: 0x00ff00)", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error al crear embed: {str(e)}", ephemeral=True)

# Comando de configuración
@bot.tree.command(name="config", description="Configura el bot (solo administradores)")
@app_commands.describe(
    staff_role="Rol de staff para tickets",
    ticket_category="Categoría para crear tickets",
    log_channel="Canal de logs"
)
async def config_bot(interaction: discord.Interaction, staff_role: discord.Role = None, ticket_category: discord.CategoryChannel = None, log_channel: discord.TextChannel = None):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Solo los administradores pueden usar este comando.", ephemeral=True)
        return

    global STAFF_ROLE_ID, TICKET_CATEGORY_ID, LOG_CHANNEL_ID

    config_changes = []
    
    if staff_role:
        STAFF_ROLE_ID = staff_role.id
        config_changes.append(f"**Rol de Staff:** {staff_role.mention}")
    
    if ticket_category:
        TICKET_CATEGORY_ID = ticket_category.id
        config_changes.append(f"**Categoría de Tickets:** {ticket_category.name}")
    
    if log_channel:
        LOG_CHANNEL_ID = log_channel.id
        config_changes.append(f"**Canal de Logs:** {log_channel.mention}")

    if config_changes:
        embed = discord.Embed(
            title="⚙️ Configuración Actualizada",
            description="\n".join(config_changes),
            color=0x00ff00,
            timestamp=datetime.now()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message("❌ No se especificaron cambios de configuración.", ephemeral=True)

# Comando de configuración para el sistema de bienvenidas
@bot.tree.command(name="config_welcome", description="Configura el sistema de bienvenidas (solo administradores)")
@app_commands.describe(
    enable="Activar o desactivar el sistema de bienvenidas",
    welcome_channel="Canal donde se enviarán los mensajes de bienvenida",
    welcome_role="Rol que se asignará automáticamente a nuevos miembros"
)
async def config_welcome(interaction: discord.Interaction, enable: bool = None, welcome_channel: discord.TextChannel = None, welcome_role: discord.Role = None):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Solo los administradores pueden usar este comando.", ephemeral=True)
        return

    global WELCOME_ENABLED, WELCOME_CHANNEL_ID, WELCOME_ROLE_ID

    config_changes = []
    
    if enable is not None:
        WELCOME_ENABLED = enable
        status = "✅ Activado" if enable else "❌ Desactivado"
        config_changes.append(f"**Sistema de Bienvenidas:** {status}")
    
    if welcome_channel:
        WELCOME_CHANNEL_ID = welcome_channel.id
        config_changes.append(f"**Canal de Bienvenidas:** {welcome_channel.mention}")
    
    if welcome_role:
        WELCOME_ROLE_ID = welcome_role.id
        config_changes.append(f"**Rol de Bienvenida:** {welcome_role.mention}")

    if config_changes:
        embed = discord.Embed(
            title="🎉 Configuración de Bienvenidas Actualizada",
            description="\n".join(config_changes),
            color=0x00ff00,
            timestamp=datetime.now()
        )
        
        # Mostrar configuración actual
        current_config = []
        current_config.append(f"**Estado:** {'✅ Activado' if WELCOME_ENABLED else '❌ Desactivado'}")
        
        if WELCOME_CHANNEL_ID:
            channel = interaction.guild.get_channel(WELCOME_CHANNEL_ID)
            current_config.append(f"**Canal:** {channel.mention if channel else 'Canal no encontrado'}")
        else:
            current_config.append("**Canal:** No configurado")
            
        if WELCOME_ROLE_ID:
            role = interaction.guild.get_role(WELCOME_ROLE_ID)
            current_config.append(f"**Rol:** {role.mention if role else 'Rol no encontrado'}")
        else:
            current_config.append("**Rol:** No configurado")
        
        embed.add_field(name="📋 Configuración Actual", value="\n".join(current_config), inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        # Mostrar configuración actual sin cambios
        embed = discord.Embed(
            title="🎉 Configuración de Bienvenidas",
            color=0x0099ff,
            timestamp=datetime.now()
        )
        
        current_config = []
        current_config.append(f"**Estado:** {'✅ Activado' if WELCOME_ENABLED else '❌ Desactivado'}")
        
        if WELCOME_CHANNEL_ID:
            channel = interaction.guild.get_channel(WELCOME_CHANNEL_ID)
            current_config.append(f"**Canal:** {channel.mention if channel else 'Canal no encontrado'}")
        else:
            current_config.append("**Canal:** No configurado")
            
        if WELCOME_ROLE_ID:
            role = interaction.guild.get_role(WELCOME_ROLE_ID)
            current_config.append(f"**Rol:** {role.mention if role else 'Rol no encontrado'}")
        else:
            current_config.append("**Rol:** No configurado")
        
        embed.description = "\n".join(current_config)
        embed.add_field(
            name="💡 Uso", 
            value="Usa los parámetros del comando para cambiar la configuración:\n"
                  "`enable: True/False` - Activar/desactivar\n"
                  "`welcome_channel: #canal` - Canal de bienvenidas\n"
                  "`welcome_role: @rol` - Rol automático", 
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

# Ejecutar el bot
if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not TOKEN:
        print("❌ Error: No se encontró el token del bot. Configura la variable DISCORD_BOT_TOKEN")
    else:
        bot.run(TOKEN)