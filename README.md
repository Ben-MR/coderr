# Coderr Project - Backend

Coderr ist eine Freelancer-Plattform speziell für Softwareentwickler. Diese API bildet das Rückgrat der Anwendung und verwaltet Nutzer, Angebote, Bestellungen und Reviews.

Das zugehörige Frontend findest du hier: coderr-frontend

Version: 1.0

## Funktionen
User Management: Registrierung und Login-System mit Unterscheidung zwischen Business und Customer.

Angebotsverwaltung: Erstellen und Verwalten von Dienstleistungen durch Business-User.

Bestellsystem: Vollständiger Bestellprozess für Kunden.

Review System: Kunden können Bewertungen abgeben, bearbeiten und löschen.

Profile: Anpassbare Nutzerprofile für alle Teilnehmer.

## Voraussetzungen
Python: Version 3.x

Framework: Django & Django REST Framework

Abhängigkeiten: Siehe requirements.txt

## Installation
Projekt klonen:

```bash
git clone git@github.com:DanielSchn/coderr-backend.git
cd coderr-backend
```

##Virtual Environment erstellen:

### Erstellen
```bash
python -m venv env
```

### Aktivieren (Linux/Mac)
```bash
source env/bin/activate
```

### Aktivieren (Windows)
```bash
env\Scripts\activate
```
## Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

### Datenbank initialisieren:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Server starten:
```bash
python manage.py runserver
```
Die API ist nun unter http://127.0.0.1:8000 erreichbar.

## Superuser (Admin) erstellen
Um Zugriff auf das Django Admin-Panel zu erhalten, führe folgende Befehle in der Shell aus:

Shell öffnen:

```bash
python manage.py shell
```

### Admin & Profil anlegen:
Kopiere diesen Block in die Shell (Passe E-Mail und Passwort ggf. an):

Python
```bash
from django.contrib.auth import get_user_model
from coderr_app.models import UserProfile

User = get_user_model()

Superuser erstellen
superuser = User.objects.create_superuser(
    username='admin', 
    email='admin@example.com', 
    password='securepassword'
)

Zugehöriges Profil erstellen
UserProfile.objects.create(
    user=superuser, 
    location='Berlin', 
    tel='1234567890', 
    description='Admin profile', 
    working_hours='9 AM - 5 PM', 
    type='staff'
)
```

### Konfiguration (Kern-Einstellungen)
Das Projekt nutzt das Django REST Framework mit folgenden Kern-Einstellungen in der settings.py:

Authentifizierung: TokenAuthentication

Berechtigungen: IsAuthenticatedOrReadOnly (Lesen für alle, Schreiben nur für eingeloggte User).

Filter: DjangoFilterBackend für präzise API-Abfragen.

### Nutzung & Befehle
Befehl	               Beschreibung
```bash
python manage.py makemigrations	   Erstellt Migrationsdateien für Modelländerungen.
python manage.py migrate	       Wendet Änderungen auf die Datenbank an.
python manage.py runserver	       Startet den lokalen Entwicklungsserver.
python manage.py test	           Führt die automatisierte Test-Suite aus.
```

#Lizenz
Dieses Projekt wurde als Lernprojekt erstellt und steht derzeit unter keiner spezifischen Lizenz.
