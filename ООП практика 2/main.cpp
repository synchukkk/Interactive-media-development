// Демонстрація множинного успадкування в C++
// B - базовий клас
// D1, D2, D3, D4, D5 - похідні класи з різними типами наслідування

#include <iostream>
using namespace std;

class B {
protected:
    int b;
public:
    B() : b(1) {}
    void showB() { cout << "B: " << b << endl; }
};

// D1 успадковує B public
class D1 : public B {
protected:
    int d1;
public:
    D1() : d1(2) {}
    void showD1() { cout << "D1: " << d1 << endl; }
};

// D2 успадковує B private
class D2 : private B {
protected:
    int d2;
public:
    D2() : d2(3) {}
    void showD2() { cout << "D2: " << d2 << endl; }
    void showBfromD2() { showB(); } // доступ до B через D2
};

// D3 успадковує B private
class D3 : private B {
protected:
    int d3;
public:
    D3() : d3(4) {}
    void showD3() { cout << "D3: " << d3 << endl; }
};

// D4 успадковує D1 private та D2 public
class D4 : private D1, public D2 {
    int d4;
public:
    D4() : d4(5) {}
    void showD4() { cout << "D4: " << d4 << endl; }
};

// D5 успадковує D2 public та D3 private
class D5 : public D2, private D3 {
    int d5;
public:
    D5() : d5(6) {}
    void showD5() { cout << "D5: " << d5 << endl; }
};

int main() {
    D4 obj4;
    obj4.showD4();
    obj4.showD2();
    obj4.showBfromD2();
    // obj4.showD1(); // помилка: D1 private

    D5 obj5;
    obj5.showD5();
    obj5.showD2();
    obj5.showBfromD2();
    // obj5.showD3(); // помилка: D3 private
    return 0;
}
