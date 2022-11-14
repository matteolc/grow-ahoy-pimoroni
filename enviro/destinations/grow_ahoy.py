import config
import urequests

from enviro import logging


def upload_reading(reading):
  payload = {
      "timestamp": reading["timestamp"]
  }

  for key, value in reading["readings"].items():
    sensor_type = key
    payload.update({"value": value})
    logging.info("Upoloading payload: ", payload)

    station_uuid = config.grow_ahoy_station_uuid
    unit_uuid = config.grow_ahoy_unit_uuid
    url = f"http://192.168.1.78:55000/factory/{station_uuid}/{unit_uuid}/{sensor_type}"
    logging.info("Uploading to: ", url)

    headers = {'X-Source-Token': config.grow_ahoy_api_key,
               'Content-Type': 'application/json'}

    try:
      result = urequests.post(url, json=payload, headers=headers)
      if result.status_code in [200, 201, 202]:
        logging.info("Readings uploaded!")
        result.close()
    except Exception as error:
      logging.error(f"Failed to upload readings: {error}")

  return True
