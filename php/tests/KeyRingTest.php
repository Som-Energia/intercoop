<?php 
use SomLabs\Intercoop\ApiClient as apiclient;
use SomLabs\Intercoop\Crypto as crypto;
use SomLabs\Intercoop\KeyRing as keyring;
use PHPUnit\Framework\TestCase;

trait AssertThrows {

	public function assertThrows($callable, $exceptionClass, $message) {
		try {
			$callable();
			$this->fail("Expected exception not thrown");
		} catch (Exception $e) {
			if (get_class($e) != $exceptionClass) throw $e;
			$this->assertEquals($message, $e->getMessage());
		}
	}

}

class KeyRing_Test extends PHPUnit_Framework_TestCase {

	use AssertThrows;

	protected $keyfile = "testkey.pem";
	protected $pubfile = "testkey-public.pem";

	public function setUp() {
		$this->key = crypto::loadKey($this->keyfile);
		$this->public = crypto::loadKey($this->pubfile);
	}

	public function setupKeyRing() {
		return new keyring(array(
			'akey' => $this->public,
		));
	}

	public function test_get_whenNotFound() {
		$ring = $this->setupKeyRing();

		$this->assertThrows(function() use($ring) {
			$ring->get('badkey');
		},
			keyring\NotFound::class,
			"Entity not found 'badkey'"
		);
	}

	public function test_get_exists() {
		$ring = $this->setupKeyRing();
		$key = $ring->get('akey');
		$this->assertEquals($this->public, $key);

	}

}

// vim: noet ts=4 sw=4
