#include <iostream>
#include <complex>
using namespace std;

// Шаблон класу масиву
// T - тип елементів масиву

template<typename T>
class Array {
    T* data;
    int size;
public:
    Array(int n) : size(n) {
        data = new T[size];
    }
    ~Array() {
        delete[] data;
    }
    T& operator[](int i) {
        return data[i];
    }
    int getSize() const {
        return size;
    }
    void print() const {
        for (int i = 0; i < size; ++i) {
            cout << data[i] << " ";
        }
        cout << endl;
    }
};

// Клас користувача
class Point {
    double x, y;
public:
    Point(double x = 0, double y = 0) : x(x), y(y) {}
    friend ostream& operator<<(ostream& os, const Point& p) {
        os << "(" << p.x << ", " << p.y << ")";
        return os;
    }
};

int main() {
    // Масив цілих чисел
    Array<int> arrInt(3);
    arrInt[0] = 1; arrInt[1] = 2; arrInt[2] = 3;
    cout << "Array<int>: "; arrInt.print();

    // Масив дійсних чисел
    Array<double> arrDouble(3);
    arrDouble[0] = 1.1; arrDouble[1] = 2.2; arrDouble[2] = 3.3;
    cout << "Array<double>: "; arrDouble.print();

    // Масив комплексних чисел
    Array<complex<double>> arrComplex(2);
    arrComplex[0] = complex<double>(1, 2);
    arrComplex[1] = complex<double>(3, 4);
    cout << "Array<complex<double>>: "; arrComplex.print();

    // Масив точок (клас користувача)
    Array<Point> arrPoint(2);
    arrPoint[0] = Point(1, 2);
    arrPoint[1] = Point(3, 4);
    cout << "Array<Point>: "; arrPoint.print();

    return 0;
}
