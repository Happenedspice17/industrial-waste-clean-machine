// Ultrasonic waste level (SR-022, ADR-0010): HC-SR04 echo pulse -> filtered level and state.
// Planning measurement only. The float shut-off at the vacuum port stays the hardware overfill protection (rule 1).
// No dynamic allocation; feed() is safe to call from the main loop for every received byte.
#pragma once
#include <stdint.h>

namespace level {

// HC-SR04: 10 us TRIG pulse, ECHO high time = round trip. Echo is 5 V: it reaches the MCU through a divider
// (WCCA hcsr04_echo_divider). Trigger the two sensors (tank, basket) alternately, >= 60 ms apart, to avoid crosstalk.
constexpr uint32_t kEchoTimeoutUs = 30000;  // no echo (> ~5 m) -> no reading

// Round-trip echo time (us) and air temperature (0.1 degC, from the DS18B20 or 200 = 20 degC) -> distance in mm.
// Returns 0 when the echo timed out or is shorter than the blind zone.
uint16_t echo_to_mm(uint32_t echo_us, int16_t temp_deci_c);

enum class State : uint8_t { kLow = 0, kHalf = 1, kFull = 2, kFault = 3 };

struct Config {
  uint16_t empty_mm;      // reading with the container empty (measured on the robot)
  uint16_t full_mm;       // reading at the usable-full mark (measured), must be < empty_mm
  uint8_t half_pct;       // >= half_pct -> kHalf
  uint8_t full_pct;       // >= full_pct -> kFull
  uint8_t release_pct;    // leave kFull below release_pct (hysteresis)
  uint16_t stale_ms;      // no valid reading for this long -> kFault
  uint16_t min_valid_mm;  // below the blind zone -> reading discarded
  uint16_t max_valid_mm;  // above the container depth -> reading discarded
};

class Filter {
 public:
  explicit Filter(const Config& c) : cfg_(c) {}
  // Add one raw reading taken at now_ms. Out-of-range readings are counted, not used.
  void add(uint16_t mm, uint32_t now_ms);
  // Evaluate staleness; call every loop.
  void tick(uint32_t now_ms);
  State state() const { return state_; }
  uint8_t percent() const { return pct_; }
  uint16_t rejected() const { return rejected_; }

 private:
  State classify(uint8_t pct) const;
  Config cfg_;
  uint16_t hist_[3] = {0, 0, 0};
  uint8_t count_ = 0;
  uint8_t pct_ = 0;
  State state_ = State::kFault;
  State candidate_ = State::kFault;
  uint8_t votes_ = 0;
  uint32_t last_ms_ = 0;
  bool seen_ = false;
  uint16_t rejected_ = 0;
};

}  // namespace level
