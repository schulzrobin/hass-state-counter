# State Counter (Home Assistant Integration)

Diese Integration zählt echte Zustandsänderungen (State Changes) ausgewählter Home Assistant Entitäten
und speichert sie dauerhaft in einer SQLite-Datenbank.

## Installation über HACS

1. HACS → Custom Repositories → URL eintragen
2. Typ: Integration
3. Installieren
4. In `configuration.yaml` konfigurieren:

```yaml
state_counter:
  entities:
    - switch.wohnzimmer
    - light.kueche