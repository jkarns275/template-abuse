#include <array>
#include <iostream>
#include <stdio.h>

#include "magic.hxx"

#include "fortunes.hxx"
#include "greetings.hxx"

int main() {
  std::random_device r;
  rng = std::default_random_engine(r());

  greetings g;
  g.sample();
  std::cout << "Please enter your name: ";

  std::string name;
  std::cin >> name;

  printf(s.c_str(), name.c_str());

  std::cout << "\nHere is your fortune...\n";
  s.clear();
  fortunes f;
  f.sample();
  std::cout << s << "\n";
}
