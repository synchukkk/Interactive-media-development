#ifndef FUNCTION_H
#define FUNCTION_H
#include <vector>
#include <string>

struct Point {
    double x;
    double y;
};

class Function {
public:
    Function();
    bool loadFromFile(const std::string& filename);
    bool saveFormattedToFile(const std::string& filename) const;
    double getMinY() const;
    double getMaxY() const;
    void printMinMax() const;
    void plot() const;
private:
    std::vector<Point> points;
};

#endif // FUNCTION_H
