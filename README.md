# HA TPollens FR

Intégration Home Assistant pour afficher les indices polliniques français via Atmo France dans un seul capteur par commune.

## Fonctionnalités

- Un capteur par ville : `sensor.pollens_fr_<nom_commune>`
- Attributs contenant les indices par type de pollen pour aujourd'hui, demain, et après-demain

## Installation

1. Ajoutez ce dépôt dans HACS
2. Installez l'intégration
3. Redémarrez Home Assistant
4. Allez dans Paramètres > Intégrations > Ajouter > "Pollens France"

## Configuration via l'interface

Vous devrez fournir :

- votre identifiant et mot de passe Atmo-France
- le nom et le code de votre commune
- le code EPCI associé

## Licence

MIT
