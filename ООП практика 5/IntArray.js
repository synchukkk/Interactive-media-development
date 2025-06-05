// Клас для роботи з масивом цілих чисел
class IntArray {
    constructor(arr) {
        this.arr = arr;
    }

    // Метод для знаходження числа, отриманого перемноженням позитивних елементів масиву менших 10
    productOfPositiveLessThan10() {
        let product = 1;
        let found = false;
        for (let num of this.arr) {
            if (num > 0 && num < 10) {
                product *= num;
                found = true;
            }
        }
        return found ? product : 0;
    }
}

// Приклад використання
const arr = new IntArray([2, -3, 5, 12, 8, 0, 11, 7]);
console.log('Добуток позитивних елементів менших 10:', arr.productOfPositiveLessThan10());
