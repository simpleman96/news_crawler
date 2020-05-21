package main;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.util.List;
import java.util.concurrent.TimeUnit;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        System.setProperty("webdriver.chrome.driver", "driver/chromedriver");
        ChromeOptions options = new ChromeOptions();
        options.setHeadless(true);
        WebDriver driver = new ChromeDriver(options);
        driver.manage().timeouts().implicitlyWait(5,TimeUnit.SECONDS);
        JavascriptExecutor js = (JavascriptExecutor) driver;

        driver.get("https://vtv.vn/dong-su-kien/dai-dich-covid-19-242.htm");
//        driver.get("https://edition.cnn.com/world/live-news/coronavirus-pandemic-04-28-20-intl/index.html");
//        Thread.sleep(5000);
//        List<WebElement> elements = driver.findElements(By.xpath("//*[@id=\"admWrapsite\"]/div[3]/div[3]/div[1]/ul/li/h4/a"));
        List<WebElement> elements = driver.findElements(By.className("post-headlinestyles__Header-sc-2ts3cz-0 kpNfDn"));
        System.out.println(driver.findElement(By.tagName("body")).toString());
        System.out.println("Size of elements: " + elements.size());

        long oldHeight = (Long)js.executeScript("return document.body.scrollHeight");
        System.out.println("Old height: " + oldHeight);
        js.executeScript("window.scrollTo(0, document.body.scrollHeight)");
        Thread.sleep(5000);

        long newHeight = (Long)js.executeScript("return document.body.scrollHeight");
        System.out.println("New height: " + newHeight);

        elements = driver.findElements(By.className("post-headlinestyles__Header-sc-2ts3cz-0 kpNfDn"));
//        elements = driver.findElements(By.xpath("//*[@id=\"admWrapsite\"]/div[3]/div[3]/div[1]/ul/li/h4/a"));

        System.out.println("Size of elements: " + elements.size());
    }
}
