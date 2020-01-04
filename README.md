Brings back `api_password` authentication for home assistant API.

# Setup

1. Clone / copy this repository to your home assistant config `custom_components` directory, eg:

``` shell
cd my-home-assistant-config-path
git clone https://github.com/biern/hass-http_legacy_auth.git custom_components/http_legacy_auth
```

2. Set config in `configuration.yaml`:

``` yaml
http_legacy_auth:
  api_password: !secret http_password
```

Password should be declared in `secrets.yaml`.
