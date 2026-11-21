# ADR-0003: Hardware emergency stop through main relay

- Status: accepted · Date: 2026-10-09 · Requirements: SR-006, SR-014

## Decision
LAY37 mushroom e-stop (NC) in series with the 40 A main relay coil feeding the switched 12 V bus (drive, collection,
separation). Logic stays powered to report. E-stop state also read by the MCU. Restart requires RFID + start button.
## Consequences
Relay inrush/contact welding is a DFMEA item (F-003); WCCA must check contact ratings; a certified product would need
a safety relay with monitored contacts (ISO 13849-1).
