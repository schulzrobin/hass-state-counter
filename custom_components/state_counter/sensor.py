from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .database import StateCounterDB

async def async_setup(hass: HomeAssistant, config: ConfigType):
    # YAML-only Variante: nichts tun (sensor entities werden per hass.states gesetzt)
    return True

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    # Wird nicht automatisch verwendet; belassen wir für Kompatibilität
    return

# Alternative: falls du die Entitäten manuell als Sensoren anlegen willst (erfordert Anpassung)
class StateCounterSensor(Entity):
    def __init__(self, entity_id: str, db: StateCounterDB):
        self._entity_id = entity_id
        self._db = db
        self._attr_name = f"State Counter {entity_id}"
        self._attr_unique_id = f"{DOMAIN}_{entity_id}"

    @property
    def name(self):
        return self._attr_name

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def state(self):
        return self._db.get_count(self._entity_id)