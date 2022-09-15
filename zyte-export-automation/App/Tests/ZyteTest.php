<?php

use Facebook\WebDriver\WebDriverBy;
use Facebook\WebDriver\WebDriverExpectedCondition;
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

class ZyteTest extends BaseTest
{
  public function test_zyte_login(): void
  {
    $expectedTitle = 'MissFire ∙ Zyte';
     
    // Zyte Url
    $this->webDriver->get("https://www.zyte.com/"); 

    $this->webDriver->manage()->window()->maximize(); 

    $login = $this->webDriver->findElement(WebDriverBy::id('link-219-454'));

    if ($login) {
      $login->click();
    }
    $this->webDriver->wait(10, 1000)->until(
      WebDriverExpectedCondition::visibilityOfElementLocated(WebDriverBy::id('id_username'))
    );

    $username = $this->webDriver->findElement(WebDriverBy::id('id_username'));
    $password = $this->webDriver->findElement(WebDriverBy::id('id_password'));
    if ($username && $password) {
      $username->sendKeys($_ENV['ZYTE_USERNAME']);
      $password->sendKeys($_ENV['ZYTE_PASSWORD']);
      
      $password->submit();
    }
    $this->webDriver->wait(10, 1000)->until(
      WebDriverExpectedCondition::titleIs($expectedTitle)
    );
    $this->assertEquals($expectedTitle, $this->webDriver->getTitle()); // Assert that the title matches our $expectedTitle
    
    $urls = [
      'https://app.zyte.com/p/486986/2/30/items',
      'https://app.zyte.com/p/486986/1/28/items'
    ];
    foreach ($urls as $key => $url) {
      if ($key > 0) {
        $this->webDriver->newWindow();
      }
      $this->webDriver->get($url);
      
      $this->webDriver->wait(10, 1000)->until(
        WebDriverExpectedCondition::visibilityOfElementLocated(WebDriverBy::id('dropdown-button-2'))
      );
      $exportBtn = $this->webDriver->findElement(
        WebDriverBy::id('dropdown-button-2')
      );
      $exportBtn->click();
      $exportCsv = $this->webDriver->findElement(
        WebDriverBy::cssSelector('#dropdown-button-2 + div ul > li:nth-child(2) > a')
      );
      sleep(3);
      $exportCsv->click();
    }
  
    while (count(glob($this->exportDir  . '.\\*')) < count($urls)) {
      sleep(2);
    }
    $this->sendMail();
    $this->webDriver->quit();
  }

  public function sendMail() {
    $currentDate = date("m-d_H-i");
    $email = $_ENV["GOOGLE_EMAIL"];
    $password = $_ENV["GOOGLE_PASSWORD"];
    $recipientList = [
      "fol@crafttec.ai",
      "ool@crafttec.ai",
      "rsa@crafttec.ai",
      "hossy@imentor.dk",
      "rovie@crafttec.ai",
    ];
    $username = "Fresca Joyce Olila";
    $msg = "";
    $mail = new PHPMailer(true);
    $mail->isSMTP();
    $mail->SMTPOptions = [
      'ssl' => [
        'verify_peer' => false,
        'verify_peer_name' => false,
        'allow_self_signed' => true
      ]
    ];
    // SMTPDebug turns on error display message
    // $mail->SMTPDebug = 3;
    $mail->SMTPSecure = 'tls';
    $mail->Host = 'smtp.gmail.com';

    // Set a port
    $mail->Port = 587;
    $mail->SMTPAuth = true;

    // Set login detail for gmail account
    $mail->Username = $email;
    $mail->Password = $password;
    $mail->CharSet = 'utf-8';

    // Set subject
    $mail->setFrom($email, $username);
    foreach ($recipientList as $val) {
      $mail->addAddress($val);
    }
    $mail->addReplyTo($email, $username);

    // Cleanup
    foreach(glob($this->exportDir  . '.\\*') as $file) {
      if (is_file($file)) {
        $mail->addAttachment($file, basename($file));
      }
    }
    $mail->IsHTML(true);
    $mail->Subject = "Zyte Report for ${currentDate}";
    $mail->Body = "Hi Beautiful and Amazing People,
    <br /><br />This is generated through Automation Zyte report for ${currentDate}.<br /><br />
    Best Regards,<br /><br />Fresca Joyce Olila";
    if (!$mail->send()) {
      $msg .= "There is an error in sending Mail: " . $mail->ErrorInfo;
    } else {
      $msg .= "Email has sent successfully";
    }
    echo "${msg}\n\n";
  }
}