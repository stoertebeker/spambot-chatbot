"# Telegram Spam Responder Userbot 🤖

Ein Telegram **Userbot**, der automatisch **in deinem Namen** auf Spam-Nachrichten antwortet und die Spammer mit deinem persönlichen Schreibstil beschäftigt.

⚠️ **WICHTIG**: Dies ist ein Userbot, kein normaler Bot. Er läuft mit deinem Telegram-Account und kann gegen Telegrams Terms of Service verstoßen. Nutze auf eigene Gefahr!

## Features

- 🎭 Imitiert **deinen** Schreibstil perfekt
- 🧠 LLM-Backend via LiteLLM (OpenAI, Anthropic, lokale Models, etc.)
- 💬 Automatische Antworten auf whitelisted Spammer
- 📥 Chat-Import: Lädt History und lernt deinen Stil
- ⏱️ **Natürliches Timing** - Realistische Verzögerungen
- ⌨️ **Typing-Indikator** - Zeigt an, dass du tippst
- 🎲 **Zufällige Pausen** - Wirkt authentisch
- 🔒 **Whitelist-basiert** - Nur auf ausgewählte User antworten
- ⏸️ **Pause-Modus** - Schnell deaktivierbar

## Wie es funktioniert

Der Userbot läuft mit **deinem** Telegram-Account und:
1. Hört auf **alle** eingehenden Nachrichten
2. Antwortet nur auf **whitelisted** User
3. Nutzt LLM um Antworten zu generieren
4. Imitiert deinen Schreibstil (gelernt aus Chat-Historie)
5. Antwortet mit realistischem Timing (Typing-Indikator, Pausen, etc.)

## Voraussetzungen

- Python 3.8+
- **Telegram API ID und API Hash** von [my.telegram.org](https://my.telegram.org)
- LLM API Key (OpenAI, Anthropic, oder andere via LiteLLM)
- Telegram Account (wird vom Userbot verwendet)

## Installation

1. **Repository klonen**
   ```bash
   git clone https://github.com/stoertebeker/spambot-chatbot.git
   cd spambot-chatbot
   ```

2. **Virtual Environment erstellen**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # oder
   venv\\Scripts\\activate  # Windows
   ```

3. **Dependencies installieren**
   ```bash
   pip install -r requirements.txt
   ```

4. **.env Datei erstellen**
   
   Kopiere `.env.example` zu `.env` und fülle die Werte aus:
   ```bash
   cp .env.example .env
   ```
   
   Dann bearbeite `.env`:
   ```env
   # Telegram API Credentials (from https://my.telegram.org)
   TELEGRAM_API_ID=12345678
   TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
   
   # LLM Configuration - OpenAI-compatible endpoint
   LITELLM_MODEL=openai/claude-haiku-4.5
   OPENAI_API_KEY=your_api_key_here
   OPENAI_API_BASE=https://your-llm-endpoint.com/v1
   
   # Or use OpenAI directly:
   # LITELLM_MODEL=gpt-3.5-turbo
   # OPENAI_API_KEY=sk-your-openai-key-here
   
   # Logging
   LOG_LEVEL=INFO
   ```

## Telegram API Credentials erhalten

1. Gehe zu [my.telegram.org](https://my.telegram.org)
2. Logge dich mit deiner Telefonnummer ein
3. Klicke auf \"API development tools\"
4. Erstelle eine neue Application:
   - **App title**: z.B. \"Spam Responder\"
   - **Short name**: z.B. \"spambot\"
   - **Platform**: Other
5. Kopiere **App api_id** und **App api_hash** in deine `.env`

## Verwendung

### Erster Start

1. **Userbot starten**
   ```bash
   python -m src.main
   ```

2. **Beim ersten Start: Login**
   
   Der Userbot fragt nach:
   - Deiner **Telefonnummer** (mit Ländercode, z.B. +49123456789)
   - Dem **Login-Code** (wird dir per Telegram geschickt)
   - Optional: **2FA Passwort** falls aktiviert
   
   Die Session wird in `data/session.json` gespeichert. Beim nächsten Start ist kein Login mehr nötig.

3. **Userbot läuft!**
   
   Der Bot hört nun auf alle eingehenden Nachrichten und antwortet automatisch auf whitelisted User.

### Userbot steuern

**Alle Commands sendest du an \"Saved Messages\" (Chat mit dir selbst):**

#### 📥 Chat-Historie importieren (EMPFOHLEN!)

```
/import 123456789
```

Der Bot:
- Lädt die **letzten 100 Nachrichten** aus dem Chat
- Analysiert **deinen** Schreibstil
- Lernt den Gesprächskontext
- Zeigt dir eine Statistik

**Was wird gelernt:**
- ✍️ Satzlänge und Struktur
- 😊 Emoji-Verwendung
- 📝 Formalitätsgrad
- 💬 Typische Ausdrücke
- ✨ Deine Schreibgewohnheiten

#### ➕ User zur Whitelist hinzufügen

```
/whitelist_add 123456789
```

Ab jetzt antwortet der Bot **automatisch** auf alle Nachrichten von diesem User!

#### 📋 Alle Commands

- `/whitelist_list` - Zeige alle whitelisted User
- `/whitelist_remove <user_id>` - Entferne User
- `/import <user_id>` - Importiere Chat-Historie
- `/pause` - Pausiere alle Auto-Antworten
- `/resume` - Fortsetzen
- `/status` - Zeige Userbot-Status
- `/help` - Zeige Hilfe

### User-ID herausfinden

**Methode 1: Mit @userinfobot**
1. Leite eine Nachricht des Users an [@userinfobot](https://t.me/userinfobot) weiter
2. Der Bot zeigt dir die User-ID

**Methode 2: Mit /import**
- Wenn du schon mit dem User gechattet hast, kannst du einfach `/import <user_id>` probieren
- Der Bot sagt dir, ob die User-ID korrekt ist

## 🎯 Beispiel-Workflow

1. **Spammer schreibt dich an**
   ```
   Spammer: \"Hey, wie geht's? 😊\"
   ```

2. **Du chattest normal** (5-10 Nachrichten)
   ```
   Du: \"Gut, und dir?\"
   Spammer: \"Auch gut! Hast du Interesse an...\"
   Du: \"Kommt drauf an...\"
   ```

3. **Import starten** (in Saved Messages)
   ```
   /import 123456789
   ```
   Bot: \"✅ Import complete! 15 messages (8 yours, 7 theirs)\"

4. **Whitelist aktivieren**
   ```
   /whitelist_add 123456789
   ```

5. **Bot übernimmt!**
   ```
   Spammer: \"Also, bist du dabei?\"
   Bot (als du): \"Mhh weiß nicht... 🤔\"
   ```
   
   Der Spammer merkt **NICHTS**! 😎

## ⏱️ Natürliches Timing

Der Bot verhält sich wie ein echter Mensch:

- **Leseverzögerung**: 1-3 Sekunden vor dem Tippen
- **Typing-Indikator**: Zeigt \"tippt...\" während der Bot schreibt
- **Realistische Geschwindigkeit**: 3.5-6 Zeichen/Sekunde
- **Zufällige Variation**: Mal schneller, mal langsamer
- **Gelegentliche Pausen**: 15% Chance auf 30s-3min Pause

**Beispiel-Timings:**
- Kurze Nachricht (20 Zeichen): ~3-5 Sekunden
- Mittlere Nachricht (100 Zeichen): ~5-8 Sekunden
- Lange Nachricht (200 Zeichen): ~8-15 Sekunden
- Mit langer Pause: +30s bis 3min extra

→ Praktisch **nicht erkennbar** als Bot! 🎭

## 🎭 Persönlichkeit anpassen

Bearbeite `config/personality.json`:

```json
{
  \"name\": \"Max\",
  \"age\": 25,
  \"occupation\": \"Student\",
  \"interests\": [\"Gaming\", \"Musik\", \"Sport\"],
  \"personality_traits\": [\"entspannt\", \"humorvoll\"],
  \"background\": \"Student aus Berlin...\",
  \"conversation_style\": \"Locker, nutzt Umgangssprache...\",
  \"system_prompt\": \"Du bist Max, ein 25-jähriger Student...\"
}
```

## 🔧 Timing anpassen

Bearbeite `config/timing.json`:

```json
{
  \"min_delay\": 2.0,
  \"max_delay\": 8.0,
  \"chars_per_second_min\": 3.5,
  \"chars_per_second_max\": 6.0,
  \"long_pause_chance\": 0.15,
  \"long_pause_min\": 30,
  \"long_pause_max\": 180,
  \"reading_delay_min\": 1.0,
  \"reading_delay_max\": 3.0
}
```

## 🤖 Andere LLM-Provider nutzen

LiteLLM unterstützt viele Provider:

**Anthropic (Claude):**
```env
LITELLM_MODEL=claude-3-sonnet-20240229
ANTHROPIC_API_KEY=your_key
```

**Lokaler LLM (Ollama):**
```env
LITELLM_MODEL=ollama/llama2
```

**Azure OpenAI:**
```env
LITELLM_MODEL=azure/gpt-35-turbo
AZURE_API_KEY=your_key
AZURE_API_BASE=your_endpoint
```

Siehe [LiteLLM Docs](https://docs.litellm.ai/docs/providers) für alle Provider.

## ⚠️ Sicherheit & Risiken

### KRITISCH:

- ❌ Dies ist ein **Userbot** - läuft mit deinem Account!
- ❌ **Verstößt gegen Telegram ToS** - Risiko eines Account-Bans!
- ❌ Telegram kann deinen Account **permanent sperren**
- ⚠️ Nutze auf **eigene Gefahr**

### Empfehlungen:

- ✅ Nutze einen **Zweit-Account** zum Testen
- ✅ Nur **wenige** User whitelisten
- ✅ Natürliches Timing nutzen (ist eingebaut)
- ✅ Bei Rate-Limit-Warnung: `/pause` nutzen
- ✅ Nicht zu viele Nachrichten pro Tag

### Generelle Sicherheit:

- 🔒 Teile niemals `.env` oder API Keys
- 🔒 `.env` ist in `.gitignore`
- 🔒 `data/session.json` ist sensibel - nicht teilen!
- 🔒 Bot antwortet nur auf whitelisted User
- 🔒 Logs werden in `logs/` gespeichert

## 🐛 Troubleshooting

**Userbot antwortet nicht:**
- ✓ Prüfe ob Userbot läuft (`python -m src.main`)
- ✓ Prüfe ob User mit `/whitelist_add` hinzugefügt wurde
- ✓ Prüfe ob `/pause` aktiv ist (mit `/resume` fortsetzen)
- ✓ Schaue in die Logs (`logs/bot.log`)

**Login-Probleme:**
- ✓ Prüfe `TELEGRAM_API_ID` und `TELEGRAM_API_HASH` in `.env`
- ✓ Lösche `data/session.json` und starte neu
- ✓ Prüfe ob 2FA aktiviert ist (Passwort bereithalten)
- ✓ Telefonnummer mit Ländercode angeben (+49...)

**LLM-Fehler:**
- ✓ Prüfe LLM API Keys in `.env`
- ✓ Prüfe `LITELLM_MODEL` Konfiguration
- ✓ Prüfe Guthaben auf LLM-Account
- ✓ Schaue in Logs für Details

**Import funktioniert nicht:**
- ✓ Prüfe ob User-ID korrekt ist
- ✓ Stelle sicher, dass du mit dem User schon gechattet hast
- ✓ Prüfe Logs für Fehlerdetails

**Rate-Limit von Telegram:**
- ✓ Sende `/pause` in Saved Messages
- ✓ Warte 1-2 Stunden
- ✓ Sende `/resume` zum Fortsetzen
- ✓ Reduziere Anzahl whitelisted User

## 📁 Projektstruktur

```
spambot-chatbot/
├── src/
│   ├── userbot.py           # Haupt-Userbot (Telethon)
│   ├── llm_handler.py       # LLM Integration
│   ├── personality.py       # Persönlichkeits-Manager
│   ├── storage.py           # Persistenz (State, Session)
│   ├── timing_manager.py    # Timing-Konfiguration
│   ├── logger.py            # Logging Setup
│   └── main.py              # Entry Point
├── config/
│   ├── personality.json     # Persönlichkeits-Konfiguration
│   └── timing.json          # Timing-Konfiguration
├── data/
│   ├── bot_state.json       # Whitelist, Style Examples
│   └── session.json         # Telegram Session (sensibel!)
├── logs/
│   └── bot.log              # Log-Datei
├── .env                     # Environment Variables (sensibel!)
├── .gitignore
├── requirements.txt
└── README.md
```

## 📊 Logging

Der Bot loggt alle wichtigen Events:

**In Console und `logs/bot.log`:**
- 📨 Eingehende Nachrichten (User-ID, Username, Text)
- 📤 Ausgehende Nachrichten (Antworten)
- 🧠 LLM-Requests und Responses
- ➕ Whitelist-Änderungen
- ⏱️ Timing-Details (Delays, Typing-Dauer)
- ⚠️ Fehler und Warnungen

**Log-Level in `.env` ändern:**
```env
LOG_LEVEL=DEBUG  # Sehr detailliert
LOG_LEVEL=INFO   # Normal (empfohlen)
LOG_LEVEL=WARNING  # Nur Warnungen
```

## 🚀 Nächste Schritte

Nach der Installation:

1. ✅ `.env` konfigurieren
2. ✅ `python -m src.main` starten
3. ✅ Mit Telegram-Account einloggen
4. ✅ `/help` in Saved Messages senden
5. ✅ Ersten Chat mit `/import` importieren
6. ✅ Mit `/whitelist_add` aktivieren
7. ✅ Zusehen wie der Bot arbeitet! 😎

## 📝 Lizenz

MIT License

## ⚠️ Disclaimer

Dieses Tool dient nur zu Bildungs- und Unterhaltungszwecken. 

- Nutze es **verantwortungsvoll**
- Verstößt gegen **Telegram ToS**
- Autor übernimmt **keine Haftung** für Bans oder Schäden
- Nutze auf **eigene Gefahr**
- Empfehlung: **Zweit-Account** verwenden

**Du wurdest gewarnt!** ⚠️
"