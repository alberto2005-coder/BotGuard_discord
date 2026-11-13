# BotGuard — tickets y moderación para Discord

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2?logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![MIT](https://img.shields.io/badge/Licencia-MIT-green)](LICENSE)

[Español](#español) · [English](#english)

---

## Español

### Índice

- [Descripción](#descripción)
- [Sistema de tickets](#sistema-de-tickets)
- [Comandos](#comandos)
- [Sistema de bienvenidas](#sistema-de-bienvenidas)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Licencia](#licencia)

### Descripción

**BotGuard** es un bot de Discord en **Python** pensado para servidores de programación y ciberseguridad. Combina un sistema de **tickets** con botones y canales privados, comandos de **moderación**, mensajes embed, bienvenidas automáticas y un comando de **IA** conectado a Groq.

La interfaz del bot está en español.

### Sistema de tickets

- Panel interactivo creado con `/panel_tickets`.
- Siete categorías: soporte de programación, ciberseguridad, reportar usuario, sugerencias, postulación de staff, solicitud de roles y alianzas.
- Cada ticket crea un **canal privado** visible solo para el usuario y el staff.
- Cierre con confirmación desde el propio ticket.
- **Logs automáticos** de apertura y cierre.

### Comandos

| Comando | Qué hace |
|---|---|
| `/panel_tickets` | Publica el panel de tickets con botones |
| `/config` | Configura rol de staff, categoría de tickets y canal de logs |
| `/config_welcome` | Configura canal, rol automático y activación de bienvenidas |
| `/ban` | Banea a un usuario |
| `/kick` | Expulsa a un usuario |
| `/timeout` | Silencia temporalmente |
| `/untimeout` | Retira el silencio |
| `/clear` | Borra mensajes del canal |
| `/embed` | Crea un mensaje embed personalizado |
| `/ia` | Consulta el modelo de Groq configurado |

Todos los comandos de moderación comprueban permisos antes de actuar.

### Sistema de bienvenidas

- Mensaje de bienvenida con embed personalizable.
- Asignación automática de un rol a los nuevos miembros.
- Registro de nuevas incorporaciones en el canal de moderación.
- Se activa y configura con `/config_welcome`.

### Estructura del proyecto

```text
BotGuard_discord/
├── main.py            # Bot, tickets, moderación, bienvenidas e IA
├── requirements.txt
├── .env.example       # Variables necesarias
├── LICENSE
└── README.md
```

### Requisitos

- **Python 3.11** o superior.
- Una aplicación de bot en el [Discord Developer Portal](https://discord.com/developers/applications).
- Una clave de **Groq** si quieres usar `/ia`.
- Permisos de **bot**, **applications.commands** y **Manage Channels**, **Manage Roles**, **Kick Members**, **Ban Members** y **Moderate Members** según lo que vayas a usar.

### Instalación

```bash
git clone https://github.com/alberto2005-coder/BotGuard_discord.git
cd BotGuard_discord
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install discord.py python-dotenv openai
```

> [!NOTE]
> `requirements.txt` incluye tanto `discord.py` como `py-cord`. Ambos instaladores exponen el módulo `discord`, así que pueden pisarse: instala solo uno. El código usa **discord.py**, que es el que se indica arriba.

### Configuración

Copia `.env.example` a `.env` y rellena los valores:

```env
DISCORD_BOT_TOKEN=tu_token_de_discord
GROQ_API_KEY=tu_api_key_de_groq
```

Después:

1. En el portal de Discord, abre tu aplicación → **Bot** y activa **Server Members Intent** (obligatorio para las bienvenidas).
2. Invita el bot con los scopes `bot` y `applications.commands`.
3. Arranca el bot:

```bash
python main.py
```

4. En el servidor, ejecuta `/config` para asignar rol de staff, categoría de tickets y canal de logs.
5. Publica el panel con `/panel_tickets` en el canal deseado.
6. Configura las bienvenidas con `/config_welcome`.

> [!IMPORTANT]
> No subas `.env` al repositorio. Si el token se filtra, regeneralo en el portal: cualquiera con ese token controla el bot.

### Licencia

**MIT** — consulta [LICENSE](LICENSE).

---

## English

### Table of contents

- [Overview](#overview)
- [Ticket system](#ticket-system)
- [Commands](#commands)
- [Welcome system](#welcome-system)
- [Project structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [License](#license)

### Overview

**BotGuard** is a **Python** Discord bot aimed at programming and cybersecurity servers. It combines a button-driven **ticket** system with private channels, **moderation** commands, embed messages, automatic welcomes and an **AI** command backed by Groq.

The bot's interface is in Spanish.

### Ticket system

- Interactive panel created with `/panel_tickets`.
- Seven categories: programming support, cybersecurity, report a user, suggestions, staff applications, role requests and partnerships.
- Each ticket creates a **private channel** visible only to the user and staff.
- Closing requires confirmation from inside the ticket.
- **Automatic logs** for opening and closing.

### Commands

| Command | What it does |
|---|---|
| `/panel_tickets` | Publishes the button-based ticket panel |
| `/config` | Sets the staff role, ticket category and log channel |
| `/config_welcome` | Sets the welcome channel, auto role and enable flag |
| `/ban` | Bans a user |
| `/kick` | Kicks a user |
| `/timeout` | Temporarily mutes a user |
| `/untimeout` | Removes the mute |
| `/clear` | Deletes channel messages |
| `/embed` | Builds a custom embed message |
| `/ia` | Queries the configured Groq model |

Every moderation command checks permissions before acting.

### Welcome system

- Customisable embed welcome message.
- Automatic role assignment for new members.
- New-joiner logs in the moderation channel.
- Enabled and configured through `/config_welcome`.

### Project structure

```text
BotGuard_discord/
├── main.py            # Bot, tickets, moderation, welcomes and AI
├── requirements.txt
├── .env.example       # Required variables
├── LICENSE
└── README.md
```

### Requirements

- **Python 3.11** or later.
- A bot application in the [Discord Developer Portal](https://discord.com/developers/applications).
- A **Groq** key if you want to use `/ia`.
- **bot** and **applications.commands** scopes, plus **Manage Channels**, **Manage Roles**, **Kick Members**, **Ban Members** and **Moderate Members** depending on what you enable.

### Installation

```bash
git clone https://github.com/alberto2005-coder/BotGuard_discord.git
cd BotGuard_discord
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install discord.py python-dotenv openai
```

> [!NOTE]
> `requirements.txt` lists both `discord.py` and `py-cord`. Both installers expose the `discord` module, so they can overwrite each other: install only one. The code uses **discord.py**, which is the one shown above.

### Configuration

Copy `.env.example` to `.env` and fill in the values:

```env
DISCORD_BOT_TOKEN=your_discord_token
GROQ_API_KEY=your_groq_key
```

Then:

1. In the Discord portal, open your application → **Bot** and enable **Server Members Intent** (required for welcomes).
2. Invite the bot with the `bot` and `applications.commands` scopes.
3. Start the bot:

```bash
python main.py
```

4. On the server, run `/config` to set the staff role, ticket category and log channel.
5. Publish the panel with `/panel_tickets` in the desired channel.
6. Configure welcomes with `/config_welcome`.

> [!IMPORTANT]
> Never commit `.env`. If the token leaks, regenerate it in the portal: anyone holding it controls the bot.

### License

**MIT** — see [LICENSE](LICENSE).
