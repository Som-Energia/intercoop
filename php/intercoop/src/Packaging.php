<?php 
namespace SomLabs\Intercoop\Packaging;

class MessageError extends \Exception {
	public function __construct(...$args) {
		$message = sprintf($this->message, ...$args);
		parent::__construct($message);
	}
}

class BadSignature extends MessageError {
	protected $message = 'Signature verification failed, untrusted content';
}
class BadPeer extends MessageError {
	protected $message = 'The entity \'%s\' is not a recognized one';
}

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
		$signature = $package['signature'];
		$valuesYaml = crypto::decode($payload);
		$values = Yaml::parse($valuesYaml);
		$peer = $values["originpeer"];

		$pubkey = $keyring->get($peer);
		if (is_null($pubkey))
			throw new Packaging\BadPeer($peer);

		if (!crypto::isAuthentic($pubkey, $valuesYaml, $signature))
			throw new Packaging\BadSignature();
		return $values;
	}

}


// vim: noet ts=4 sw=4
