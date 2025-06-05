#include <iostream>
#include <cmath>
using namespace std;

class Polygon {
public:
    virtual double perimeter() const = 0;
    virtual ~Polygon() {}
};

class Triangle : public Polygon {
    double a, b, c;
public:
    Triangle(double a, double b, double c) : a(a), b(b), c(c) {}
    double perimeter() const override {
        return a + b + c;
    }
};

class Rectangle : public Polygon {
    double width, height;
public:
    Rectangle(double width, double height) : width(width), height(height) {}
    double perimeter() const override {
        return 2 * (width + height);
    }
};

class Pentagon : public Polygon {
    double side;
public:
    Pentagon(double side) : side(side) {}
    double perimeter() const override {
        return 5 * side;
    }
};

int main() {
    Triangle t(3, 4, 5);
    Rectangle r(4, 6);
    Pentagon p(2);

    cout << "Периметр трикутника: " << t.perimeter() << endl;
    cout << "Периметр прямокутника: " << r.perimeter() << endl;
    cout << "Периметр п'ятикутника: " << p.perimeter() << endl;

    return 0;
}
