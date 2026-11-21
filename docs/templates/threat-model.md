# Threat model — <scope> (rev <N>, <YYYY-MM-DD>)

Owner · reviewers · related SR / ADR / DFMEA IDs. Method: STRIDE per data flow; risk = impact (1–5) × likelihood (1–5).

## Assets
| Asset | Why it matters (safety, privacy, availability, integrity) |
|---|---|

## Data flows and trust boundaries
| Flow | From → To | Channel | Crosses boundary? |
|---|---|---|---|
| Camera frames | USB camera → vision (Linux) | USB/V4L2 | Yes (physical device) |
| Calibration / routes | Phone → web UI | Wi-Fi HTTP(S) | Yes |
| Motion commands | Linux → MCU | Bridge RPC | Yes (Linux not trusted for safety) |
| Operator card | Card → RC522 → MCU/Linux | SPI | Yes |

## Threats
| ID | Flow | STRIDE | Attack scenario | Impact | Likelihood | Risk | Control | SR | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|---|

## Residual risks and accepted limits
<e.g., RFID UID cloning accepted for the prototype; vision spoofing accepted because vision is advisory>

## Verification
Security test protocol/report IDs and results.
