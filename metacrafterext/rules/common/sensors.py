"""Low-cost air quality sensor networks (Sensor.Community, sensors.AFRICA): sensor models and the
value types of their readings."""
import re

_SENSOR_MODEL = re.compile(
    r"^(?:SDS0(?:11|18|21)|PMS[1-9]003|PMSA003|SPS30|HPM|PPD42NS|DHT(?:11|22)|BME(?:280|680)|BMP(?:180|280)"
    r"|HTU21D|SHT(?:3[015]|85)|DS18B20|SPH0645(?:_MIC)?|DNMS|MQ-?\d{1,3}|BAM[ -]?10[12]0|SEN5X|NEXTPM|IPS-7100)$")


def validate_air_sensor_model(value):
    """A sensor model of Sensor.Community or sensors.AFRICA: SDS011, pms5003, DHT22, BME280, BAM 1020,
    SPH0645_MIC, MQ-7 (not P2, DHT or a station name)."""
    return bool(_SENSOR_MODEL.match(str(value).strip().upper()))


SENSOR_COMMUNITY_VALUE_TYPES = frozenset((
    "P0", "P1", "P2", "P4", "N05", "N1", "N25", "N4", "N10", "TS", "temperature", "humidity", "pressure",
    "pressure_at_sealevel", "noise_LAeq", "noise_LA_min", "noise_LA_max", "noise_Leq", "durP1", "durP2",
    "ratioP1", "ratioP2", "samples", "min_micro", "max_micro", "interval", "hdop", "lat", "lon", "height",
    "timestamp",
))
_MEASURES = frozenset(("P0", "P1", "P2", "temperature", "humidity", "pressure", "noise_LAeq", "noise_Leq"))


def validate_sensor_community_value_type(value):
    """A value type of a Sensor.Community reading: P1 (PM10), P2 (PM2.5), P0 (PM1), temperature,
    humidity, noise_LAeq, durP1 (not PM2.5, P3 or Temperature)."""
    return str(value).strip() in SENSOR_COMMUNITY_VALUE_TYPES


def validate_sensor_community_measure(value):
    """A value type that is a measure, for the rule on values alone: P0, P1, P2, temperature,
    humidity, pressure, noise_LAeq (the diagnostics lat, lon, samples are left to the field name)."""
    return str(value).strip() in _MEASURES
