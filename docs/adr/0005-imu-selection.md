# ADR-0005: IMU — BNO055 (IMU mode) preferred over MPU-6050

- Status: proposed · Date: 2026-11-15 · Requirements: R7, R8

## Decision
BNO055 in IMU mode (no magnetometer: unreliable near steel and motors): on-chip fusion saves firmware time. MPU-6050
is cheap but EOL (mostly clones) and needs own fusion; acceptable fallback because LiDAR scan matching corrects
heading drift. Test I2C clock stretching on the STM32U585 early. Note: BME280/BMP280 are barometers, not IMUs.
