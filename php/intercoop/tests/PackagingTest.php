<?php 
use SomLabs\Intercoop\Crypto as crypto;
use PHPUnit\Framework\TestCase;

class PackagingTest extends PHPUnit\Framework\TestCase{

	public function assertExceptionMessage($e, $expected){
		$this->assertEquals($expected, $e->getMessage());
	}

	public function setUp(){
		//crypto::generateKeys($this->keyfile, $this->pubfile);
		$this->key = crypto::loadKey($this->keyfile);
		$this->public = crypto::loadKey($this->pubfile);
	}

}

// vim: noet ts=4 sw=4
