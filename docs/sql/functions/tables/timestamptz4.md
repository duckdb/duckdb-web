| Function | Description | Example |
|:--|:---|:---|
| `generate_series(`*`timestamptz`*`, `*`timestamptz`*`, `*`interval`*`)` | Generate a table of timestamps in the closed range (including both the starting timestamp and the ending timestamp), stepping by the interval | `generate_series(TIMESTAMPTZ '2001-04-10', TIMESTAMPTZ '2001-04-11', INTERVAL 30 MINUTE)` |
| `range(`*`timestamptz`*`, `*`timestamptz`*`, `*`interval`*`)` | Generate a table of timestamps in the half open range (including the starting timestamp, but stopping before the ending timestamp) , stepping by the interval | `range(TIMESTAMPTZ '2001-04-10', TIMESTAMPTZ '2001-04-11', INTERVAL 30 MINUTE)` |
