from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.event import async_track_state_change_event

from .const import DOMAIN
from .database import StateCounterDB

async def async_setup(hass: HomeAssistant, config: ConfigType):
    """Setup der YAML-basierten State Counter Integration."""
    if DOMAIN not in config:
        return True

    entities = config[DOMAIN].get("entities", [])
    if not entities:
        return True

    # DB initialisieren (im config-Verzeichnis)
    db = StateCounterDB(hass.config.path())

    @callback
    def state_change_listener(event):
        """Callback: nur echte Zustandsänderungen zählen (old != new)."""
        entity_id = event.data.get("entity_id")
        if entity_id not in entities:
            return

        old_state = event.data.get("old_state")
        new_state = event.data.get("new_state")

        # Wenn einer der States None ist → ignorieren (z.B. bei Start)
        if old_state is None or new_state is None:
            return

        # Nur zählen, wenn sich der tatsächliche State geändert hat
        if old_state.state == new_state.state:
            return

        # Zähler persistent erhöhen
        new_value = db.increment(entity_id)

        # Aktuellen Zähler als State veröffentlichen (sichtbar in Entitäten-Liste)
        hass.states.async_set(
            f"{DOMAIN}.{entity_id.replace('.', '_')}",
            new_value,
            {
                "friendly_name": f"State count {entity_id}",
                "entity_tracked": entity_id
            }
        )

    # Listener für alle angegebenen Entitäten registrieren
    async_track_state_change_event(hass, entities, state_change_listener)

    return True