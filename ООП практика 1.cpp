#include <iostream>
#include <string>
#include <iomanip>

using namespace std;

// Базовий клас Rahunok (Рахунок)
class Rahunok {
protected:
    int nomerRahunku;           // унікальний номер рахунка
    double suma;                // сума на рахунку
    double vidsotkiBase;        // базові відсотки
    double vidsotkiDodatkovi;   // додаткові відсотки
    
public:
    // Конструктор з параметрами
    Rahunok(int nomer, double pochatkovaSuma, double baseVidsotky = 5.0) {
        nomerRahunku = nomer;
        suma = pochatkovaSuma;
        vidsotkiBase = baseVidsotky;
        vidsotkiDodatkovi = 0.0;
        cout << "Створено рахунок №" << nomerRahunku << endl;
    }
    
    // Деструктор
    virtual ~Rahunok() {
        cout << "Знищено рахунок №" << nomerRahunku << endl;
    }
    
    // Функція відображення рахунка
    virtual void pokazatyRahunok() {
        cout << "\n=== ІНФОРМАЦІЯ ПРО РАХУНОК ===" << endl;
        cout << "Номер рахунка: " << nomerRahunku << endl;
        cout << "Сума на рахунку: " << fixed << setprecision(2) << suma << " грн" << endl;
        cout << "Базові відсотки: " << vidsotkiBase << "%" << endl;
        cout << "Додаткові відсотки: " << vidsotkiDodatkovi << "%" << endl;
        cout << "Загальні відсотки: " << (vidsotkiBase + vidsotkiDodatkovi) << "%" << endl;
    }
    
    // Встановлення додаткових відсотків
    void vstanovytyDodatkoviVidsotky(double dodatkovi) {
        vidsotkiDodatkovi = dodatkovi;
        cout << "Встановлено додаткові відсотки: " << dodatkovi << "%" << endl;
    }
    
    // Перерахування грошей з урахуванням відсотків
    void pererahuvaty() {
        double zahalniVidsotky = vidsotkiBase + vidsotkiDodatkovi;
        double narahування = suma * (zahalniVidsotky / 100);
        suma += narahування;
        
        cout << "Нараховано відсотки: " << fixed << setprecision(2) 
             << narahування << " грн" << endl;
        cout << "Нова сума на рахунку: " << suma << " грн" << endl;
    }
    
    // Геттери для доступу до даних
    int getNomerRahunku() const { return nomerRahunku; }
    double getSuma() const { return suma; }
};

// Похідний клас Vkladnyk (Вкладник)
class Vkladnyk : public Rahunok {
private:
    string serijaPassportu;     // серія паспорту
    string nomerPassportu;      // номер паспорту
    string prizvysche;          // прізвище
    string imja;                // ім'я
    string pobatkovi;           // по батькові
    
public:
    // Конструктор з параметрами
    Vkladnyk(int nomerRah, double pochatkovaSuma, double baseVidsotky,
             string serija, string nomerPass, string prizv, string im, string pobat)
        : Rahunok(nomerRah, pochatkovaSuma, baseVidsotky) {
        serijaPassportu = serija;
        nomerPassportu = nomerPass;
        prizvysche = prizv;
        imja = im;
        pobatkovi = pobat;
        cout << "Створено вкладника: " << prizvysche << " " << imja << " " << pobat << endl;
    }
    
    // Деструктор
    ~Vkladnyk() {
        cout << "Знищено дані вкладника: " << prizvysche << " " << imja << endl;
    }
    
    // Функція відображення даних про вкладника
    void pokazatyVkladnyka() {
        cout << "\n=== ДАНІ ПРО ВКЛАДНИКА ===" << endl;
        cout << "ПІБ: " << prizvysche << " " << imja << " " << pobatkovi << endl;
        cout << "Паспорт: серія " << serijaPassportu << ", номер " << nomerPassportu << endl;
    }
    
    // Перевизначена функція відображення рахунка (показує і дані вкладника, і рахунка)
    void pokazatyRahunok() override {
        pokazatyVkladnyka();        // спочатку показуємо дані вкладника
        Rahunok::pokazatyRahunok(); // потім показуємо дані рахунка
    }
    
    // Функція для зміни даних паспорту
    void zminytyPassport(string novaSeria, string novyNomer) {
        serijaPassportu = novaSeria;
        nomerPassportu = novyNomer;
        cout << "Оновлено дані паспорту: серія " << novaSeria 
             << ", номер " << novyNomer << endl;
    }
    
    // Функція для зміни ПІБ
    void zminytyPIB(string novePrizv, string noveIm, string novePobat) {
        prizvysche = novePrizv;
        imja = noveIm;
        pobatkovi = novePobat;
        cout << "Оновлено ПІБ: " << prizvysche << " " << imja << " " << pobatkovi << endl;
    }
    
    // Геттери
    string getPovneImja() const {
        return prizvysche + " " + imja + " " + pobatkovi;
    }
    
    string getPassport() const {
        return serijaPassportu + " " + nomerPassportu;
    }
};

// Головна функція для демонстрації роботи класів
int main() {
    cout << "=== ПРАКТИЧНА РОБОТА №1: БАЗОВЕ УСПАДКУВАННЯ ===" << endl;
    cout << "Студент: Синчук Ярослав" << endl;
    cout << "Варіант 13: Класи Rahunok та Vkladnyk" << endl;
    cout << "================================================" << endl;
    
    // Створення об'єкта базового класу Rahunok
    cout << "\n1. Створення базового рахунка:" << endl;
    Rahunok* rahunok1 = new Rahunok(12345, 10000.0, 7.5);
    rahunok1->pokazatyRahunok();                           // відображення інформації про рахунок
    rahunok1->vstanovytyDodatkoviVidsotky(2.5);           // встановлення додаткових відсотків
    rahunok1->pererahuvaty();                             // перерахування з відсотками
    
    cout << "\n" << string(50, '-') << endl;
    
    // Створення об'єкта похідного класу Vkladnyk
    cout << "\n2. Створення вкладника з рахунком:" << endl;
    Vkladnyk* vkladnyk1 = new Vkladnyk(
        67890,              // номер рахунка
        25000.0,            // початкова сума
        6.0,                // базові відсотки
        "КТ",               // серія паспорту
        "123456",           // номер паспорту
        "Іваненко",         // прізвище
        "Іван",             // ім'я
        "Іванович"          // по батькові
    );
    
    // Демонстрація роботи методів похідного класу
    vkladnyk1->pokazatyRahunok();                         // відображає і дані вкладника, і рахунка
    vkladnyk1->vstanovytyDodatkoviVidsotky(3.0);         // успадкований метод
    vkladnyk1->pererahuvaty();                           // успадкований метод
    
    cout << "\n" << string(50, '-') << endl;
    
    // Демонстрація додаткових методів вкладника
    cout << "\n3. Оновлення даних вкладника:" << endl;
    vkladnyk1->zminytyPassport("АВ", "789012");          // зміна паспортних даних
    vkladnyk1->zminytyPIB("Петренко", "Петро", "Петрович"); // зміна ПІБ
    vkladnyk1->pokazatyVkladnyka();                      // показ оновлених даних вкладника
    
    cout << "\n" << string(50, '-') << endl;
    
    // Створення ще одного вкладника для демонстрації
    cout << "\n4. Створення другого вкладника:" << endl;
    Vkladnyk vkladnyk2(
        11111,              // номер рахунка
        50000.0,            // початкова сума
        8.0,                // базові відсотки
        "МК",               // серія паспорту
        "987654",           // номер паспорту
        "Сидоренко",        // прізвище
        "Марія",            // ім'я
        "Олександрівна"     // по батькові
    );
    
    vkladnyk2.pokazatyRahunok();                         // показ всієї інформації
    
    // Демонстрація поліморфізму
    cout << "\n" << string(50, '-') << endl;
    cout << "\n5. Демонстрація поліморфізму:" << endl;
    
    Rahunok* polimorfnyVkazivnyk = &vkladnyk2;          // вказівник базового класу на об'єкт похідного
    polimorfnyVkazivnyk->pokazatyRahunok();             // викликається перевизначений метод
    polimorfnyVkazivnyk->vstanovytyDodatkoviVidsotky(1.5);
    polimorfnyVkazivnyk->pererahuvaty();
    
    cout << "\n" << string(50, '-') << endl;
    cout << "\n6. Завершення програми:" << endl;
    
    // Звільнення пам'яті
    delete rahunok1;      // виклик деструктора базового класу
    delete vkladnyk1;     // виклик деструкторів похідного і базового класів
    // vkladnyk2 знищиться автоматично при завершенні програми
    
    cout << "\nПрограма завершена успішно!" << endl;
    return 0;
}