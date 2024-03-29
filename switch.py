import logging
import time
from homeassistant.components.switch import SwitchDevice

REQUIREMENTS = ['fritzconnection==0.8.2']
_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    _LOGGER.debug('Setting up fritz_guestwifi Component')
    host = config.get('host', '169.254.1.1')
    port = config.get('port', 49000)
    username = config.get('username', '')
    password = config.get('password', None)

    if not password:
        raise ValueError('Password is not set in configuration')

    guest_wifi = FritzBoxGuestWifi(
        host=host,
        port=port,
        username=username,
        password=password
    )

    async_add_entities([guest_wifi])


class FritzBoxGuestWifi(SwitchDevice):

    def __init__(self, host, port, username, password):
        # pylint: disable=import-error
        import fritzconnection as fc
        self._connection = fc.FritzConnection(
            address=host,
            port=port,
            user=username,
            password=password
        )
        self._name = "GuestWifi"
        self._state = None
        self._icon = "mdi:wifi"
        self._update_timestamp = time.time()

    @property
    def name(self):
        """Name of GuestWifi switch."""
        return self._name

    @property
    def icon(self):
        """Icon of GuestWifi switch."""
        return self._icon

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    def turn_on(self, **kwargs):
        _LOGGER.info('Turning on guest wifi.')
        self._handle_turn_on_off(True)

    def turn_off(self, **kwargs):
        _LOGGER.info('Turning off guest wifi.')
        self._handle_turn_on_off(False)

    async def async_fetch_state(self):
        from fritzconnection.fritzconnection import ServiceError, ActionError
        try:
            status = self._connection.call_action('WLANConfiguration:3', 'GetInfo')["NewStatus"]
            return True if status == "Up" else False
        except ServiceError or ActionError:
            _LOGGER.error('Could not get Guest Wifi state')

    async def async_update(self):
        if time.time() > (self._update_timestamp + 60):
            self._state = await self.async_fetch_state()

    def _handle_turn_on_off(self, turn_on):
        from fritzconnection.fritzconnection import ServiceError, ActionError
        new_state = '1' if turn_on else '0'
        try:
            self._update_timestamp = time.time()
            self._connection.call_action('WLANConfiguration:3', 'SetEnable', NewEnable=new_state)
            self._state = turn_on
        except ServiceError or ActionError:
            _LOGGER.error('Home Assistant cannot call the wished service on the FRITZ!Box. '
                          'Are credentials, address and port correct?')
