<?php 
use SomLabs\Intercoop\PeerInfo;
use SomLabs\Intercoop\Test\AssertThrows;
use PHPUnit\Framework\TestCase;

class PeerInfoTest extends TestCase{

	use AssertThrows;

	private $datadir = "instance/somillusio/peers/";

	public function test_datadir_invalid(){			
		$this->assertThrows(function() {
			$peers = new PeerInfo('ffhf');			
		},
			SomLabs\Intercoop\PeerInfo\DatadirNotExists::class,
			"Given datadir not exists"
		);
	}

	

}

// vim: noet ts=4 sw=4
