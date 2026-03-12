# Changelog

## Version 2.0 - "Natürlich & Unauffällig" (Aktuell)

### 🎉 Neue Features

#### ⏱️ Natürliches Timing-System
- **Leseverzögerung**: 1-3 Sekunden vor dem Antworten
- **Typing-Indikator**: Zeigt "tippt..." während Bot schreibt
- **Realistische Tippgeschwindigkeit**: 3.5-6 Zeichen/Sekunde
- **Zufällige Variation**: ±30% für natürliches Verhalten
- **Gelegentliche Pausen**: 15% Chance auf 30s-3min Verzögerung
- **Intelligente Berechnung**: Basiert auf Nachrichtenlänge

#### 🔄 Warm Start - Stil-Lernsystem
- **Stil-Analyse**: LLM analysiert deine Schreibweise
- **Beispiel-Sammlung**: Speichert bis zu 10 deiner Nachrichten
- **Automatische Integration**: System-Prompt wird erweitert
- **Nahtlose Übernahme**: Bot imitiert deinen Stil perfekt
- Neue Befehle:
  - `/warmstart <chat_id>` - Aktiviert Lernmodus
  - Weiterleiten von Nachrichten zum Lernen
  - `/warmstart <chat_id>` erneut - Zeigt Analyse

#### 📊 Verbesserte Konversationsverwaltung
- **Stil-Speicherung**: Pro Chat-ID separate Stil-Beispiele
- **Kontext-Erhaltung**: Stil bleibt bei /reset erhalten
- **Erweiterte Logs**: Besseres Monitoring in Console

#### 🎭 Erweitertes Persönlichkeits-System
- **Zweistufig**: Basis-Persönlichkeit + individueller Stil
- **Dynamischer System-Prompt**: Passt sich an gelernten Stil an
- **Flexible Konfiguration**: JSON + Warm Start kombinierbar

### 🔧 Verbesserungen

- **Bessere Timing-Kontrolle**: Min/Max Delays konfigurierbar
- **Typing-Indikator-Loop**: Erneuert sich automatisch alle 5s
- **Fehlerbehandlung**: Robuster bei LLM/Telegram-Fehlern
- **Code-Struktur**: Modular und erweiterbar
- **Dokumentation**: README, FEATURES.md, CHANGELOG.md

### 📝 Neue Befehle

- `/warmstart <chat_id>` - Stil-Lernmodus aktivieren/analysieren
- `/timing` - Zeigt aktuelle Timing-Einstellungen

### 🐛 Bugfixes

- Import-Fehler in main.py behoben
- JSON-Escape-Zeichen in personality.json korrigiert

---

## Version 1.0 - "Initial Release"

### ✨ Initiale Features

- Telegram Bot Integration
- LiteLLM Backend-Support
- Persönlichkeits-System (JSON-basiert)
- Multi-Chat-Verwaltung
- Admin-Only Kontrolle
- Basis-Befehle:
  - `/start` - Bot starten
  - `/add <chat_id>` - Target hinzufügen
  - `/remove <chat_id>` - Target entfernen
  - `/list` - Targets anzeigen
  - `/reset <chat_id>` - Konversation zurücksetzen
  - `/status` - Bot-Status
  - `/help` - Hilfe anzeigen

### 📦 Projektstruktur

```
spambot-chatbot/
├── .env
├── .gitignore
├── requirements.txt
├── config/
│   └── personality.json
└── src/
    ├── main.py
    ├── telegram_bot.py
    ├── llm_handler.py
    └── personality.py
```

---

## Roadmap / Geplante Features

### Version 2.1 (Geplant)
- [ ] Persistente Speicherung (SQLite)
- [ ] Konfigurierbare Timing-Parameter via Befehle
- [ ] Statistiken pro Chat
- [ ] Besseres Error-Handling

### Version 3.0 (Zukunft)
- [ ] Web-Dashboard
- [ ] Mehrere Admins
- [ ] Bild-Support
- [ ] Voice-Message-Support
- [ ] Zeitbasierte Verfügbarkeit
- [ ] Auto-Stil-Anpassung während Chat
- [ ] Sentiment-Analyse

---

## Migration Guide

### Von v1.0 zu v2.0

1. **Aktualisiere Dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. **Keine Breaking Changes**: Alle v1.0 Befehle funktionieren weiterhin

3. **Neue Features nutzen**:
   - Verwende `/warmstart` für bessere Ergebnisse
   - Bot verhält sich automatisch natürlicher (Timing)

4. **Optionale Anpassungen**:
   - Timing-Parameter in `telegram_bot.py` anpassen
   - Persönlichkeit in `config/personality.json` verfeinern

---

## Credits

- **LiteLLM**: Universelles LLM-Interface
- **python-telegram-bot**: Telegram Bot Framework
- **OpenAI**: GPT-Modelle (oder andere LLM-Provider)