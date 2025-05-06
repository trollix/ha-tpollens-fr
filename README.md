# HA TPollens FR

Intégration Home Assistant pour afficher les indices polliniques français via Atmo France dans un seul capteur.

## Fonctionnalités

- Un seul capteur `sensor.pollens_fr`
- Attributs contenant les indices par type de pollen pour aujourd'hui, demain, et après-demain

## Installation

1. Ajoutez ce dépôt dans HACS
2. Installez l'intégration
3. Redémarrez Home Assistant
4. Ajoutez une configuration YAML

## Configuration YAML

```yaml
sensor:
  - platform: ha_tpollens_fr
    username: "votre_login"
    password: "votre_mot_de_passe"
    zone:
      nom: "Pessac"
      code: "33318"
      codeEpci: "243300316"
```

## Licence

MIT
