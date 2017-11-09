<?php 
namespace SomLabs\Intercoop\Packaging;

class MessageError extends \Exception {
	public function __construct(...$args) {
		$message = sprintf($this->message, ...$args);
		parent::__construct($message);
		$this->arguments = $args;
	}
}

class BadSignature extends MessageError {
	protected $message = 'Signature verification failed, untrusted content';
}
class BadPeer extends MessageError {
	protected $message = 'The entity \'%s\' is not a recognized one';
}
class MissingField extends MessageError {
	protected $message = 'Required field \'%s\' missing on the payload';
}
class BadFormat extends MessageError {
	protected $message = "Error while parsing message as YAML:\n%s";
}

namespace SomLabs\Intercoop;

use SomLabs\Intercoop\Crypto as crypto;
use Symfony\Component\Yaml\Yaml;
use Symfony\Component\Yaml\Exception as YamlException;


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

		try {
			$values = Yaml::parse($valuesYaml);
		} catch (YamlException\ParseException $e) {
			throw new Packaging\BadFormat($e->getMessage());
		}

		if (!isset($values["originpeer"]))
			throw new Packaging\MissingField('originpeer');
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
