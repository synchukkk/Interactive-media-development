#include "Function.h"
#include <iostream>

int main() {
    Function f;
    if (!f.loadFromFile("data.txt")) {
        std::cerr << "Не вдалося відкрити файл data.txt" << std::endl;
        return 1;
    }
    std::cout << "Графік функції (ASCII):" << std::endl;
    f.plot();
    f.printMinMax();
    if (!f.saveFormattedToFile("formatted_data.txt")) {
        std::cerr << "Не вдалося записати у formatted_data.txt" << std::endl;
        return 2;
    }
    std::cout << "Дані збережено у formatted_data.txt" << std::endl;
    return 0;
}
