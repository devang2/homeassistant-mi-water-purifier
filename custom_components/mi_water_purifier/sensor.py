"""Support for Xiaomi water purifier."""
import math
import logging

from homeassistant.const import (CONF_NAME, CONF_HOST, CONF_TOKEN, )
from homeassistant.helpers.entity import Entity
from homeassistant.exceptions import PlatformNotReady
from miio import Device, DeviceException
from datetime import timedelta

SCAN_INTERVAL = timedelta(seconds=10)
_LOGGER = logging.getLogger(__name__)

TAP_WATER_QUALITY = {'name': 'Tap water', 'key': 'ttds'}
FILTERED_WATER_QUALITY = {'name': 'Filtered water', 'key': 'ftds'}
PP_COTTON_FILTER_REMAINING = {'name': 'PP cotton filter', 'key': 'pfd', 'days_key': 'pfp'}
PP_USED_FLOW = {'name': 'PP filter used flow', 'key': 'ppusedflow'}
PP_TOTAL_FLOW = {'name': 'PP filter total flow', 'key': 'pptotalflow'}
PP_USED_TIME = {'name': 'PP filter used time', 'key': 'ppusedtime'}
PP_TOTAL_TIME = {'name': 'PP filter total time', 'key': 'pptotaltime'}
PP_REMAINING_TIME = {'name': 'PP filter remaining time', 'key': 'ppremainingtime'}
FRONT_ACTIVE_CARBON_FILTER_REMAINING = {'name': 'Front active carbon filter', 'key': 'fcfd', 'days_key': 'fcfp'}
FRONT_USED_FLOW = {'name': 'front filter used flow', 'key': 'frontusedflow'}
FRONT_TOTAL_FLOW = {'name': 'front filter total flow', 'key': 'fronttotalflow'}
FRONT_USED_TIME = {'name': 'front filter used time', 'key': 'frontusedtime'}
FRONT_TOTAL_TIME = {'name': 'front filter total time', 'key': 'fronttotaltime'}
FRONT_REMAINING_TIME = {'name': 'front filter remaining time', 'key': 'frontremainingtime'}
RO_FILTER_REMAINING = {'name': 'RO filter', 'key': 'rfd', 'days_key': 'rfp'}
RO_USED_FLOW = {'name': 'RO filter used flow', 'key': 'rousedflow'}
RO_TOTAL_FLOW = {'name': 'RO filter total flow', 'key': 'rototalflow'}
RO_USED_TIME = {'name': 'RO filter used time', 'key': 'rousedtime'}
RO_TOTAL_TIME = {'name': 'RO filter total time', 'key': 'rototaltime'}
RO_REMAINING_TIME = {'name': 'RO filter remaining time', 'key': 'roremainingtime'}
REAR_ACTIVE_CARBON_FILTER_REMAINING = {'name': 'Rear active carbon filter', 'key': 'rcfd', 'days_key': 'rcfp'}
REAR_USED_FLOW = {'name': 'rear filter used flow', 'key': 'rearusedflow'}
REAR_TOTAL_FLOW = {'name': 'rear filter total flow', 'key': 'reartotalflow'}
REAR_USED_TIME = {'name': 'rear filter used time', 'key': 'rearusedtime'}
REAR_TOTAL_TIME = {'name': 'rear filter total time', 'key': 'reartotaltime'}
REAR_REMAINING_TIME = {'name': 'rear filter remaining time', 'key': 'rearremainingtime'}

TEST18 = {'name': 'status18', 'key': 'status18'}
TEST19 = {'name': 'status19', 'key': 'status19'}
TEST20 = {'name': 'status20', 'key': 'status20'}
TEST21 = {'name': 'status21', 'key': 'status21'}
TEST22 = {'name': 'status22', 'key': 'status22'}

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Perform the setup for Xiaomi water purifier."""

    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)
    token = config.get(CONF_TOKEN)

    _LOGGER.info("Initializing Xiaomi water purifier with host %s (token %s...)", host, token[:5])

    devices = []
    try:
        device = Device(host, token)
        waterPurifier = XiaomiWaterPurifier(device, name)
        devices.append(waterPurifier)
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, TAP_WATER_QUALITY))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, FILTERED_WATER_QUALITY))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, PP_COTTON_FILTER_REMAINING))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, PP_USED_FLOW))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, PP_TOTAL_FLOW))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, PP_USED_TIME))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, PP_TOTAL_TIME))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, PP_REMAINING_TIME))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, FRONT_ACTIVE_CARBON_FILTER_REMAINING))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, FRONT_USED_FLOW))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, FRONT_TOTAL_FLOW))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, FRONT_USED_TIME))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, FRONT_TOTAL_TIME))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, FRONT_REMAINING_TIME))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, RO_FILTER_REMAINING))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, RO_USED_FLOW))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, RO_TOTAL_FLOW))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, RO_USED_TIME))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, RO_TOTAL_TIME))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, RO_REMAINING_TIME))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, REAR_ACTIVE_CARBON_FILTER_REMAINING))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, REAR_USED_FLOW))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, REAR_TOTAL_FLOW))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, REAR_USED_TIME))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, REAR_TOTAL_TIME))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, REAR_REMAINING_TIME))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, TEST18))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, TEST19))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, TEST20))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, TEST21))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, TEST22))

    except DeviceException:
        _LOGGER.exception('Fail to setup Xiaomi water purifier')
        raise PlatformNotReady

    add_devices(devices)

class XiaomiWaterPurifierSensor(Entity):
    """Representation of a XiaomiWaterPurifierSensor."""

    def __init__(self, waterPurifier, data_key):
        """Initialize the XiaomiWaterPurifierSensor."""
        self._state = None
        self._data = None
        self._waterPurifier = waterPurifier
        self._data_key = data_key
        self.parse_data()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._data_key['name']

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        if self._data_key['key'] is TAP_WATER_QUALITY['key'] or \
           self._data_key['key'] is FILTERED_WATER_QUALITY['key']:
            return 'mdi:water'
        elif self._data_key['key'] is PP_USED_FLOW['key'] or \
             self._data_key['key'] is PP_TOTAL_FLOW['key'] or \
             self._data_key['key'] is FRONT_USED_FLOW['key'] or \
             self._data_key['key'] is FRONT_TOTAL_FLOW['key'] or \
             self._data_key['key'] is RO_USED_FLOW['key'] or \
             self._data_key['key'] is RO_TOTAL_FLOW['key'] or \
             self._data_key['key'] is REAR_USED_FLOW['key'] or \
             self._data_key['key'] is REAR_TOTAL_FLOW['key']:
              return 'mdi:water-percent'
        elif self._data_key['key'] is PP_USED_TIME['key'] or \
             self._data_key['key'] is PP_TOTAL_TIME['key'] or \
             self._data_key['key'] is PP_REMAINING_TIME['key'] or \
             self._data_key['key'] is FRONT_USED_TIME['key'] or \
             self._data_key['key'] is FRONT_TOTAL_TIME['key'] or \
             self._data_key['key'] is FRONT_REMAINING_TIME['key'] or \
             self._data_key['key'] is RO_USED_TIME['key'] or \
             self._data_key['key'] is RO_TOTAL_TIME['key'] or \
             self._data_key['key'] is RO_REMAINING_TIME['key'] or \
             self._data_key['key'] is REAR_USED_TIME['key'] or \
             self._data_key['key'] is REAR_TOTAL_TIME['key'] or \
             self._data_key['key'] is REAR_REMAINING_TIME['key']:
              return 'mdi:clock'
        else:
            return 'mdi:filter-outline'

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        if self._data_key['key'] is TAP_WATER_QUALITY['key'] or \
           self._data_key['key'] is FILTERED_WATER_QUALITY['key']:
            return 'TDS'
        elif self._data_key['key'] is PP_USED_FLOW['key'] or \
             self._data_key['key'] is PP_TOTAL_FLOW['key'] or \
             self._data_key['key'] is FRONT_USED_FLOW['key'] or \
             self._data_key['key'] is FRONT_TOTAL_FLOW['key'] or \
             self._data_key['key'] is RO_USED_FLOW['key'] or \
             self._data_key['key'] is RO_TOTAL_FLOW['key'] or \
             self._data_key['key'] is REAR_USED_FLOW['key'] or \
             self._data_key['key'] is REAR_TOTAL_FLOW['key']:
              return 'L'
        elif self._data_key['key'] is PP_USED_TIME['key'] or \
             self._data_key['key'] is PP_TOTAL_TIME['key'] or \
             self._data_key['key'] is PP_REMAINING_TIME['key'] or \
             self._data_key['key'] is FRONT_USED_TIME['key'] or \
             self._data_key['key'] is FRONT_TOTAL_TIME['key'] or \
             self._data_key['key'] is FRONT_REMAINING_TIME['key'] or \
             self._data_key['key'] is RO_USED_TIME['key'] or \
             self._data_key['key'] is RO_TOTAL_TIME['key'] or \
             self._data_key['key'] is RO_REMAINING_TIME['key'] or \
             self._data_key['key'] is REAR_USED_TIME['key'] or \
             self._data_key['key'] is REAR_TOTAL_TIME['key'] or \
             self._data_key['key'] is REAR_REMAINING_TIME['key']:
              return 'days'
        elif self._data_key['key'] is TEST18['key'] or \
             self._data_key['key'] is TEST19['key'] or \
             self._data_key['key'] is TEST20['key'] or \
             self._data_key['key'] is TEST21['key'] or \
             self._data_key['key'] is TEST22['key']:
            return ''
        else:
            return '%'
        return '%'

    @property
    def device_state_attributes(self):
        """Return the state attributes of the last update."""
        attrs = {}

        if self._data_key['key'] is PP_COTTON_FILTER_REMAINING['key'] or \
           self._data_key['key'] is FRONT_ACTIVE_CARBON_FILTER_REMAINING['key'] or \
           self._data_key['key'] is RO_FILTER_REMAINING['key'] or \
           self._data_key['key'] is REAR_ACTIVE_CARBON_FILTER_REMAINING['key']:
            attrs[self._data_key['name']] = '{} days remaining'.format(self._data[self._data_key['days_key']])

        return attrs

    def parse_data(self):
        if self._waterPurifier._data:
            self._data = self._waterPurifier._data
            self._state = self._data[self._data_key['key']]

    def update(self):
        """Get the latest data and updates the states."""
        self.parse_data()

class XiaomiWaterPurifier(Entity):
    """Representation of a XiaomiWaterPurifier."""

    def __init__(self, device, name):
        """Initialize the XiaomiWaterPurifier."""
        self._state = None
        self._device = device
        self._name = name
        self.parse_data()

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return 'mdi:water'

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return 'TDS'

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def hidden(self) -> bool:
        """Return True if the entity should be hidden from UIs."""
        return True

    @property
    def device_state_attributes(self):
        """Return the state attributes of the last update."""
        attrs = {}
        attrs[TAP_WATER_QUALITY['name']] = '{}TDS'.format(self._data[TAP_WATER_QUALITY['key']])
        attrs[PP_COTTON_FILTER_REMAINING['name']] = '{}%'.format(self._data[PP_COTTON_FILTER_REMAINING['key']])
        attrs[PP_USED_FLOW['name']] = '{}L'.format(self._data[PP_USED_FLOW['key']])
        attrs[PP_TOTAL_FLOW['name']] = '{}L'.format(self._data[PP_TOTAL_FLOW['key']])
        attrs[PP_USED_TIME['name']] = '{}days'.format(self._data[PP_USED_TIME['key']])
        attrs[PP_TOTAL_TIME['name']] = '{}days'.format(self._data[PP_TOTAL_TIME['key']])
        attrs[PP_REMAINING_TIME['name']] = '{}days'.format(self._data[PP_REMAINING_TIME['key']])
        attrs[FRONT_ACTIVE_CARBON_FILTER_REMAINING['name']] = '{}%'.format(self._data[FRONT_ACTIVE_CARBON_FILTER_REMAINING['key']])
        attrs[FRONT_USED_FLOW['name']] = '{}L'.format(self._data[FRONT_USED_FLOW['key']])
        attrs[FRONT_TOTAL_FLOW['name']] = '{}L'.format(self._data[FRONT_TOTAL_FLOW['key']])
        attrs[FRONT_USED_TIME['name']] = '{}days'.format(self._data[FRONT_USED_TIME['key']])
        attrs[FRONT_TOTAL_TIME['name']] = '{}days'.format(self._data[FRONT_TOTAL_TIME['key']])
        attrs[FRONT_REMAINING_TIME['name']] = '{}days'.format(self._data[FRONT_REMAINING_TIME['key']])
        attrs[RO_FILTER_REMAINING['name']] = '{}%'.format(self._data[RO_FILTER_REMAINING['key']])
        attrs[RO_USED_FLOW['name']] = '{}L'.format(self._data[RO_USED_FLOW['key']])
        attrs[RO_TOTAL_FLOW['name']] = '{}L'.format(self._data[RO_TOTAL_FLOW['key']])
        attrs[RO_USED_TIME['name']] = '{}days'.format(self._data[RO_USED_TIME['key']])
        attrs[RO_TOTAL_TIME['name']] = '{}days'.format(self._data[RO_TOTAL_TIME['key']])
        attrs[RO_REMAINING_TIME['name']] = '{}days'.format(self._data[RO_REMAINING_TIME['key']])
        attrs[REAR_ACTIVE_CARBON_FILTER_REMAINING['name']] = '{}%'.format(self._data[REAR_ACTIVE_CARBON_FILTER_REMAINING['key']])
        attrs[REAR_USED_FLOW['name']] = '{}L'.format(self._data[REAR_USED_FLOW['key']])
        attrs[REAR_TOTAL_FLOW['name']] = '{}L'.format(self._data[REAR_TOTAL_FLOW['key']])
        attrs[REAR_USED_TIME['name']] = '{}days'.format(self._data[REAR_USED_TIME['key']])
        attrs[REAR_TOTAL_TIME['name']] = '{}days'.format(self._data[REAR_TOTAL_TIME['key']])
        attrs[REAR_REMAINING_TIME['name']] = '{}days'.format(self._data[REAR_REMAINING_TIME['key']])

        attrs[TEST18['name']] = '{} test18'.format(self._data[TEST18['key']])
        attrs[TEST19['name']] = '{} test19'.format(self._data[TEST19['key']])
        attrs[TEST20['name']] = '{} test20'.format(self._data[TEST20['key']])
        attrs[TEST21['name']] = '{} test21'.format(self._data[TEST21['key']])
        attrs[TEST22['name']] = '{} test22'.format(self._data[TEST22['key']])

        return attrs

    def parse_data(self):
        """Parse data."""
        try:
            data = {}
            """status = self._device.get_properties(["all"])"""
            """status = self._device.send('get_prop', [])"""
            status = self._device.get_properties(["all"])
            data[TAP_WATER_QUALITY['key']] = status[0]
            data[FILTERED_WATER_QUALITY['key']] = status[1]
            pfd = int((status[11] - status[3]) / 24)
            data[PP_COTTON_FILTER_REMAINING['days_key']] = pfd
            data[PP_COTTON_FILTER_REMAINING['key']] = math.floor(pfd * 24 * 100 / status[11])
            data[PP_USED_FLOW['key']] = status[2]
            data[PP_TOTAL_FLOW['key']] = status[10]
            ppusedtime = int(status[3]/24)
            data[PP_USED_TIME['key']] = ppusedtime
            pptotaltime = int(status[11]/24)
            data[PP_TOTAL_TIME['key']] = pptotaltime
            ppremainingtime = int((status[11] - status[3])/24)
            data[PP_REMAINING_TIME['key']] = ppremainingtime
            fcfd = int((status[13] - status[5]) / 24)
            data[FRONT_ACTIVE_CARBON_FILTER_REMAINING['days_key']] = fcfd
            data[FRONT_ACTIVE_CARBON_FILTER_REMAINING['key']] = math.floor(fcfd * 24 * 100 / status[13])
            data[FRONT_USED_FLOW['key']] = status[4]
            data[FRONT_TOTAL_FLOW['key']] = status[12]
            frontusedtime = int(status[5]/24)
            data[FRONT_USED_TIME['key']] = frontusedtime
            fronttotaltime = int(status[13]/24)
            data[FRONT_TOTAL_TIME['key']] = fronttotaltime
            frontremainingtime = int((status[13] - status[5])/24)
            data[FRONT_REMAINING_TIME['key']] = frontremainingtime
            rfd = int((status[15] - status[7]) / 24)
            data[RO_FILTER_REMAINING['days_key']] = rfd
            data[RO_FILTER_REMAINING['key']] = math.floor(rfd * 24 * 100 / status[15])
            data[RO_USED_FLOW['key']] = status[6]
            data[RO_TOTAL_FLOW['key']] = status[14]
            rousedtime = int(status[7]/24)
            data[RO_USED_TIME['key']] = rousedtime
            rototaltime = int(status[15]/24)
            data[RO_TOTAL_TIME['key']] = rototaltime
            roremainingtime = int((status[15] - status[7])/24)
            data[RO_REMAINING_TIME['key']] = roremainingtime
            rcfd = int((status[17] - status[9]) / 24)
            data[REAR_ACTIVE_CARBON_FILTER_REMAINING['days_key']] = rcfd
            data[REAR_ACTIVE_CARBON_FILTER_REMAINING['key']] = math.floor(rcfd * 24 * 100 / status[17])
            data[REAR_USED_FLOW['key']] = status[8]
            data[REAR_TOTAL_FLOW['key']] = status[16]
            rearusedtime = int(status[9]/24)
            data[REAR_USED_TIME['key']] = rearusedtime
            reartotaltime = int(status[17]/24)
            data[REAR_TOTAL_TIME['key']] = reartotaltime
            rearremainingtime = int((status[17] - status[9])/24)
            data[REAR_REMAINING_TIME['key']] = rearremainingtime

            data[TEST18['key']] = status[18]
            data[TEST19['key']] = status[19]
            data[TEST20['key']] = status[20]
            data[TEST21['key']] = status[21]
            data[TEST22['key']] = status[22]

            self._data = data
            self._state = self._data[FILTERED_WATER_QUALITY['key']]
        except DeviceException:
            _LOGGER.exception('Fail to get_prop from Xiaomi water purifier')
            self._data = None
            self._state = None
            raise PlatformNotReady

    def update(self):
        """Get the latest data and updates the states."""
        self.parse_data()
