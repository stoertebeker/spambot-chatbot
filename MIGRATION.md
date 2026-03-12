# Migration von Bot zu Userbot

## Was hat sich geändert?

### Von Telegram Bot → Telegram Userbot

**Vorher (Bot):**
- Läuft als separater Bot-Account
- Benötigt Bot-Token von @BotFather
- Spammer müssen den Bot anschreiben
- Bot antwortet nur in eigenen Chats

**Jetzt (Userbot):**
- Läuft mit DEINEM Telegram-Account
- Benötigt API ID/Hash von my.telegram.org
- Bot sieht ALLE deine Chats
- Antwortet automatisch in deinem Namen
- Spammer merken NICHTS!

## Wichtigste Unterschiede

### 1. Authentication

**Alt:**
```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
ADMIN_USER_ID=123456789
```

**Neu:**
```env
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=0123456789abcdef...
```

### 2. Login-Prozess

**Alt:**
- Token aus .env → fertig

**Neu:**
- Telefonnummer eingeben
- Login-Code aus Telegram eingeben
- 2FA Passwort (falls aktiviert)
- Session wird gespeichert

### 3. Commands

**Alt (an Bot senden):**
```
/add 123456789
/list
/remove 123456789
```

**Neu (an "Saved Messages" senden):**
```
/whitelist_add 123456789
/whitelist_list
/whitelist_remove 123456789
/import 123456789
/pause
/resume
```

### 4. Workflow

**Alt:**
1. Spammer schreibt DICH an
2. Du leitest Nachrichten an BOT weiter
3. Du sagst Spammer: "Schreib mal @meinbot"
4. Spammer chattet mit Bot
5. Bot antwortet als separate Entität

**Neu:**
1. Spammer schreibt DICH an
2. Du sendest `/import <user_id>` (in Saved Messages)
3. Du sendest `/whitelist_add <user_id>`
4. Bot übernimmt - Spammer merkt NICHTS!
5. Alles läuft in DEINEM Chat

## Risiken (NEU!)

⚠️ **WICHTIG:**

- Userbot verstößt gegen Telegram ToS
- Risiko eines Account-Bans
- Telegram kann Account permanent sperren
- **Empfehlung: Zweit-Account verwenden!**

**Das gab es beim Bot nicht!** Bot war TOS-konform.

## Vorteile des Userbots

✅ Spammer merkt NICHTS (antwortet in deinem Namen)
✅ Kein separater Bot-Account nötig
✅ Chat-Import: Lernt automatisch deinen Stil
✅ Nahtlose Integration in deine Chats
✅ Realistischer (nutzt deinen Account)

## Code-Änderungen

### Gelöscht
- `src/telegram_bot.py` - Alter Bot-Code
- `run.py` - Alter Entry Point
- Alle MD-Dateien außer README

### Neu
- `src/userbot.py` - Neuer Userbot (Telethon)
- `src/main.py` - Überarbeitet für Userbot
- `src/storage.py` - Session-Support
- `README.md` - Komplett neu
- `SETUP.md` - Setup-Anleitung

### Behalten (mit Anpassungen)
- `src/llm_handler.py` - Fast unverändert
- `src/timing_manager.py` - Unverändert
- `src/logger.py` - Unverändert
- `src/personality.py` - Unverändert
- `config/` - Unverändert

### Dependencies

**Entfernt:**
```txt
python-telegram-bot==21.0.1
aiofiles==23.2.1
```

**Hinzugefügt:**
```txt
telethon==1.34.0
cryptg==0.4.0
```

## Migration-Schritte

Wenn du vom alten Bot-System kommst:

1. **Backup erstellen**
   ```bash
   cp -r data/ data_backup/
   cp .env .env.backup
   ```

2. **Dependencies updaten**
   ```bash
   pip install -r requirements.txt
   ```

3. **.env anpassen**
   - Entferne `TELEGRAM_BOT_TOKEN`
   - Entferne `ADMIN_USER_ID`
   - Füge `TELEGRAM_API_ID` hinzu
   - Füge `TELEGRAM_API_HASH` hinzu

4. **Alte Daten migrieren** (optional)
   
   Die `data/bot_state.json` ist kompatibel:
   - `active_targets` → wird zu `whitelist`
   - `style_examples` → bleibt gleich
   - Einfach lassen, wird automatisch geladen!

5. **Userbot starten**
   ```bash
   python -m src.main
   ```

6. **Testen mit Zweit-Account!**

## FAQ

**Q: Kann ich den alten Bot weiter nutzen?**
A: Ja, mit dem alten Code (Git-Tag/Commit). Aber empfohlen ist der Userbot.

**Q: Muss ich alles neu konfigurieren?**
A: Nein, `config/` und teilweise `data/` bleiben kompatibel.

**Q: Kann ich zwischen Bot und Userbot wechseln?**
A: Ja, mit Git-Branches. Aber verschiedene `.env` Files nötig.

**Q: Sind meine alten Chat-Daten verloren?**
A: Nein, `data/bot_state.json` ist kompatibel. Style-Examples bleiben erhalten.

**Q: Muss ich die Spammer neu hinzufügen?**
A: Wenn du `data/bot_state.json` behältst: Nein. Ansonsten: Ja, mit `/whitelist_add`.

**Q: Funktioniert der Userbot auf meinem Server?**
A: Ja, aber du musst einmalig interaktiv einloggen (Telefonnummer + Code).

## Support

Bei Problemen:

1. Schaue in `logs/bot.log`
2. Lies `SETUP.md`
3. Prüfe `.env` Konfiguration
4. Teste mit Zweit-Account

## Zusammenfassung

**Nutze den Userbot wenn:**
- ✅ Du willst, dass Spammer NICHTS merken
- ✅ Du in deinem Namen antworten willst
- ✅ Du Chat-Import nutzen willst
- ✅ Du das Risiko eines Bans akzeptierst
- ✅ Du einen Zweit-Account zum Testen hast

**Nutze den alten Bot wenn:**
- ❌ Du TOS-konform bleiben willst
- ❌ Du kein Ban-Risiko eingehen willst
- ❌ Du einen separaten Bot-Account bevorzugst
- ❌ Dir egal ist, dass Spammer merken, dass es ein Bot ist

**Empfehlung:** Userbot mit Zweit-Account! 🚀