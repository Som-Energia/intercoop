<?php


ini_set('display_errors', 1);

require_once __DIR__.'/../vendor/autoload.php';

//$app = require __DIR__.'/../src/app.php';
//require __DIR__.'/../config/prod.php';
//require __DIR__.'/../src/portalexample.php';
//$app->run();

$portal = new SomLabs\Intercoop\Portal('prod');
$portal->run();
