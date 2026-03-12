# Setup-Anleitung für Telegram Userbot

## Schritt 1: Telegram API Credentials erhalten

1. Gehe zu https://my.telegram.org
2. Logge dich mit deiner Telefonnummer ein
3. Klicke auf "API development tools"
4. Fülle das Formular aus:
   - **App title**: `Spam Responder`
   - **Short name**: `spambot`
   - **Platform**: `Other`
5. Notiere dir:
   - **App api_id** (Zahl, z.B. 12345678)
   - **App api_hash** (String, z.B. 0123456789abcdef0123456789abcdef)

## Schritt 2: LLM API Key besorgen

### Option A: OpenAI
1. Gehe zu https://platform.openai.com
2. Erstelle einen API Key
3. Notiere den Key

### Option B: Anthropic (Claude)
1. Gehe zu https://console.anthropic.com
2. Erstelle einen API Key
3. Notiere den Key

### Option C: Andere LLM Provider
Siehe https://docs.litellm.ai/docs/providers

## Schritt 3: Projekt Setup

```bash
# Repository klonen
git clone https://github.com/stoertebeker/spambot-chatbot.git
cd spambot-chatbot

# Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# Dependencies installieren
pip install -r requirements.txt
```

## Schritt 4: .env Datei erstellen

Erstelle eine `.env` Datei im Projekt-Root:

```env
# Telegram API (von my.telegram.org)
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=0123456789abcdef0123456789abcdef

# LLM Configuration - Option A: Eigener LLM Endpoint
LITELLM_MODEL=claude-haiku-4.5
LITELLM_API_BASE=https://your-llm-endpoint.com
LITELLM_API_KEY=your_api_key

# LLM Configuration - Option B: OpenAI direkt
# LITELLM_MODEL=gpt-3.5-turbo
# OPENAI_API_KEY=sk-...

# LLM Configuration - Option C: Anthropic direkt
# LITELLM_MODEL=claude-3-haiku-20240307
# ANTHROPIC_API_KEY=sk-ant-...

# Logging
LOG_LEVEL=INFO
```

## Schritt 5: Userbot starten

```bash
python -m src.main
```

### Beim ersten Start:

Der Bot fragt nach:

1. **Telefonnummer** (mit Ländercode)
   ```
   Please enter your phone number (with country code): +491234567890
   ```

2. **Login-Code** (wird dir per Telegram geschickt)
   ```
   Please enter the code you received: 12345
   ```

3. **2FA Passwort** (falls aktiviert)
   ```
   Please enter your 2FA password: dein_passwort
   ```

Die Session wird in `data/session.json` gespeichert.

## Schritt 6: Ersten Spammer hinzufügen

1. **Öffne "Saved Messages"** in Telegram (Chat mit dir selbst)

2. **Sende Hilfe-Command:**
   ```
   /help
   ```

3. **Finde User-ID des Spammers:**
   - Leite eine Nachricht von ihm an @userinfobot weiter
   - Notiere die User-ID (z.B. 123456789)

4. **Importiere Chat-Historie:**
   ```
   /import 123456789
   ```

5. **Aktiviere Whitelist:**
   ```
   /whitelist_add 123456789
   ```

6. **Fertig!** Der Bot antwortet jetzt automatisch.

## Wichtige Commands

Alle Commands in **Saved Messages** senden:

- `/help` - Zeige alle Commands
- `/status` - Zeige Bot-Status
- `/whitelist_list` - Zeige alle whitelisted User
- `/pause` - Pausiere Auto-Antworten
- `/resume` - Fortsetzen

## Troubleshooting

### "Invalid API ID or Hash"
- Prüfe `TELEGRAM_API_ID` und `TELEGRAM_API_HASH` in `.env`
- API_ID muss eine Zahl sein (ohne Anführungszeichen)
- API_HASH muss ein String sein (ohne Anführungszeichen)

### "Phone code invalid"
- Warte bis der Code per Telegram ankommt
- Code läuft nach wenigen Minuten ab - neu anfordern

### "Session file is corrupted"
```bash
rm data/session.json
python -m src.main
```

### LLM-Fehler
- Prüfe API Keys in `.env`
- Prüfe Model-Name in `.env`
- Schaue in `logs/bot.log` für Details

## Sicherheit

⚠️ **WICHTIG:**

- Nutze einen **Zweit-Account** zum Testen!
- Telegram kann deinen Account **bannen**
- Userbot verstößt gegen Telegram ToS
- `.env` und `data/session.json` NIEMALS teilen!
- Nicht zu viele User whitelisten

## Logs ansehen

```bash
# Live-Logs ansehen
tail -f logs/bot.log

# Letzte 50 Zeilen
tail -50 logs/bot.log

# Nach Fehlern suchen
grep ERROR logs/bot.log
```

## Userbot stoppen

```bash
# Drücke Ctrl+C im Terminal
# Oder sende in Saved Messages:
/pause
```

## Nächste Schritte

1. ✅ Persönlichkeit anpassen: `config/personality.json`
2. ✅ Timing anpassen: `config/timing.json`
3. ✅ Weitere LLM-Provider testen
4. ✅ Logs monitoren
5. ✅ Feedback sammeln und Bot verbessern

Viel Erfolg! 🚀