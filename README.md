# sensor.tautulli

A platform which allows you to get information from Tautulli.
  
To get started put `/custom_components/sensor/tautulli.py` here:  
`<config directory>/custom_components/sensor/tautulli.py`  
  
**Example configuration.yaml:**

```yaml
sensor:
  platform: tautulli
  api_key: 24b6eac0a858748664878d146bf63623b4
  host: 192.168.1.14
  port: 8181
  attributes:
    - magic_title
```

**Configuration variables:**  

key | description  
:--- | :---  
**platform (Required)** | The sensor platform name.  
**api_key (Required)** | Your Tautulli api_key  
**host (Required)** | The IP adress of the server running Tautulli.  
**port (Optional)** | The port the Tautulli uses, defaults to `8181`  
**attributes (Optional)** | A list of [attributes](attributes.md) you want to monitor.  

***
Due to how `custom_componentes` are loaded, it is normal to see a `ModuleNotFoundError` error on first boot after adding this, to resolve it, restart Home-Assistant.
