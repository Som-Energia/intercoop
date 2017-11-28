<?php 
use PHPUnit\Framework\TestCase;
use SomLabs\Intercoop\Test\AssertThrows;
use SomLabs\Intercoop\Packaging as packaging;
use SomLabs\Intercoop\Crypto as crypto;
use SomLabs\Intercoop\KeyRing;
use Symfony\Component\Yaml\Yaml;

class PackagingTest extends TestCase{

	use AssertThrows;

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


	public function setUp() {
		//crypto::generateKeys($this->keyfile, $this->pubfile);
		$this->key = crypto::loadKey($this->keyfile);
		$this->public = crypto::loadKey($this->pubfile);

		$this->values = Yaml::parse(self::YAML_SAMPLE);
		// yaml sorts by key so lets dump it again
		$this->yaml = Yaml::dump($this->values);
		$this->encodedPayload1 = crypto::encode($this->yaml);
		$this->signedPayload1 = crypto::sign($this->key, $this->yaml);
		$this->keyring = new KeyRing(array(
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

	public function assertParserRaises($message, $exceptionClass, $errorMessage) {
		$this->assertThrows(function() use($message) {
			packaging::parse($this->keyring, $message);
		},
			$exceptionClass,
			$errorMessage
		);
	}

	public function test_parse_invalidSignature() {
		$message = $this->setupMessage(array(
			'signedyaml' => Yaml::dump($this->values)."\n\n"
			));
		$this->assertParserRaises($message,
			SomLabs\Intercoop\Packaging\BadSignature::class,
			'Signature verification failed, untrusted content');
	}

	public function test_parse_unrecognizedPeer() {
		$this->values['originpeer'] = 'badpeer';
		$message = $this->setupMessage();

		$this->assertParserRaises($message,
			SomLabs\Intercoop\Packaging\BadPeer::class,
			'The entity \'badpeer\' is not a recognized one');
	}

	public function test_parse_missingPeerField() {
		unset($this->values['originpeer']);
		$message = $this->setupMessage();

		$this->assertParserRaises($message,
			SomLabs\Intercoop\Packaging\MissingField::class,
			'Required field \'originpeer\' missing on the payload');
	}

	public function test_parse_badYaml() {
		$message = $this->setupMessage(array(
			'yaml' => "\t"
			));

		$this->assertParserRaises($message,
			SomLabs\Intercoop\Packaging\BadFormat::class,
			"Error while parsing message as YAML:\n".
			"A YAML file cannot contain tabs as indentation".
			" at line 1 (near \"\t\").");
	}

	public function test_parse_missingPayload() {
		$message = $this->setupMessage(array(
			'removedFromMessage' => ['payload']
			));
		$this->assertParserRaises($message,
			SomLabs\Intercoop\Packaging\BadMessage::class,
			'Malformed message: missing payload');
	}

	public function test_parse_missingSignature() {
		$message = $this->setupMessage(array(
			'removedFromMessage' => ['signature']
			));
		$this->assertParserRaises($message,
			SomLabs\Intercoop\Packaging\BadMessage::class,
			'Malformed message: missing signature');
	}

	public function test_parse_wrongVersion() {
		$message = $this->setupMessage(array(
			'version' => '0.0'
			));
		$this->assertParserRaises($message,
			SomLabs\Intercoop\Packaging\WrongVersion::class,
			'Wrong protocol version, expected 1.0, received 0.0');
	}

	public function test_parse_missingVersion() {
		$message = $this->setupMessage(array(
			'removedFromMessage' => ['intercoopVersion']
			));
		$this->assertParserRaises($message,
			SomLabs\Intercoop\Packaging\BadMessage::class,
			'Malformed message: missing intercoopVersion');
	}

	public function test_parse_badContainerYaml() {
		$message = "\t";
		$this->assertParserRaises($message,
			SomLabs\Intercoop\Packaging\BadMessage::class,
			'Malformed message: '.
			"Error while parsing message as YAML:\n".
			"A YAML file cannot contain tabs as indentation".
			" at line 1 (near \"\t\").");
	}

	public function test_parse_payloadIsNotUtf8() {
		$message = $this->setupMessage(array(
			'payload' => 'SAFASLDFKJASLK=='
			));
		$this->assertParserRaises($message,
			SomLabs\Intercoop\Packaging\BadMessage::class,
			'Malformed message: Payload is not base64 coded UTF8');
	}

	public function TODO_test_parse_payloadIsNotBase64() {
		$message = $this->setupMessage(array(
			'payload' => 'SO'
			));
		$this->assertParserRaises($message,
			SomLabs\Intercoop\Packaging\BadMessage::class,
			'Malformed message: Payload is invalid base64: Incorrect padding');
	}



}

// vim: noet ts=4 sw=4
