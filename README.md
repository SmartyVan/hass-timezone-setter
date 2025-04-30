# Timezone Setter

Set your Home Assistant system timezone dynamically using either:
- A direct [IANA timezone string](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) (e.g., `America/New_York`)
- Or geographic coordinates (`latitude` and `longitude`) via [timezonefinderL](https://timezonefinder.readthedocs.io/en/latest/1_usage.html#timezonefinderl): a fast and lightweight python package for looking up the corresponding timezone for given coordinates on earth entirely offline!

This integration is useful for mobile installations (like vans, RVs or boats), or automations that require adjusting the system timezone based on location. Best of all, it does not require an internet connection.

---

## 🔧 Installation

### HACS Installation (Custom Repository)

This integration is not yet available in the HACS default store, however you can still install it via HACS as a custom repository:

1. In Home Assistant, go to **HACS → Integrations**
2. Click the **⋮ (three-dot menu)** in the top right
3. Choose **"Custom repositories"**
4. In the dialog:
   - **Repository**: `https://github.com/SmartyVan/hass-timezone-setter`
   - **Category**: `Integration`
5. Click **Add**

The integration will then appear in your HACS Integrations list and can be installed and updated like any other.

### Or, Manual Installation

1. Copy this repository to your Home Assistant config folder:
   ```
   custom_components/timezone_setter/
   ```

2. Restart Home Assistant.

3. The integration will register a service:
   ```
   timezone_setter.set_timezone
   ```

---

## ⚙️ Usage

Call the `timezone_setter.set_timezone` service via the Developer Tools, automations, or scripts.

### You can provide:
- A **timezone** string (preferred if known), *or*
- A **latitude** + **longitude** pair, from which the integration will detect the proper timezone

### Example service call (YAML):

```yaml
service: timezone_setter.set_timezone
data:
  timezone: "America/Chicago"
```
Or:

```yaml
service: timezone_setter.set_timezone
data:
  latitude: 40.7128
  longitude: -74.0060
```

If both are provided, `timezone` takes priority and coordinates will be ignored.

---

## 📝 Notes

- Uses [`timezonefinderL`](https://timezonefinder.readthedocs.io/en/latest/1_usage.html#timezonefinderl) for fast and lightweight timezone lookup without an internet connection.
- Service requires admin permissions.
- Only updates the system timezone (does not affect individual users or devices).

---

## 📄 License

MIT License

---

## 🙋‍♂️ Author

Created by [@SmartyVan](https://github.com/SmartyVan)
