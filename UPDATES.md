"# 🆕 Updates in Version 2.1

## Neue Features

### 💾 Persistenz-System
- **Automatisches Speichern**: Bot-State wird automatisch in `data/bot_state.json` gespeichert
- **Überlebt Neustarts**: Active Targets und Style-Beispiele bleiben erhalten
- **Kein Datenverlust**: Bei Bot-Neustart werden alle Einstellungen wiederhergestellt

**Verwendung:**
- Automatisch! Kein Setup nötig
- Bei `/add` oder `/remove` wird State gespeichert
- Bei Bot-Shutdown wird finaler State gespeichert

### 📝 Logging-System
- **Strukturierte Logs**: Zeitstempel, Logger-Name, Level, Nachricht
- **Log-Rotation**: Automatisch bei 10MB, hält 5 Backup-Dateien
- **Mehrere Level**: DEBUG, INFO, WARNING, ERROR
- **Dateien**: `logs/bot.log`

**Log-Level einstellen:**
```env
LOG_LEVEL=INFO  # In .env Datei
```

**Logs ansehen:**
```bash
# Live verfolgen
tail -f logs/bot.log

# Nur Fehler
grep ERROR logs/bot.log
```

### 🔧 Konfigurierbare Timing-Parameter
- **Externe Konfiguration**: `config/timing.json`
- **Anpassbar**: Alle Timing-Parameter ohne Code-Änderung
- **Hot-Reload**: Änderungen werden beim nächsten Bot-Start übernommen

**config/timing.json:**
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

### 🔄 Verbessertes Error Handling
- **Retry-Logik**: Automatische Wiederholungen bei temporären Fehlern
- **Spezifische Exceptions**: Unterscheidet zwischen Rate-Limits, Timeouts, etc.
- **Exponential Backoff**: Intelligente Wartezeiten zwischen Retries
- **Bessere Fehlermeldungen**: Detaillierte Logs für Debugging

**Behandelte Fehlertypen:**
- `RateLimitError`: Wartet und versucht erneut
- `Timeout`: Retry mit kürzerer Wartezeit
- `ServiceUnavailableError`: Längere Wartezeit vor Retry
- `APIError`: Logged und gibt Fallback-Antwort

### ✅ Environment Validation
- **Vollständige Prüfung**: Alle erforderlichen Variablen werden validiert
- **Hilfreiche Fehler**: Zeigt genau, was fehlt
- **Start-Sicherheit**: Bot startet nur mit vollständiger Konfiguration

## Verbesserte Projektstruktur

```
spambot-chatbot/
├── src/
│   ├── __init__.py
│   ├── main.py              # ✨ Mit Logging & Validation
│   ├── telegram_bot.py      # ✨ Mit Storage & Timing Manager
│   ├── llm_handler.py       # ✨ Mit Retry-Logik
│   ├── personality.py       # ✨ Mit Logging
│   ├── storage.py           # 🆕 NEU: Persistenz
│   ├── timing_manager.py    # 🆕 NEU: Timing-Config
│   └── logger.py            # 🆕 NEU: Logging-Setup
├── config/
│   ├── personality.json
│   └── timing.json          # 🆕 NEU: Timing-Config
├── data/                    # 🆕 NEU: Gespeicherter State
│   └── bot_state.json       # (automatisch erstellt)
├── logs/                    # 🆕 NEU: Log-Dateien
│   └── bot.log              # (automatisch erstellt)
└── ...
```

## Migration von v2.0

**Keine Änderungen nötig!** Die neuen Features funktionieren automatisch:

1. **Persistenz**: Wird automatisch aktiviert beim ersten `/add`
2. **Logging**: Funktioniert sofort, Logs in `logs/bot.log`
3. **Timing**: Default-Config wird erstellt wenn nicht vorhanden

**Optional:**
- `.env`: Füge `LOG_LEVEL=INFO` hinzu (optional)
- `config/timing.json`: Passe Timing an (optional)

## Neue .env Optionen

```env
# Erforderlich (wie vorher)
TELEGRAM_BOT_TOKEN=your_token
ADMIN_USER_ID=your_id
OPENAI_API_KEY=your_key

# Optional (neu)
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR
LITELLM_MODEL=gpt-3.5-turbo # Explizites Model
```

## Verbesserungen im Detail

### Storage (src/storage.py)
- Speichert Active Targets
- Speichert Style-Beispiele
- JSON-Format (menschenlesbar)
- Automatisches Backup

### Timing Manager (src/timing_manager.py)
- Lädt Config aus JSON
- Erstellt Default-Config bei Bedarf
- Getter für alle Parameter
- Update-Funktion (zukünftig via Bot-Befehl)

### Logger (src/logger.py)
- Rotating File Handler
- Console + File Output
- Anpassbare Formate
- Library-Log-Unterdrückung

### LLM Handler Verbesserungen
- Retry mit Exponential Backoff
- Spezifische Exception-Behandlung
- Bessere Error-Messages
- Detailliertes Logging

## Was bleibt gleich?

- ✅ Alle Bot-Befehle funktionieren wie vorher
- ✅ Warm Start funktioniert wie vorher
- ✅ Personality-System unverändert
- ✅ Natürliches Timing wie vorher
- ✅ Keine Breaking Changes

## Nächste Schritte

### Nach dem Update:
1. Bot starten: `python run.py`
2. Prüfen: Logs in `logs/bot.log`
3. Testen: `/add`, `/remove`, `/warmstart`
4. State prüfen: `cat data/bot_state.json`

### Optional:
- Timing anpassen in `config/timing.json`
- Log-Level ändern in `.env`
- Alte Logs rotieren/löschen

## Bekannte Limitationen

- Konversations-Historie wird nicht persistiert (nur im RAM)
- Style-Beispiele limitiert auf 10 pro Chat
- Logs rotieren bei 10MB (konfigurierbar)

## Support

Bei Problemen:
1. Logs prüfen: `tail -f logs/bot.log`
2. State prüfen: `cat data/bot_state.json`
3. Config prüfen: `cat config/timing.json`
4. GitHub Issues erstellen mit Logs

---

**Version**: 2.1  
**Datum**: 2024  
**Kompatibilität**: Python 3.8+"