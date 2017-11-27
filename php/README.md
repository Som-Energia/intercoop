Intercoop protocol PHP implementation
=====================================

Install
-------

 sudo apt-get install composer php7.0-mbstring
 composer install 

 alias phpunit='vendor/bin/phpunit'



Useful tips
-----------

After any change at the html.twig layout files you have to delete var/cache to see the changes

For executing tests type in terminal: vendor/bin/phpunit

For testing app in local: php -S localhost:8080 -t web web/index.php



