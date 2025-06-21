Projekt: Lokales multimodales KI-System für Chat, Bildverständnis und Bildgenerierung

Ziel:
Erstellung eines vollständig lokal lauffähigen multimodalen Frameworks zur Interaktion über Text, Bildverständnis und Bildgenerierung. Das System soll keine externen APIs oder Cloud-Dienste verwenden. Die gesamte Inferenz soll lokal auf einer Workstation mit 24 GB VRAM erfolgen.

Hauptkomponenten:
1. Text-LLM (Chatmodul)
2. Vision-Modul (Bildanalyse)
3. Bildgenerator (Text-zu-Bild)

Hardwarevorgabe:
- 1 GPU mit 24 GB VRAM (z. B. RTX 4090 oder Äquivalent)
- 64 GB RAM empfohlen
- Lokales Betriebssystem: Linux (Ubuntu 22.04 LTS empfohlen)

Module im Detail:

1. Text-LLM:
Modell: Mistral-7B-Instruct (GGUF-Format, quantisiert)
Backend: llama.cpp
Ausführung: CPU oder GPU (abhängig von Systemlast)
Ziel: Durchführung natürlicher Textdialoge und Prompt-Interpretation

2. Vision-Modul:
Modell: LLaVA-1.5-7B (HuggingFace)
Vision-Encoder: ViT-G / CLIP mit BLIP2-Unterstützung
Backend: HuggingFace transformers + accelerate + bitsandbytes
Ziel: Analyse und semantische Beschreibung hochgeladener Bilder

3. Bildgenerierung:
Modell: Stable Diffusion 1.5 (alternativ: SDXL oder SDXL-Turbo)
Backend: diffusers oder invokeAI
LoRA-Unterstützung: Ja (z. B. projektinterne Modelle wie „olymp_V4“)
Ziel: Erzeugung von Bildern auf Basis natürlicher Spracheingaben

Software-Framework:
- Hauptinterface: Gradio (lokale Web-Oberfläche)
- Sprache: Python 3.10+
- Struktur: Modular (chat.py, vision.py, generator.py, main.py)
- Optional: Docker-Compose-Struktur zur Containerisierung

Anforderungen:
- Alle Modelle müssen lokal ausführbar und offline verfügbar sein
- Ressourcen müssen sequentiell oder nach Bedarf geladen werden
- System muss promptbasiert zwischen den Modulen wechseln können
- Inferenzgeschwindigkeit und Speichernutzung sollen optimiert werden
- Keine API-Keys oder Drittanbieter-Zugriffe erlaubt

Optionale Erweiterungen:
- REST-Schnittstelle zur externen Integration
- Prompt-Controller zur dynamischen Verzweigung (z. B. LangChain)
- CLI-Modus für Headless-Ausführung

Zielgruppe:
Entwicklungsumgebungen ohne Internetzugang, Datenschutz-kritische Infrastruktur, private AI-Server

Status:
Bereit zur Umsetzung. Implementierungsstart sobald Moduldefinitionen bereitstehen.
