<?php 
namespace SomLabs\Intercoop;

use SomLabs\Intercoop\Crypto as crypto;
use Symfony\Component\Yaml\Yaml;

class Packaging {

	# TODO: take it from somewhere else
	public static $protocolVersion = '1.0';

	static function generate($ownKey, $data){
		$payload = Yaml::dump($data);
		$result = array(
			'intercoopVersion' => self::$protocolVersion,
			'payload' => crypto::encode($payload),
			'signature' => crypto::sign($ownKey, $payload),
		);
		return Yaml::dump($result);
	}

}


// vim: noet ts=4 sw=4
