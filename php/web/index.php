<?php

use SomLabs\Intercoop\PeerInfo as peerinfo;
use SomLabs\Intercoop\UserInfo as userinfo;

ini_set('display_errors', 1);

require_once __DIR__.'/../vendor/autoload.php';

//$app = require __DIR__.'/../src/app.php';
//require __DIR__.'/../config/prod.php';
//require __DIR__.'/../src/portalexample.php';
//$app->run();

$portal = new SomLabs\Intercoop\Portal(
	"Més opcions",
	"mesopcions",
	"testkey.pem"//,
	//peerinfo::PeerInfo('instance/somillusio/peers'),
    //userinfo::UserInfo('instance/somillusio/users'),
);
$portal->run();
