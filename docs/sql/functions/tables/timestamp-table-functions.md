| Function | Description | Example |
|:--|:--|:---|
| `generate_series(`*`timestamp`*`, `*`timestamp`*`, `*`interval`*`)` | Generate a table of timestamps in the closed range, stepping by the interval | `generate_series(TIMESTAMP '2001-04-10', TIMESTAMP '2001-04-11', INTERVAL 30 MINUTE)` |
| `range(`*`timestamp`*`, `*`timestamp`*`, `*`interval`*`)` | Generate a table of timestamps in the half open range, stepping by the interval | `range(TIMESTAMP '2001-04-10', TIMESTAMP '2001-04-11', INTERVAL 30 MINUTE)` |
