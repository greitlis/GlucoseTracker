# Glukose Tracker for KIDS
Der Glukose Tracker soll Kindern mit Insulinpflichtigem Diabetes helfen ihre Blutzuckerwerte im Überblick zu behalten. Nach dem Anlegen eines Logins können in der App Blutzuckerwerte eingertagen und mit aktuellem Datum und Uhrzeit gespeichert werden. Im Glukosetagebuch kann man sich den Verlauf der eingetragenen Werte in Tabellenform oder graphisch anschauen. Die Rubrik Verordnungen dient dazu die Angaben des zuständigen Arztes der zuständigen Ärztin sowie das Spritzschema der individuellen Insulintherapie fest zuhalten.
Die App ist bewusst übersichtlich und simpel gehalten, damit sie auch von jüngeren Nutzern einfach und selbständig bedient werden kann.

## Secrets einrichten
Für die Verbindung zum Daten-Repo braucht es eine `secrets.toml` Datei, welche lokal im Ordner `.streamlit` liegt. Die Datei ist und wird nicht im Github hochgeladen. Folgendes in der secrets.toml Datei eingeben:

```
[github]
owner = "username"
repo = "glucose-database"
token = "xyz"
```

Das Daten-Repo (privat) ist unter folgendem Link zu finden:
https://github.com/greitlis/glucose-database

## Packages installieren
Um die App zu starten, müssen Packages installiert werden. Diese sind im `requirements.txt` festgehalten und können wie folgt installiert werden

```
pip install -r requirements.txt
```

## App starten
Um die Streamlit App zu starten muss folgender Befehl in einem Terminal ausgeführt werden:
```
streamlit run Home.py
```
## Debugging mit VS Code
Zum Starten die Datei öffnen, die man debuggen will (Home.py). Dannach auf "Run and Debug" und das Profil `Python Debugger: Current File Streamlit` auswählen.

## Link zum Streamlit App
https://glucosetracker-forkids.streamlit.app

## Git konfigurieren
Um Änderungen am Code direkt in Github zu laden, muss man sich für Git einen Usernamen konfigurieren. Dazu folgende Befehle im Terminal eingeben:
```
git config --global user.email schmidt@students.zhaw.ch    
git config --global user.name "Judith Schmidt"   
```                    

