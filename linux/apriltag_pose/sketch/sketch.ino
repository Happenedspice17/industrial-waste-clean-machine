#include <Arduino_RouterBridge.h>

volatile float px, py, pyaw;
volatile int ntags;
volatile unsigned long last_ms;

void onPose(float x, float y, float yaw, int n) {
  px = x; py = y; pyaw = yaw; ntags = n;
  last_ms = millis();
}

void setup() {
  Bridge.begin();
  Monitor.begin();
  Bridge.provide("pose", onPose);
}

void loop() {
  static unsigned long t0;
  if (millis() - t0 < 500) return;
  t0 = millis();
  if (millis() - last_ms > 1000) {
    Monitor.println("pose STALE");
  } else if (ntags == 0) {
    Monitor.println("no tag");
  } else {
    Monitor.print("x="); Monitor.print(px, 3);
    Monitor.print(" y="); Monitor.print(py, 3);
    Monitor.print(" yaw="); Monitor.print(pyaw * 57.2958, 1);
    Monitor.print(" tags="); Monitor.println(ntags);
  }
}
