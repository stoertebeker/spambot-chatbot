"# Spambot-Chatbot 🤖

Ein Telegram-Bot, der automatisch auf Spam-Nachrichten antwortet und die Spammer mit einer vordefinierten Persönlichkeit beschäftigt.

## Features

- 🎭 Vordefinierte Persönlichkeit in JSON-Datei konfigurierbar
- 🧠 LLM-Backend via LiteLLM (unterstützt OpenAI, Anthropic, Cohere, etc.)
- 💬 Automatische Konversationsführung mit Spammern
- 🎯 Gezielte Aktivierung für bestimmte Chat-IDs
- 📊 Verwaltung mehrerer Spam-Chats gleichzeitig
- 🔒 Admin-Only Kontrolle
- ⏱️ **Natürliches Timing** - Realistische Antwortverzögerungen
- ⌨️ **\"Typing...\" Indikator** - Zeigt an, dass jemand tippt
- 🎲 **Zufällige Pausen** - Gelegentlich längere Pausen (wirkt beschäftigt)
- 🔄 **Warm Start** - Lernt deinen Schreibstil aus bisherigen Nachrichten

## Voraussetzungen

- Python 3.8+
- Telegram Bot Token (von [@BotFather](https://t.me/botfather))
- OpenAI API Key (oder andere LLM-Provider)
- Deine Telegram User ID

## Installation

1. **Repository klonen oder herunterladen**

2. **Virtual Environment erstellen**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Auf macOS/Linux
   ```

3. **Dependencies installieren**
   ```bash
   pip install -r requirements.txt
   ```

4. **.env Datei erstellen**
   ```bash
   cp .env.example .env
   ```
   
   Dann `.env` bearbeiten und ausfüllen:
   - `TELEGRAM_BOT_TOKEN`: Von @BotFather erhalten
   - `ADMIN_USER_ID`: Deine Telegram User ID (kannst du von @userinfobot erfahren)
   - `OPENAI_API_KEY`: Dein OpenAI API Key

5. **Persönlichkeit anpassen (optional)**
   
   Bearbeite `config/personality.json` um die Persona anzupassen.

## Telegram Bot erstellen

1. Öffne [@BotFather](https://t.me/botfather) in Telegram
2. Sende `/newbot`
3. Folge den Anweisungen und wähle einen Namen und Username
4. Kopiere den Bot Token in deine `.env` Datei

## Deine User ID herausfinden

1. Öffne [@userinfobot](https://t.me/userinfobot) in Telegram
2. Starte den Bot mit `/start`
3. Der Bot zeigt dir deine User ID
4. Kopiere die ID in deine `.env` Datei

## Verwendung

1. **Bot starten**
   ```bash
   python run.py
   ```

2. **Bot in Telegram öffnen**
   
   Suche nach deinem Bot-Username und sende `/start`

3. **Spammer hinzufügen**
   
   Wenn dich ein Spammer kontaktiert:
   - Finde die Chat-ID (z.B. durch Weiterleiten einer Nachricht an @userinfobot)
   - Sende an deinen Bot: `/add <chat_id>`
   
   Der Bot antwortet nun automatisch auf alle Nachrichten von dieser Chat-ID.

4. **Optional: Warm Start (empfohlen!)**
   
   Damit der Bot deinen Schreibstil imitiert:
   - `/warmstart <chat_id>` - Aktiviert Lernmodus
   - Leite dem Bot 5-10 DEINER Nachrichten aus dem Chat weiter
   - `/warmstart <chat_id>` nochmal - Zeigt Stil-Analyse
   - Dann `/add <chat_id>` - Bot übernimmt nahtlos

5. **Weitere Befehle**
   - `/list` - Zeigt alle aktiven Spam-Chats
   - `/remove <chat_id>` - Entfernt einen Chat von der Liste
   - `/reset <chat_id>` - Setzt die Konversation zurück
   - `/timing` - Zeigt Timing-Einstellungen
   - `/status` - Zeigt Bot-Status
   - `/help` - Zeigt Hilfe

## 🔄 Warm Start - So funktioniert's

Der **Warm Start** ermöglicht es dem Bot, deinen persönlichen Schreibstil zu lernen und macht ihn praktisch unerkennbar:

### Schritt-für-Schritt:

1. **Aktiviere Warm Start**
   ```
   /warmstart 123456789
   ```
   (Ersetze `123456789` mit der Chat-ID des Spammers)

2. **Nachrichten weiterleiten**
   - Öffne den Chat mit dem Spammer
   - Wähle 5-10 DEINER Nachrichten aus
   - Leite sie an deinen Bot weiter (Telegram Forward-Funktion)
   - Der Bot speichert sie als Stil-Beispiele

3. **Stil analysieren**
   ```
   /warmstart 123456789
   ```
   Der Bot analysiert deinen Stil und zeigt dir eine Zusammenfassung

4. **Bot aktivieren**
   ```
   /add 123456789
   ```
   Jetzt übernimmt der Bot mit deinem Schreibstil!

### Was wird gelernt?

- ✍️ Satzlänge und -struktur
- 😊 Emoji-Verwendung
- 📝 Formalitätsgrad
- 💬 Typische Ausdrücke und Redewendungen
- ✨ Besondere Schreibgewohnheiten

## ⏱️ Natürliches Timing

Der Bot verhält sich wie ein echter Mensch:

- **Leseverzögerung**: 1-3 Sekunden bevor er zu tippen beginnt
- **Typing-Indikator**: Zeigt \"tippt...\" während der Bot \"schreibt\"
- **Realistische Tippgeschwindigkeit**: 3.5-6 Zeichen pro Sekunde
- **Zufällige Variation**: Mal schneller, mal langsamer
- **Gelegentliche Pausen**: 15% Chance auf 30 Sekunden - 3 Minuten Pause (wirkt beschäftigt)

**Beispiel:**
- Kurze Nachricht (20 Zeichen): ~3-5 Sekunden Verzögerung
- Mittlere Nachricht (100 Zeichen): ~5-8 Sekunden Verzögerung
- Lange Nachricht (200 Zeichen): ~8-15 Sekunden Verzögerung
- Mit langer Pause: +30 Sekunden bis 3 Minuten extra

Dadurch ist praktisch **nicht erkennbar**, dass ein Bot antwortet!

## 🎭 Persönlichkeit anpassen

Bearbeite `config/personality.json`:

```json
{
  \"name\": \"Lisa\",
  \"age\": 28,
  \"occupation\": \"Marketing Managerin\",
  \"interests\": [\"Reisen\", \"Yoga\", \"Kochen\"],
  \"personality_traits\": [\"freundlich\", \"neugierig\"],
  \"background\": \"Dein Background Text...\",
  \"conversation_style\": \"Beschreibung des Gesprächsstils...\",
  \"system_prompt\": \"Der System-Prompt für das LLM...\"
}
```

## Andere LLM-Provider verwenden

LiteLLM unterstützt viele Provider. Beispiele:

**Anthropic (Claude):**
```env
LITELLM_MODEL=claude-3-sonnet-20240229
ANTHROPIC_API_KEY=your_key
```

**Local LLM (Ollama):**
```env
LITELLM_MODEL=ollama/llama2
```

**Azure OpenAI:**
```env
LITELLM_MODEL=azure/gpt-35-turbo
AZURE_API_KEY=your_key
AZURE_API_BASE=your_endpoint
```

Siehe [LiteLLM Dokumentation](https://docs.litellm.ai/docs/providers) für alle Provider.

## 🎯 Beispiel-Workflow

1. Spammer schreibt: \"Hey, wie geht's?\"
2. Du antwortest ein paar Mal normal
3. Du aktivierst `/warmstart 123456789`
4. Du leitest deine letzten 5-10 Nachrichten weiter
5. Bot analysiert: \"Kurze Sätze, viele Emojis 😊, lockerer Stil\"
6. Du aktivierst `/add 123456789`
7. Bot übernimmt nahtlos - Spammer merkt nichts!

## Sicherheitshinweise

⚠️ **Wichtig:**
- Teile niemals deinen `.env` File oder API Keys
- Die `.env` Datei ist in `.gitignore` und wird nicht committed
- Nur du (Admin) kannst den Bot steuern
- Der Bot antwortet NUR auf Chat-IDs, die du explizit hinzufügst

## Troubleshooting

**Bot antwortet nicht:**
- Prüfe ob der Bot läuft (`python run.py`)
- Prüfe ob die Chat-ID mit `/add` hinzugefügt wurde
- Prüfe die Logs in der Konsole

**LLM Fehler:**
- Prüfe ob `OPENAI_API_KEY` korrekt gesetzt ist
- Prüfe ob du Guthaben auf deinem OpenAI Account hast
- Prüfe die Logs für detaillierte Fehlermeldungen

**Telegram Fehler:**
- Prüfe ob `TELEGRAM_BOT_TOKEN` korrekt ist
- Prüfe ob `ADMIN_USER_ID` korrekt ist (Zahl ohne Anführungszeichen)

**Warm Start funktioniert nicht:**
- Stelle sicher, dass du DEINE Nachrichten weiterleitest, nicht die des Spammers
- Leite mindestens 5 Nachrichten weiter
- Verwende `/warmstart <chat_id>` zweimal (einmal aktivieren, einmal analysieren)

## Lizenz

MIT License - siehe LICENSE Datei

## Haftungsausschluss

Dieses Tool dient nur zu Bildungs- und Unterhaltungszwecken. Nutze es verantwortungsvoll."