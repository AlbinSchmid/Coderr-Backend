# Coderr/ Backend Projekt

Dieses Projekt ist das Backend von Coderr, entwickelt mit Django und Django REST Framework.

---

## Installation & Setup

## Voraussetzungen

Stelle sicher, dass du Python 3.9+ und pip installiert hast.

## Repository klonen

git clone https://github.com/deinusername/coderr-backend.git
cd coderr-backend

## Virtuelle Umgebung erstellen & aktivieren

python -m venv venv  # Virtuelle Umgebung erstellen
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

## Abhängigkeiten installieren

pip install -r requirements.txt

## Konfiguration

Erstelle eine .env-Datei im Root-Verzeichnis und füge deine Umgebungsvariablen hinzu:

DEBUG=True
SECRET_KEY=dein-geheimer-schlüssel
DATABASE_URL=sqlite:///db.sqlite3  # Oder PostgreSQL/MySQL Verbindungsstring

## Datenbankmigrationen ausführen

python manage.py migrate

## Server starten

python manage.py runserver

Der Server läuft nun unter: http://127.0.0.1:8000/

## API-Dokumentation

Die API ist unter http://127.0.0.1:8000/api/ erreichbar.
Falls Django REST Framework Browsable API aktiviert ist, kannst du Endpunkte direkt testen.

## Wichtige Technologien

Django (5.1.6)

Django REST Framework (3.15.2)

django-cors-headers (4.7.0) für Cross-Origin-Requests

django-filter (25.1) für Query-Filter

python-dotenv (1.0.1) für Umgebungsvariablen

## Entwickeln & Testen

### Superuser erstellen (für Admin-Zugang)

python manage.py createsuperuser

### Tests ausführen

python manage.py test

## Deployment

Für ein Deployment mit Gunicorn und PostgreSQL:

pip install gunicorn psycopg2-binary
python manage.py collectstatic --noinput


## Mitwirken

Pull Requests sind willkommen! Stelle sicher, dass deine Änderungen getestet sind.
