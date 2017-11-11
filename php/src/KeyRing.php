<?php 
namespace SomLabs\Intercoop\KeyRing;

class MessageError extends \Exception {
	public function __construct(...$args) {
		$message = sprintf($this->message, ...$args);
		parent::__construct($message);
		$this->arguments = $args;
	}
}

class NotFound extends MessageError {
	protected $message = "Entity not found '%s'";
}


namespace SomLabs\Intercoop;

use phpseclib\Crypt\RSA;

class KeyRing {

	public function __construct(array $keys) {
		$this->keys = $keys;
	}

	public function get(string $key) : RSA {
		if (!isset($this->keys[$key]))
			throw new KeyRing\NotFound($key);
		return $this->keys[$key];
	}

}


// vim: noet ts=4 sw=4
