#include "Function.h"
#include <fstream>
#include <iomanip>
#include <iostream>
#include <algorithm>

Function::Function() {}

bool Function::loadFromFile(const std::string& filename) {
    std::ifstream fin(filename);
    if (!fin) return false;
    points.clear();
    double x, y;
    while (fin >> x >> y) {
        points.push_back({x, y});
    }
    return true;
}

bool Function::saveFormattedToFile(const std::string& filename) const {
    std::ofstream fout(filename);
    if (!fout) return false;
    for (const auto& p : points) {
        fout << std::setw(10) << std::showpos << std::fixed << std::setprecision(3) << p.x << "\t"
             << std::setw(10) << std::showpos << std::fixed << std::setprecision(3) << p.y << "\n";
    }
    return true;
}

double Function::getMinY() const {
    if (points.empty()) return 0;
    return std::min_element(points.begin(), points.end(), [](const Point& a, const Point& b){ return a.y < b.y; })->y;
}

double Function::getMaxY() const {
    if (points.empty()) return 0;
    return std::max_element(points.begin(), points.end(), [](const Point& a, const Point& b){ return a.y < b.y; })->y;
}

void Function::printMinMax() const {
    std::cout << "Min Y: " << getMinY() << std::endl;
    std::cout << "Max Y: " << getMaxY() << std::endl;
}

void Function::plot() const {
    // Simple ASCII plot for demonstration
    double minY = getMinY();
    double maxY = getMaxY();
    int height = 10;
    for (int i = height; i >= 0; --i) {
        double y = minY + (maxY - minY) * i / height;
        std::cout << std::setw(8) << std::fixed << std::setprecision(2) << y << " | ";
        for (const auto& p : points) {
            if (std::abs(p.y - y) < (maxY - minY) / height / 2) std::cout << "*";
            else std::cout << " ";
        }
        std::cout << std::endl;
    }
    std::cout << "         +";
    for (size_t i = 0; i < points.size(); ++i) std::cout << "-";
    std::cout << std::endl << "          ";
    for (const auto& p : points) std::cout << std::setw(1) << int(p.x);
    std::cout << std::endl;
}
