# 📦 Installation Guide - Spambot-Chatbot v2.1

## Schnellstart (5 Minuten)

### 1. Repository herunterladen

```bash
# Via Git
git clone https://github.com/stoertebeker/spambot-chatbot.git
cd spambot-chatbot

# Oder: ZIP herunterladen und entpacken
```

### 2. Virtual Environment erstellen

```bash
python3 -m venv venv

# Aktivieren (macOS/Linux)
source venv/bin/activate

# Aktivieren (Windows)
venv\Scripts\activate
```

### 3. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 4. .env Datei erstellen

```bash
cp .env.example .env
```

Dann `.env` bearbeiten:

```env
# Erforderlich
TELEGRAM_BOT_TOKEN=your_bot_token_here
ADMIN_USER_ID=your_telegram_user_id
OPENAI_API_KEY=your_openai_api_key

# Optional
LOG_LEVEL=INFO
LITELLM_MODEL=gpt-3.5-turbo
```

**Wo bekomme ich die Werte her?**

- **TELEGRAM_BOT_TOKEN**: [@BotFather](https://t.me/botfather) → `/newbot`
- **ADMIN_USER_ID**: [@userinfobot](https://t.me/userinfobot) → `/start`
- **OPENAI_API_KEY**: [OpenAI Platform](https://platform.openai.com/api-keys)

### 5. Setup validieren

```bash
python test_setup.py
```

Sollte ausgeben: `✅ ALL CHECKS PASSED!`

### 6. Bot starten

```bash
python run.py
```

✅ **Fertig!** Der Bot läuft jetzt.

---

## Detaillierte Installation

### Systemanforderungen

- **Python**: 3.8 oder höher
- **Betriebssystem**: macOS, Linux, Windows
- **RAM**: Mindestens 256 MB frei
- **Festplatte**: ~50 MB für Code + Dependencies

### Schritt-für-Schritt

#### 1. Python prüfen

```bash
python3 --version
# Sollte zeigen: Python 3.8.x oder höher
```

Falls Python fehlt:
- **macOS**: `brew install python3`
- **Ubuntu/Debian**: `sudo apt install python3 python3-pip`
- **Windows**: [python.org](https://python.org) → Download

#### 2. Virtual Environment (empfohlen)

Warum? Isoliert Dependencies vom System.

```bash
# Erstellen
python3 -m venv venv

# Aktivieren
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Deaktivieren (später)
deactivate
```

#### 3. Dependencies installieren

```bash
pip install -r requirements.txt
```

**Was wird installiert?**
- `python-telegram-bot` - Telegram Bot API
- `litellm` - Universal LLM Interface
- `python-dotenv` - Environment Variables
- `aiofiles` - Async File I/O

#### 4. Konfiguration

##### .env Datei

```bash
cp .env.example .env
nano .env  # oder vim, code, etc.
```

Vollständiges Beispiel:

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_USER_ID=987654321

# LLM Provider
OPENAI_API_KEY=sk-...
LITELLM_MODEL=gpt-3.5-turbo

# Optional: Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR

# Optional: Andere LLM Provider
# ANTHROPIC_API_KEY=...
# COHERE_API_KEY=...
```

##### Personality anpassen

```bash
nano config/personality.json
```

Beispiel:

```json
{
  "name": "Sarah",
  "age": 25,
  "occupation": "Studentin",
  "interests": ["Musik", "Sport"],
  "system_prompt": "Du bist Sarah, eine 25-jährige Studentin..."
}
```

##### Timing anpassen (optional)

```bash
nano config/timing.json
```

Default-Werte werden automatisch erstellt.

#### 5. Telegram Bot erstellen

1. Öffne [@BotFather](https://t.me/botfather)
2. Sende: `/newbot`
3. Folge Anweisungen:
   - Name: z.B. "My Spambot Handler"
   - Username: z.B. "my_spambot_bot" (muss auf "bot" enden)
4. Kopiere Token → `.env` als `TELEGRAM_BOT_TOKEN`

#### 6. User ID herausfinden

1. Öffne [@userinfobot](https://t.me/userinfobot)
2. Sende: `/start`
3. Bot zeigt deine ID
4. Kopiere ID → `.env` als `ADMIN_USER_ID`

#### 7. OpenAI API Key

1. Gehe zu [platform.openai.com](https://platform.openai.com)
2. Registriere/Login
3. Navigiere zu "API Keys"
4. Erstelle neuen Key
5. Kopiere Key → `.env` als `OPENAI_API_KEY`

**Alternative LLM Provider:**

```env
# Anthropic Claude
LITELLM_MODEL=claude-3-sonnet-20240229
ANTHROPIC_API_KEY=...

# Local Ollama
LITELLM_MODEL=ollama/llama2
# Kein API Key nötig

# Azure OpenAI
LITELLM_MODEL=azure/gpt-35-turbo
AZURE_API_KEY=...
AZURE_API_BASE=...
```

#### 8. Setup validieren

```bash
python test_setup.py
```

**Erwartete Ausgabe:**

```
🔍 Spambot-Chatbot Setup Validation
============================================================

📁 Files:
✅ .env (required)
✅ config/personality.json (required)
⚠️  config/timing.json (optional)
✅ src/storage.py (required)
...

✅ ALL CHECKS PASSED!

🚀 You can start the bot with: python run.py
============================================================
```

#### 9. Bot starten

```bash
python run.py
```

**Erwartete Ausgabe:**

```
============================================================
Logging system initialized
Log level: INFO
Log file: logs/bot.log
============================================================
============================================================
🤖 SPAMBOT-CHATBOT v2.1
============================================================
🚀 Bot startet als 'Lisa'...
Admin User ID: 123456789
Aktive Targets: 0
```

---

## Troubleshooting

### Python nicht gefunden

**Problem:** `python3: command not found`

**Lösung:**
- macOS: `brew install python3`
- Ubuntu: `sudo apt install python3`
- Windows: Python von python.org installieren

### Import Fehler

**Problem:** `ModuleNotFoundError: No module named 'telegram'`

**Lösung:**
```bash
# Virtual Environment aktiviert?
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt
```

### Bot startet nicht

**Problem:** `ValueError: TELEGRAM_BOT_TOKEN nicht gefunden!`

**Lösung:**
1. `.env` Datei existiert?
2. Korrekte Werte in `.env`?
3. Keine Anführungszeichen um Werte!

```env
# Falsch:
TELEGRAM_BOT_TOKEN="123:ABC"

# Richtig:
TELEGRAM_BOT_TOKEN=123:ABC
```

### LLM Fehler

**Problem:** `APIError: Invalid API Key`

**Lösung:**
1. OpenAI API Key korrekt?
2. Guthaben auf OpenAI Account?
3. Logs prüfen: `tail -f logs/bot.log`

### Permission Fehler

**Problem:** `PermissionError: [Errno 13] Permission denied`

**Lösung:**
```bash
# macOS/Linux: Schreibrechte prüfen
ls -la data/ logs/

# Falls nötig:
chmod 755 data/ logs/
```

---

## Erweiterte Konfiguration

### Logging-Level anpassen

```env
# .env
LOG_LEVEL=DEBUG  # Sehr detailliert für Debugging
LOG_LEVEL=INFO   # Standard (empfohlen)
LOG_LEVEL=WARNING  # Nur Warnungen
LOG_LEVEL=ERROR  # Nur Fehler
```

### Timing anpassen

```json
// config/timing.json
{
  "min_delay": 1.0,        // Schnellere Antworten
  "max_delay": 5.0,        // Kürzere max. Verzögerung
  "chars_per_second_min": 5.0,  // Schnelleres Tippen
  "chars_per_second_max": 8.0,
  "long_pause_chance": 0.05,    // Seltener lange Pausen
  "long_pause_min": 15,
  "long_pause_max": 60
}
```

### Als Systemdienst (Linux)

```bash
# systemd service erstellen
sudo nano /etc/systemd/system/spambot.service
```

```ini
[Unit]
Description=Spambot Chatbot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/spambot-chatbot
Environment="PATH=/path/to/spambot-chatbot/venv/bin"
ExecStart=/path/to/spambot-chatbot/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Service aktivieren
sudo systemctl enable spambot
sudo systemctl start spambot

# Status prüfen
sudo systemctl status spambot

# Logs ansehen
sudo journalctl -u spambot -f
```

---

## Deinstallation

```bash
# Bot stoppen (falls als Service)
sudo systemctl stop spambot
sudo systemctl disable spambot

# Virtual Environment deaktivieren
deactivate

# Verzeichnis löschen
cd ..
rm -rf spambot-chatbot/
```

---

## Support

Bei Problemen:

1. **Logs prüfen**: `tail -f logs/bot.log`
2. **Setup validieren**: `python test_setup.py`
3. **Dokumentation lesen**: README.md, FEATURES.md
4. **GitHub Issues**: [Issues erstellen](https://github.com/stoertebeker/spambot-chatbot/issues)

---

**Version**: 2.1  
**Letztes Update**: 2024  
**Kompatibilität**: Python 3.8+