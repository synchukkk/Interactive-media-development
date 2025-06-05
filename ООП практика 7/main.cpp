#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

struct HelpEntry {
    std::string term;
    std::vector<std::string> explanation; // 1-5 рядків
};

// Початкове формування тексту допомоги
void initializeHelp(std::vector<HelpEntry>& helpList) {
    helpList.clear();
    helpList.push_back({"Клас", {"Клас — це шаблон для створення об'єктів, що описує їхню структуру та поведінку."}});
    helpList.push_back({"Об'єкт", {"Об'єкт — це екземпляр класу з конкретними значеннями полів."}});
    helpList.push_back({"Інкапсуляція", {"Інкапсуляція — це механізм приховування деталей реалізації об'єкта."}});
}

// Виведення всього тексту допомоги
void printAllHelp(const std::vector<HelpEntry>& helpList) {
    std::cout << "\nТекст допомоги:\n";
    for (const auto& entry : helpList) {
        std::cout << "Термін: " << entry.term << std::endl;
        for (const auto& line : entry.explanation) {
            std::cout << "  " << line << std::endl;
        }
        std::cout << std::endl;
    }
}

// Виведення пояснення для заданого терміну
void printExplanation(const std::vector<HelpEntry>& helpList) {
    std::cout << "Введіть термін: ";
    std::string searchTerm;
    std::getline(std::cin, searchTerm);
    bool found = false;
    for (const auto& entry : helpList) {
        if (entry.term == searchTerm) {
            std::cout << "Пояснення для терміну '" << entry.term << "':" << std::endl;
            for (const auto& line : entry.explanation) {
                std::cout << "  " << line << std::endl;
            }
            found = true;
            break;
        }
    }
    if (!found) {
        std::cout << "Термін не знайдено!" << std::endl;
    }
}

// Меню
void showMenu() {
    std::cout << "\nМеню:\n";
    std::cout << "1. Початкове формування тексту допомоги\n";
    std::cout << "2. Вивести весь текст допомоги\n";
    std::cout << "3. Вивести пояснення для заданого терміну\n";
    std::cout << "0. Вийти\n";
    std::cout << "Оберіть пункт меню: ";
}

int main() {
    std::vector<HelpEntry> helpList;
    int choice;
    do {
        showMenu();
        std::string input;
        std::getline(std::cin, input);
        try {
            choice = std::stoi(input);
        } catch (...) {
            choice = -1;
        }
        switch (choice) {
            case 1:
                initializeHelp(helpList);
                std::cout << "Текст допомоги сформовано!" << std::endl;
                break;
            case 2:
                printAllHelp(helpList);
                break;
            case 3:
                printExplanation(helpList);
                break;
            case 0:
                std::cout << "Вихід з програми." << std::endl;
                break;
            default:
                std::cout << "Некоректний вибір! Спробуйте ще раз." << std::endl;
        }
    } while (choice != 0);
    return 0;
}
