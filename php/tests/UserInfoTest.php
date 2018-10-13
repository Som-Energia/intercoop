<?php 
use SomLabs\Intercoop\UserInfo;
use SomLabs\Intercoop\Test\AssertThrows;
use PHPUnit\Framework\TestCase;

class UserInfoTest extends TestCase{

	use AssertThrows;

	private $datadir = "instance/somillusio/users/";

	public function test_datadir_invalid(){			
		$this->assertThrows(function() {
			$users = new UserInfo('ffhf');			
		},
			SomLabs\Intercoop\UserInfo\DatadirNotExists::class,
			"Given datadir not exists"
		);
	}

	

}

// vim: noet ts=4 sw=4
