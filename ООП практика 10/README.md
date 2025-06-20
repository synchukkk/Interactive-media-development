# Паралельна обробка масиву в C#

## Опис
Ця програма демонструє використання потоків у C# для паралельної обробки масиву цілих чисел. Вона створює масив із 10 випадкових чисел у діапазоні від 0 до 25, а потім запускає два потоки:
- **T0**: Обчислює суму всіх елементів масиву.
- **T1**: Обчислює добуток всіх елементів масиву.

## Мета
- Ознайомитися з основами багатопотокового програмування в C#.
- Виявити потенційні проблеми потокобезпечності.
- Проаналізувати паралельну програму за допомогою візуалізатора паралелізму Visual Studio.

## Запуск
1. Відкрийте проект у Visual Studio.
2. Запустіть програму (`Program.cs`).
3. У консолі буде виведено масив, його суму та добуток.

## Потенційні проблеми потокобезпечності
У цьому прикладі змінні `sum` і `product` є спільними для потоків, але кожен потік працює лише зі своєю змінною, тому конфліктів не виникає. Якщо ж декілька потоків змінювали б одну й ту ж змінну, потрібно було б використовувати механізми синхронізації (наприклад, `lock`).

## Аналіз у Visual Studio
Для аналізу паралельного виконання використовуйте візуалізатор паралелізму (Concurrency Visualizer) у Visual Studio:
- Запустіть програму з профілюванням (Debug > Performance Profiler > Concurrency).
- Перегляньте графік виконання потоків та взаємодію між ними.

## Автор
- Ярослав Синчук 034
