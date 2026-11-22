// Host test for level.{h,cpp} (SR-022). Built and run with g++ by tests/test_level.py.
#include <cstdio>
#include "../level.h"

static int fails = 0;
#define CHECK(c) do { if (!(c)) { std::printf("FAIL line %d: %s\n", __LINE__, #c); ++fails; } } while (0)

int main() {
  CHECK(level::echo_to_mm(1749, 200) == 300);   // 300 mm at 20 degC (c = 343.4 m/s)
  CHECK(level::echo_to_mm(1749, 400) == 310);   // warmer air -> faster sound -> longer reading for same echo
  CHECK(level::echo_to_mm(0, 200) == 0);
  CHECK(level::echo_to_mm(30000, 200) == 0);    // timeout

  const level::Config cfg{400, 100, 40, 80, 70, 500, 30, 600};
  level::Filter f(cfg);
  f.tick(0);
  CHECK(f.state() == level::State::kFault);
  uint32_t t = 0;
  for (int i = 0; i < 3; ++i) f.add(380, t += 100);
  CHECK(f.state() == level::State::kLow);
  f.add(130, t += 100);  // one spike: median holds
  CHECK(f.state() == level::State::kLow);
  f.add(130, t += 100);  // two of last three at 130: median 130 -> 90 %, first vote
  CHECK(f.state() == level::State::kLow);
  f.add(130, t += 100);  // second vote
  CHECK(f.state() == level::State::kFull);
  CHECK(f.percent() == 90);
  for (int i = 0; i < 4; ++i) f.add(175, t += 100);  // 75 %: above release, stays full
  CHECK(f.state() == level::State::kFull);
  f.add(10, t += 100);  // blind zone, rejected
  CHECK(f.rejected() == 1);
  f.tick(t + 600);
  CHECK(f.state() == level::State::kFault);
  std::printf("%s\n", fails ? "FAILED" : "OK");
  return fails ? 1 : 0;
}
