using System;
using System.Threading;

class Program
{
    static int[] numbers = new int[10];
    static int sum = 0;
    static int product = 1;

    static void Main()
    {
        Random rand = new Random();
        for (int i = 0; i < numbers.Length; i++)
        {
            numbers[i] = rand.Next(0, 26);
        }
        Console.WriteLine("Масив: " + string.Join(", ", numbers));

        Thread t0 = new Thread(SumElements);
        Thread t1 = new Thread(ProductElements);

        t0.Start();
        t1.Start();

        t0.Join();
        t1.Join();

        Console.WriteLine($"Сума: {sum}");
        Console.WriteLine($"Добуток: {product}");
    }

    static void SumElements()
    {
        sum = 0;
        foreach (int n in numbers)
        {
            sum += n;
        }
    }

    static void ProductElements()
    {
        product = 1;
        foreach (int n in numbers)
        {
            product *= n;
        }
    }
}
