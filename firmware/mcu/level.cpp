#include "level.h"

namespace level {

namespace {
constexpr uint8_t kVotesNeeded = 2;  // rule 6: confirm a state change on 2 consecutive filtered reads
constexpr uint8_t kVotesCap = 3;     // capped vote counter

uint16_t median3(uint16_t a, uint16_t b, uint16_t c) {
  if (a > b) { uint16_t t = a; a = b; b = t; }
  if (b > c) { b = c; }
  return a > b ? a : b;
}
}  // namespace

uint16_t echo_to_mm(uint32_t echo_us, int16_t temp_deci_c) {
  if (echo_us == 0 || echo_us >= kEchoTimeoutUs) return 0;
  // speed of sound c = 331.3 + 0.606 * T  (m/s) -> in mm/us * 1e4: 3313 + 0.606 * T(0.1 degC)
  const int32_t c_e4 = 3313 + (606 * static_cast<int32_t>(temp_deci_c)) / 1000;
  const uint32_t mm = (echo_us * static_cast<uint32_t>(c_e4)) / 20000;  // round trip / 2
  return mm > 0xFFFF ? 0xFFFF : static_cast<uint16_t>(mm);
}

State Filter::classify(uint8_t pct) const {
  if (state_ == State::kFull && pct >= cfg_.release_pct) return State::kFull;
  if (pct >= cfg_.full_pct) return State::kFull;
  if (pct >= cfg_.half_pct) return State::kHalf;
  return State::kLow;
}

void Filter::add(uint16_t mm, uint32_t now_ms) {
  if (mm < cfg_.min_valid_mm || mm > cfg_.max_valid_mm) {
    ++rejected_;
    return;
  }
  hist_[count_ % 3] = mm;
  if (count_ < 255) ++count_;
  last_ms_ = now_ms;
  seen_ = true;
  if (count_ < 3) return;
  const uint16_t d = median3(hist_[0], hist_[1], hist_[2]);
  const int32_t span = static_cast<int32_t>(cfg_.empty_mm) - static_cast<int32_t>(cfg_.full_mm);
  int32_t pct = span > 0 ? (static_cast<int32_t>(cfg_.empty_mm) - d) * 100 / span : 100;
  if (pct < 0) pct = 0;
  if (pct > 100) pct = 100;
  pct_ = static_cast<uint8_t>(pct);
  const State s = classify(pct_);
  if (s == state_) {
    votes_ = 0;
    return;
  }
  if (s == candidate_) {
    if (votes_ < kVotesCap) ++votes_;
  } else {
    candidate_ = s;
    votes_ = 1;
  }
  if (votes_ >= kVotesNeeded || state_ == State::kFault) {
    state_ = s;
    votes_ = 0;
  }
}

void Filter::tick(uint32_t now_ms) {
  if (!seen_ || now_ms - last_ms_ > cfg_.stale_ms) {
    state_ = State::kFault;
    count_ = 0;
  }
}

}  // namespace level
