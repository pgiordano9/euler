// Copyright 2026 Peter Giordano.

#include <iostream>

int main() {
  using std::cout;
  uint64_t sum = 2;
  uint32_t fnum = 1;
  uint32_t snum = 2;

  while (snum < 4000000) {
    uint32_t newNum = fnum + snum;

    if (newNum % 2 == 0) {
      sum += newNum;
    }

    fnum = snum;
    snum = newNum;
  }

  cout << sum;
  return 0;
}
