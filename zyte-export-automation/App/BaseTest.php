<?php 
require 'vendor/autoload.php';

use PHPUnit\Framework\TestCase;
use Facebook\WebDriver\Remote\DesiredCapabilities;
use Facebook\WebDriver\Remote\RemoteWebDriver;
use Facebook\WebDriver\Chrome\ChromeOptions;

class BaseTest extends TestCase
{
  protected $exportDir;

  protected $webDriver;
  
  /**
   * Stuff that need to be setup before running the tests should go here.
   *
   * @return void
   */
  public function setUp(): void
  {    

    $dotenv = Dotenv\Dotenv::createImmutable(dirname(__DIR__, 1));
    $dotenv->load();

    $capabilities    = DesiredCapabilities::chrome(); // Use Chrome for automated test
    $chromeOptions   = new ChromeOptions();

    $this->exportDir = dirname(__DIR__, 1) . '\\zyte_export';

    // Cleanup
    foreach(glob($this->exportDir  . '.\\*') as $file) {
      if (is_file($file)) {
        // Delete Files
        unlink($file);
      }
    }

    $prefs = [
      'download.default_directory' => $this->exportDir
    ];
    $chromeOptions->setExperimentalOption('prefs', $prefs);
    // $chromeOptions->addArguments(['--headless']);
    $capabilities->setCapability(ChromeOptions::CAPABILITY, $chromeOptions);
    $this->webDriver = RemoteWebDriver::create($_ENV['SELENIUM_SERVER_URL'], $capabilities);
  }
  
  /**
   * Stuff that need to be executed after the tests have run should go here.
   *
   * @return void
   */
  // public function tearDown(): void
  // {
  //   $this->webDriver->quit(); // Stop webDriver after tests have run
  // }
  
  /**
   * A simple test that doesn't really do 
   * anything to avoid warnings for this file
   *
   * @return void
   * @group ignore
   */
  public function test_base_setup(): void
  {
    $this->markTestSkipped('Setup for BaseTest class');
  }
}
