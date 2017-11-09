<?php 
use PHPUnit\Framework\TestCase;
use SomLabs\Intercoop\Packaging as packaging;
use SomLabs\Intercoop\Crypto as crypto;
use Symfony\Component\Yaml\Yaml;


class KeyRingMock {
	function __construct($keymap) {
		$this->keymap = $keymap;
	}
	public function get($key) {
		if (array_key_exists($key, $this->keymap))
			return $this->keymap[$key];

		return null;
	}
}

class PackagingTest extends PHPUnit_Framework_TestCase{

	protected $keyfile = "testkey.pem";
	protected $pubfile = "testkey-public.pem";

	const YAML_SAMPLE = <<<EOT
intercoopVersion: '1.0'
originpeer: testpeer
origincode: 666
name: Perico de los Palotes
address: Percebe, 13
city: Villarriba del Alcornoque
state: Albacete
postalcode: '01001'
country: ES
EOT;


	public function assertExceptionMessage($e, $expected) {
		$this->assertEquals($expected, $e->getMessage());
	}

	public function setUp() {
		//crypto::generateKeys($this->keyfile, $this->pubfile);
		$this->key = crypto::loadKey($this->keyfile);
		$this->public = crypto::loadKey($this->pubfile);

		$this->values = Yaml::parse(self::YAML_SAMPLE);
		// yaml sorts by key so lets dump it again
		$this->yaml = Yaml::dump($this->values);
		$this->encodedPayload1 = crypto::encode($this->yaml);
		$this->signedPayload1 = crypto::sign($this->key, $this->yaml);
		$this->keyring = new KeyRingMock(array(
			'testpeer' => $this->public,
			));
	}

	public function test_generate() {
		$message = packaging::generate($this->key, $this->values);
		
		$this->assertEquals(
			Yaml::parse($message),
			array(
				'intercoopVersion' => '1.0',
				'signature' => $this->signedPayload1,
				'payload' => $this->encodedPayload1,
			));
	}

	public function setupMessage(array $overrides=array()) {
		$defaults = [
			'values' => null,
			'yaml' => null,
			'signedyaml' => null,
			'payload' => null,
			'removedFromMessage' => array(),
			'version' => null,
			];

		extract(array_merge($defaults, array_intersect_key($overrides, $defaults)));

		if (!$version) $version = packaging::$protocolVersion;

		if (!$values) $values = $this->values;
		if (!$yaml) $yaml = Yaml::dump($values);
		if (!$payload) $payload = crypto::encode($yaml);
		if (!$signedyaml) $signedyaml = $yaml;


		$messageValues = array(
			'intercoopVersion' => $version,
			'signature' => crypto::sign($this->key, $signedyaml),
			'payload' => $payload,
			);
		// TODO: use array_diff($messageValues, $removedFromMessage)
		foreach ($removedFromMessage as $field)
			unset($messageValues[$field]);

		return Yaml::dump($messageValues);
	}


	public function test_parse() {
		$message = $this->setupMessage();

		$values = packaging::parse($this->keyring, $message);

		$this->assertEquals($this->values, $values);
	}

	public function test_parse_invalidSignature() {
		$message = $this->setupMessage(array(
			'signedyaml' => Yaml::dump($this->values)."\n\n"
			));

		try {
			packaging::parse($this->keyring, $message);
			$this->fail("Expected exception not thrown");
		} catch (SomLabs\Intercoop\Packaging\BadSignature $e) {
			$this->assertExceptionMessage($e,
				'Signature verification failed, untrusted content');
		}
	}

	public function test_parse_unrecognizedPeer() {
		$this->values['originpeer'] = 'badpeer';
		$message = $this->setupMessage();

		try {
			packaging::parse($this->keyring, $message);
			$this->fail("Expected exception not thrown");
		} catch (SomLabs\Intercoop\Packaging\BadPeer $e) {
			$this->assertExceptionMessage($e,
				'The entity \'badpeer\' is not a recognized one');
		}
	}
}

// vim: noet ts=4 sw=4
