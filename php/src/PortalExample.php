<?php
require_once('vendor/autoload.php');

// use SomLabs\Intercoop\Catalog;
// use SomLabs\Intercoop\Crypto;
// use SomLabs\Intercoop\Packaging;
// use SomLabs\Intercoop\KeyRing;
// use SomLabs\Intercoop\PeerInfo;
// use SomLabs\Intercoop\UserInfo;

require_once('vendor/somlabs/intercoop/src/Catalog.php');
require_once('vendor/somlabs/intercoop/src/Crypto.php');
require_once('vendor/somlabs/intercoop/src/Packaging.php');
require_once('vendor/somlabs/intercoop/src/PeerInfo.php');
require_once('vendor/somlabs/intercoop/src/UserInfo.php'); # TODO: Implent UserInfo
// require_once('vendor/somlabs/intercoop/src/KeyRing.php'); # TODO: Implement

$keyfile = dirname(__FILE__).'/../testkey.pem';
$peers = new PeerInfo(dirname(__FILE__).'/instance/sommobilitat/peers');
$users = new UserInfo(dirname(__FILE__).'/instance/sommobilitat/users');
$catalog = new Catalog($keyfile, $peers, $users);

$peer = "sommobilitat";
$service = "newUser";
$user = "
originpeer: wordpress
email: bernat@test.com
service_type: factures
";

$uuid = $catalog->activate($peer, $service, $user);
echo $uuid;
?>