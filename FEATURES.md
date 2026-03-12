# 🚀 Erweiterte Features - Spambot-Chatbot

## Übersicht der Verbesserungen

Diese Version des Spambot-Chatbots wurde speziell entwickelt, um **maximal unauffällig** zu sein. Der Spammer soll nicht merken, dass ein Bot übernommen hat.

## 1. ⏱️ Natürliches Timing-System

### Komponenten:

#### a) Leseverzögerung
- **1-3 Sekunden** zufällige Verzögerung, bevor der Bot zu "tippen" beginnt
- Simuliert die Zeit, die ein Mensch braucht, um eine Nachricht zu lesen

#### b) Typing-Indikator
- Zeigt "tippt..." in Telegram während der Bot die Antwort "schreibt"
- Wird alle 5 Sekunden erneuert (Telegram-Limitation)
- Läuft für die gesamte berechnete Tippzeit

#### c) Realistische Tippgeschwindigkeit
- **3.5-6 Zeichen pro Sekunde** (zufällig bei Bot-Start gewählt)
- Entspricht durchschnittlicher menschlicher Tippgeschwindigkeit
- Variation: ±30% pro Nachricht für Natürlichkeit

#### d) Min/Max Delays
- **Minimum**: 2 Sekunden (selbst bei sehr kurzen Nachrichten)
- **Maximum**: 8 Sekunden (verhindert zu lange Wartezeiten)

#### e) Gelegentliche lange Pausen
- **15% Wahrscheinlichkeit** für eine längere Pause
- **30 Sekunden bis 3 Minuten** zusätzliche Verzögerung
- Simuliert: "Person ist kurz weg", "macht was anderes", etc.

### Berechnungsbeispiele:

```
Nachricht: "Okay 😊" (7 Zeichen)
- Leseverzögerung: 2.1s
- Tippzeit: 7 / 4.2 (chars/s) = 1.7s
- Angewendet: max(2s, 1.7s) = 2s
- Mit Variation (×1.1): 2.2s
- Typing-Indikator: 2.2s
- Gesamtverzögerung: 4.3s

Nachricht: "Das klingt super interessant! Erzähl mir mehr darüber 🤔" (58 Zeichen)
- Leseverzögerung: 1.8s
- Tippzeit: 58 / 4.2 = 13.8s
- Mit Variation (×0.9): 12.4s
- Typing-Indikator: 12.4s
- Gesamtverzögerung: 14.2s

Nachricht mit langer Pause: "Ja genau!" (10 Zeichen)
- Leseverzögerung: 2.5s
- Tippzeit: 2.4s
- Lange Pause: 67s (zufällig)
- Gesamtverzögerung: 71.9s
```

## 2. 🔄 Warm Start - Stil-Lernsystem

### Wie es funktioniert:

1. **Aktivierung**: `/warmstart <chat_id>`
2. **Sammlung**: Nutzer leitet seine eigenen Nachrichten weiter
3. **Speicherung**: Bot speichert bis zu 10 Beispielnachrichten
4. **Analyse**: LLM analysiert den Schreibstil
5. **Integration**: System-Prompt wird erweitert mit Stil-Anweisungen

### Was wird analysiert:

- **Satzlänge**: Kurze vs. lange Sätze
- **Satzstruktur**: Einfach vs. komplex
- **Emoji-Verwendung**: Häufigkeit und Position
- **Formalität**: Du/Sie, Umgangssprache vs. förmlich
- **Typische Ausdrücke**: Füllwörter, Phrasen
- **Grammatik-Eigenheiten**: Dialekt, Abkürzungen
- **Interpunktion**: Häufigkeit von !, ?, ..., etc.

### Beispiel-Analyse:

**Input (deine Nachrichten):**
```
1. "hey! wie läufts? 😊"
2. "cool cool"
3. "haha ja genau das meine ich"
4. "ach krass, wusste ich gar nicht"
5. "muss ich mir mal anschauen!"
```

**LLM-Analyse:**
```
Schreibstil-Analyse:
- Sehr informell und locker
- Kurze, direkte Sätze
- Häufige Verwendung von Emojis (😊)
- Ausrufezeichen am Satzende üblich
- Umgangssprache: "läufts", "krass", "haha"
- Wenig Kommas, einfache Struktur
- Wiederholungen für Betonung ("cool cool")
```

**Erweiterter System-Prompt:**
```
Du bist Lisa... [Original-Prompt]

WICHTIG: Der Nutzer, den du imitierst, hat in der Vergangenheit 
so geschrieben (ahme diesen Stil nach):
1. "hey! wie läufts? 😊"
2. "cool cool"
3. "haha ja genau das meine ich"
...

Schreibe im gleichen lockeren, informellen Stil mit kurzen Sätzen 
und gelegentlichen Emojis.
```

## 3. 🎭 Persönlichkeits-System

### Zweistufiges System:

1. **Basis-Persönlichkeit** (personality.json)
   - Grundcharakter: Name, Alter, Beruf
   - Allgemeine Eigenschaften und Interessen
   - Standard-Gesprächsstil

2. **Individueller Stil** (Warm Start)
   - Überschreibt/erweitert Gesprächsstil
   - Passt sich deinem persönlichen Schreiben an
   - Macht Bot praktisch ununterscheidbar von dir

### Kombination:

Der Bot kombiniert:
- **Was** er sagt (Persönlichkeit aus JSON)
- **Wie** er es sagt (dein Stil aus Warm Start)
- **Wann** er antwortet (Timing-System)

## 4. 📊 Konversations-Management

### Features:

- **Separate Konversationen**: Jede Chat-ID hat eigene Historie
- **Kontext-Limit**: Max. 20 Nachrichten Verlauf (+ System-Prompt)
- **Persistenz**: Stil-Beispiele bleiben gespeichert (im RAM während Bot läuft)
- **Reset-Funktion**: `/reset <chat_id>` löscht Verlauf, behält aber Stil

## 5. 🛡️ Sicherheits-Features

### Admin-Only Kontrolle:

- Nur Admin kann Befehle nutzen
- Nur Admin kann Targets hinzufügen/entfernen
- Bot antwortet nur auf explizit hinzugefügte Chat-IDs

### Privacy:

- Keine Logs von Nachrichteninhalten (nur Metadaten)
- API-Keys in .env (nicht im Code)
- .gitignore verhindert versehentliches Committen

## 6. 🔧 Konfigurierbarkeit

### Anpassbare Parameter:

**Im Code (telegram_bot.py, __init__):**
```python
self.min_delay = 2.0                    # Min. Antwortverzögerung
self.max_delay = 8.0                    # Max. Antwortverzögerung
self.chars_per_second = 3.5-6.0        # Tippgeschwindigkeit
self.occasional_long_pause_chance = 0.15  # 15% für lange Pause
self.long_pause_duration = (30, 180)    # 30s - 3min
```

**In .env:**
```env
LITELLM_MODEL=gpt-3.5-turbo  # LLM-Modell
OPENAI_API_KEY=...            # API Key
```

**In config/personality.json:**
```json
{
  "name": "...",
  "system_prompt": "...",
  ...
}
```

## 7. 📈 Zukünftige Erweiterungen (Ideen)

- [ ] Persistente Speicherung (SQLite/JSON-Datei)
- [ ] Web-Dashboard zur Verwaltung
- [ ] Mehrere Persönlichkeiten pro Chat
- [ ] Zeitbasierte Verfügbarkeit (antwortet nur zu bestimmten Zeiten)
- [ ] Sentiment-Analyse (reagiert auf Stimmung)
- [ ] Automatische Stil-Anpassung während Konversation
- [ ] Bild/Sticker-Support
- [ ] Voice-Message-Support
- [ ] Multi-User (mehrere Admins)
- [ ] Statistiken & Analytics

## 8. 🎯 Best Practices

### Für maximale Unauffälligkeit:

1. **Nutze Warm Start IMMER**
   - Leite 5-10 deiner Nachrichten weiter
   - Je mehr, desto besser die Imitation

2. **Lass den Bot übernehmen, nicht ersetzen**
   - Schreib erst ein paar Nachrichten selbst
   - Dann aktiviere den Bot
   - Nahtloser Übergang

3. **Monitoring**
   - Schau gelegentlich in die Konversation
   - Bei Bedarf `/reset` und neu starten

4. **Persönlichkeit anpassen**
   - Stelle sicher, dass personality.json zu dir passt
   - Je authentischer, desto besser

5. **Timing beobachten**
   - Wenn Bot zu schnell/langsam antwortet
   - Parameter in Code anpassen

## 9. ⚠️ Limitationen

### Aktuelle Einschränkungen:

- **Keine Persistenz**: Bei Bot-Neustart gehen Stil-Beispiele verloren
- **RAM-basiert**: Alle Daten nur im Arbeitsspeicher
- **Keine Bild-Analyse**: Bot kann Bilder nicht interpretieren
- **Statische Persönlichkeit**: Lernt nicht während Konversation
- **Ein Admin**: Nur eine Person kann Bot kontrollieren

### Erkennungsrisiken:

- **Plötzlicher Stilwechsel**: Wenn Bot ohne Warm Start aktiviert wird
- **Zu perfekte Grammatik**: Manche LLMs schreiben zu "sauber"
- **Keine Tippfehler**: Menschen machen Fehler, Bot nicht
- **Immer verfügbar**: Bot antwortet 24/7, Menschen schlafen

### Gegenmaßnahmen:

- **Warm Start** behebt Stilwechsel-Problem
- **System-Prompt** kann "Fehler machen" anweisen
- **Lange Pausen** simulieren "beschäftigt sein"
- **Manuelles Monitoring** für kritische Situationen

## 10. 💡 Technische Details

### Architektur:

```
Telegram ←→ telegram_bot.py ←→ llm_handler.py ←→ LiteLLM ←→ OpenAI/etc.
                ↓
        personality.py ←→ config/personality.json
```

### Async-Flow bei Nachricht:

1. Nachricht empfangen (Telegram)
2. Chat-ID prüfen (in active_targets?)
3. Leseverzögerung (1-3s)
4. LLM-Anfrage starten
5. Typing-Indikator senden (parallel)
6. Tippzeit berechnen
7. Warten (Typing + Tippzeit)
8. Antwort senden

### Dependencies:

- **python-telegram-bot**: Telegram Bot API
- **litellm**: Universelles LLM Interface
- **python-dotenv**: Environment Variables
- **asyncio**: Asynchrone Operationen

Alle Features sind modular und können einzeln an-/abgeschaltet werden!