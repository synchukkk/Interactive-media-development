// Клас для роботи з масивом цілих чисел
#include <iostream>
#include <vector>

class IntArray {
private:
    std::vector<int> arr;
public:
    IntArray(const std::vector<int>& input) : arr(input) {}

    // Метод для знаходження числа, отриманого перемноженням позитивних елементів масиву менших 10
    int productOfPositiveLessThan10() const {
        int product = 1;
        bool found = false;
        for (int num : arr) {
            if (num > 0 && num < 10) {
                product *= num;
                found = true;
            }
        }
        return found ? product : 0;
    }
};

int main() {
    IntArray arr({2, -3, 5, 12, 8, 0, 11, 7});
    std::cout << "Добуток позитивних елементів менших 10: " << arr.productOfPositiveLessThan10() << std::endl;
    return 0;
}
