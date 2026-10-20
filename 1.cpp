// Copyright 2026 Peter Giordano.

#include <iostream>

int main() {
  using std::cout;
  uint32_t sum = 0;

  for (int i = 3; i < 1000; i++) {
    if (i % 3 == 0 || i % 5 == 0) {
      sum = sum + i;
    }
  }

  cout << sum;
  return 0;
}
