#!/bin/bash
composer update
java -jar selenium-server-standalone-3.141.59.jar &
./vendor/bin/phpunit --testdox --colors --exclude-group ignore App/