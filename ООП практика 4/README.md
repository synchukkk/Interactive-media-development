# Шаблонний клас «Розумний вказівник» (SmartPointer)

Цей проект містить просту реалізацію шаблонного класу розумного вказівника на C++. Клас SmartPointer забезпечує автоматичне управління динамічною пам’яттю, подібно до std::unique_ptr, але з базовою функціональністю для навчальних цілей.

## Можливості
- Автоматичне видалення об’єкта при знищенні розумного вказівника
- Оператори розіменування (->, *)
- Заборона копіювання (аналог unique_ptr)
- Підтримка переміщення (move semantics)
- Методи release, reset, get

## Використання

```cpp
#include "SmartPointer.h"
#include <iostream>

class Test {
public:
    Test() { std::cout << "Test created\n"; }
    ~Test() { std::cout << "Test destroyed\n"; }
    void hello() { std::cout << "Hello!\n"; }
};

int main() {
    SmartPointer<Test> ptr(new Test());
    ptr->hello();
    ptr.reset(new Test());
    ptr->hello();
    Test* raw = ptr.release();
    if (raw) raw->hello();
    delete raw;
    return 0;
}
```

## Файли
- `SmartPointer.h` — реалізація шаблонного класу
- `main.cpp` (у цьому ж файлі) — приклад використання

## Як скомпілювати

Використайте будь-який компілятор C++ (наприклад, g++):

```
g++ -std=c++11 Pr4 -o main.exe
./main.exe
```

## Ліцензія

Цей код призначений для навчальних цілей.
