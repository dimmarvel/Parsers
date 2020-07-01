using System;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;

namespace ParserAutoDromRu
{
    class Program
    {
        static void Main(string[] args)
        {
            IWebDriver driver = new ChromeDriver();

            int i = 1;
            while (i < 100)
            {
                driver.Url = "https://auto.drom.ru/all/page" + i++ + "/";
                var cars = driver.FindElements(By.CssSelector(@"a[data-ftid=bulls-list_bull]"));
                foreach (var car in cars)
                {
                    var carName = car.FindElement(By.CssSelector(@"span[data-ftid=bull_title]")).Text;
                    var carPrice = car.FindElement(By.CssSelector(@"span[data-ftid=bull_price]")).Text;
                    Console.WriteLine("Car (name = {0}, price = {1})", carName, carPrice);
                }
            }
            


        }
    }
}
