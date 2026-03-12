# ⚡ Schnellstart-Anleitung

Diese Anleitung bringt deinen Spambot-Chatbot in **unter 10 Minuten** zum Laufen!

## 📋 Checkliste

- [ ] Python 3.8+ installiert
- [ ] Telegram Account
- [ ] OpenAI API Key (oder anderer LLM-Provider)

## 🚀 In 5 Schritten zum laufenden Bot

### 1️⃣ Bot bei Telegram erstellen (2 Minuten)

1. Öffne [@BotFather](https://t.me/botfather) in Telegram
2. Sende: `/newbot`
3. Wähle einen Namen (z.B. "My Assistant Bot")
4. Wähle einen Username (z.B. "my_assistant_bot")
5. **Kopiere den Bot Token** (sieht aus wie: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2️⃣ Deine User ID herausfinden (1 Minute)

1. Öffne [@userinfobot](https://t.me/userinfobot)
2. Sende: `/start`
3. **Kopiere deine ID** (eine Zahl wie: `123456789`)

### 3️⃣ Projekt einrichten (2 Minuten)

```bash
# Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# oder: venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements.txt

# .env erstellen und bearbeiten
cp .env.example .env
nano .env  # oder mit einem anderen Editor
```

**In der `.env` Datei ausfüllen:**
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_USER_ID=123456789
OPENAI_API_KEY=sk-...
LITELLM_MODEL=gpt-3.5-turbo
```

### 4️⃣ Bot starten (1 Minute)

```bash
python run.py
```

Du solltest sehen:
```
🚀 Bot startet als 'Lisa'...
Admin User ID: 123456789
Persönlichkeit geladen: Lisa
```

### 5️⃣ Bot testen (2 Minuten)

1. Öffne deinen Bot in Telegram (suche nach dem Username)
2. Sende: `/start`
3. Der Bot sollte antworten!

## 🎯 Ersten Spammer hinzufügen

### Chat-ID herausfinden

Wenn dich jemand anschreibt:

**Option A: Mit @userinfobot**
1. Leite eine Nachricht des Spammers an [@userinfobot](https://t.me/userinfobot) weiter
2. Der Bot zeigt dir die Chat-ID

**Option B: Über Telegram Desktop**
1. Rechtsklick auf den Chat → "Link kopieren"
2. Die Zahl im Link ist die Chat-ID

### Bot aktivieren

```
/add 987654321
```
(Ersetze `987654321` mit der echten Chat-ID)

✅ **Fertig!** Der Bot antwortet jetzt automatisch!

## 🔄 Mit Warm Start (empfohlen)

Für beste Ergebnisse:

```
# 1. Warm Start aktivieren
/warmstart 987654321

# 2. Leite 5-10 DEINER Nachrichten an den Bot weiter
# (aus dem Chat mit dem Spammer)

# 3. Analyse starten
/warmstart 987654321

# 4. Bot aktivieren
/add 987654321
```

Jetzt imitiert der Bot perfekt deinen Schreibstil! 🎭

## 📱 Wichtige Befehle

| Befehl | Beschreibung |
|--------|-------------|
| `/start` | Bot begrüßt dich |
| `/add <id>` | Fügt Spammer hinzu |
| `/remove <id>` | Entfernt Spammer |
| `/list` | Zeigt aktive Chats |
| `/warmstart <id>` | Stil lernen/analysieren |
| `/reset <id>` | Konversation zurücksetzen |
| `/status` | Bot-Info anzeigen |
| `/help` | Hilfe anzeigen |

## ⚠️ Troubleshooting

### Bot startet nicht

**Fehler: "TELEGRAM_BOT_TOKEN nicht gefunden"**
```bash
# Prüfe .env Datei
cat .env

# Stelle sicher, dass keine Leerzeichen um = sind
# Richtig: TELEGRAM_BOT_TOKEN=123...
# Falsch:  TELEGRAM_BOT_TOKEN = 123...
```

**Fehler: "Module not found"**
```bash
# Virtual Environment aktiviert?
source venv/bin/activate

# Dependencies neu installieren
pip install -r requirements.txt
```

### Bot antwortet nicht

1. **Läuft der Bot?** → Terminal prüfen
2. **Chat-ID hinzugefügt?** → `/list` prüfen
3. **Richtige Chat-ID?** → Nochmal mit @userinfobot prüfen

### LLM-Fehler

**"Unauthorized" oder "Invalid API Key"**
```bash
# Prüfe OpenAI API Key
echo $OPENAI_API_KEY

# Prüfe Guthaben auf OpenAI Dashboard
# https://platform.openai.com/account/usage
```

**"Rate Limit" Fehler**
- Zu viele Anfragen → Warte kurz
- Oder upgrade OpenAI Plan

## 🎉 Nächste Schritte

1. **Persönlichkeit anpassen**
   - Bearbeite `config/personality.json`
   - Ändere Name, Alter, Interessen, etc.

2. **Timing anpassen**
   - Öffne `src/telegram_bot.py`
   - Zeile ~20-25: Timing-Parameter

3. **Anderen LLM nutzen**
   - Siehe `README.md` → "Andere LLM-Provider"
   - z.B. Claude, Llama, etc.

4. **Dokumentation lesen**
   - `README.md` - Vollständige Anleitung
   - `FEATURES.md` - Technische Details
   - `CHANGELOG.md` - Neue Features

## 💡 Pro-Tipps

✅ **DO:**
- Warm Start IMMER nutzen für beste Ergebnisse
- Persönlichkeit an dich anpassen
- Gelegentlich Konversation checken
- Bei Problemen `/reset` nutzen

❌ **DON'T:**
- Bot Token öffentlich teilen
- Zu viele Chats gleichzeitig (API Limits!)
- Bot für illegale Aktivitäten nutzen
- .env Datei committen (ist in .gitignore)

## 🆘 Hilfe benötigt?

1. **README.md lesen** - Ausführliche Dokumentation
2. **FEATURES.md lesen** - Technische Details
3. **Logs prüfen** - Terminal-Output ansehen
4. **Issue erstellen** - Bei Bugs/Problemen

---

**Viel Erfolg beim Spammer-Trollen! 🎭**