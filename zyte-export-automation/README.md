

# Automated Testing using PHP

## Installation and Setup

You will need to install Java on your machine for Selenium. You can follow [this link](https://java.com/en/download/help/download_options.html) on how to install Java for your OS.

## Selenium

You will need to download the Selenium WebDriver for the browsers that you want to use for automation. You can find them in the links below. Be sure to download the version that matches the version of the browser you have installed.

- [Chrome](https://chromedriver.chromium.org/downloads)
- [Firefox](https://github.com/mozilla/geckodriver/releases)
- [Internet Explorer](https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver)
- [Microsoft Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

Last thing is to download the latest [Selenium Server (Grid)](https://www.selenium.dev/downloads/).

## PHP Setup

1. Run the command below in your terminal to install composer and other dependencies.

    ```sh
    composer install
    ```
    If you don't have PHP or composer installed on your machine, you can check [this link](https://thecodedeveloper.com/install-composer-windows-xampp/) on how to set everything up for Windows.
    
2. Rename `.env.example` into `.env` or copy it and then rename it into `.env` file.
    ```sh
    SELENIUM_SERVER_URL=http://localhost:4444/wd/hub
    ZYTE_USERNAME=your@email.com
    ZYTE_PASSWORD=yourpassword
    GOOGLE_EMAIL=your@email.com
    GOOGLE_PASSWORD=yourpassword
    ```

## Running the tests

1. To run the tests, you must first start the Selenium server grid with the command below.

    ```sh
    java -jar path/to/selenium-server-standalone-version-x.xxx.jar
    ```

    Make sure to replace the `path/to/selenium-server-standalone-version-x.xxx.jar` with the real directory where your Selenium server is located.

2. Run the command below to run PHPUnit.

    ```sh
    ./vendor/bin/phpunit --testdox --colors --exclude-group ignore App/
    ```

3. Wait for the automated test to be finished.

## PHPUnit Documentation

You can check out the [PHPUnit documentation](https://phpunit.readthedocs.io/en/9.5/writing-tests-for-phpunit.html) to know all kinds of things about PHPUnit and how to write simple and complex tests.