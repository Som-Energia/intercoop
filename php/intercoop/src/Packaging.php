<?php 
namespace SomLabs\Intercoop;

use SomLabs\Intercoop\Crypto as crypto;
use Symfony\Component\Yaml\Yaml;

class Packaging {

	# TODO: take it from somewhere else
	public static $protocolVersion = '1.0';

	static function generate($ownKey, $data) {
		$payload = Yaml::dump($data);
		$result = array(
			'intercoopVersion' => self::$protocolVersion,
			'payload' => crypto::encode($payload),
			'signature' => crypto::sign($ownKey, $payload),
		);
		return Yaml::dump($result);
	}

	static function parse($keyring, $message) {
		$package = Yaml::parse($message);
		$payload = $package['payload'];
		$valuesYaml = crypto::decode($payload);
		$values = Yaml::parse($valuesYaml);
		return $values;
	}

}


// vim: noet ts=4 sw=4
