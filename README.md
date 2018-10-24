# sensor.tautulli [![Build Status](https://travis-ci.com/custom-components/sensor.tautulli.svg?branch=master)](https://travis-ci.com/custom-components/sensor.tautulli)

A platform which allows you to get information from Tautulli.
  
To get started put `/custom_components/sensor/tautulli.py` here:  
`<config directory>/custom_components/sensor/tautulli.py`  
  
**Example configuration.yaml:**

```yaml
sensor:
  platform: tautulli
  api_key: 24b6eac0a858748664878d146bf63623b4
  host: 192.168.1.14
  monitored_variables:
    - magic_title
```

**Configuration variables:**  

key | description  
:--- | :---  
**platform (Required)** | The sensor platform name.  
**api_key (Required)** | Your Tautulli api_key  
**host (Required)** | The IP adress of the server running Tautulli.  
**port (Optional)** | The port the Tautulli uses, defaults to `8181`  
**ssl (Optional)** | Set to `True`if your Tautulli instance uses SSL, defaults to `False`.
**monitored_variables (Optional)** | A list of [monitored_variables](monitored_variables.md) you want to monitor.  
**monitored_users (Optional)** | A list of users you want to monitor, if none is defined all users will be monitored. **NB!: Case sensetive!**

***
Due to how `custom_componentes` are loaded, it is normal to see a `ModuleNotFoundError` error on first boot after adding this, to resolve it, restart Home-Assistant.
