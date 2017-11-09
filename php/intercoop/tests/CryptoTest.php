<?php 
use SomLabs\Intercoop\Crypto as crypto;
use PHPUnit\Framework\TestCase;

class CryptoTest extends PHPUnit_Framework_TestCase{

	protected $plain = "this is the content\n";
	protected $base64 = "dGhpcyBpcyB0aGUgY29udGVudAo=";
	protected $signed = (
		"AxmEUIQBd82wC4-9Jm337gWbvMapcLMVvE3Ord9wvnFmvuMUW7qzO-uI8Iac".
		"rW6uPWM-93g9Y6q2YjfeQCZl_JB7lJorY5PLgSXhvu0-TcCPFkaIEAh7-4Tl".
		"lQx_-hwoN1Q3REOy-pB12iJZf9XrrOejfGG83kqXmXElSeS5RAWKwt2FcJFL".
		"IZIRZ9CDHRvX31428YURv-HlmpklwBE_t6WSJmc-b4dCcTDKih-eJ3OteDvM".
		"csN_0H76uzEZTbJf3GwH8m5lCjNkWKVufBP_J2aQ-LvtgKiuyZI6lP9TcffV".
		"da9k4vdM2zoPDtGTAxZQz68suevbGbAM_fYnBge2FA=="
		);
	protected $shahex = "a567f5414a110729344c395089d87821310b22f4";
	protected $keyfile = "testkey.pem";
	protected $pubfile = "testkey-public.pem";

	public function assertExceptionMessage($e, $expected){
		$this->assertEquals($expected, $e->getMessage());
	}

	public function setUp(){
		//crypto::generateKeys($this->keyfile, $this->pubfile);
		$this->key = crypto::loadKey($this->keyfile);
		$this->public = crypto::loadKey($this->pubfile);
	}

	public function test_encode_unicode(){
		$encoded = crypto::encode($this->plain);
		$this->assertEquals($this->base64, $encoded);
	}

	public function test_decode_unicode(){
		$decoded = crypto::decode($this->base64);
		$this->assertEquals($this->plain, $decoded);
	}

	public function TODO_test_decode_incorrectBase64Padding(){
		try {
			crypto::decode("AA");
			$this->fail("Exception not thrown");
		} catch (Exception $e) {
			$this->assertExceptionMessage($e, "Incorrect Padding");
		}
	}
	public function test_decode_notUnicode(){
		$encoded = "ABCD";
		try {
			crypto::decode($encoded);
			$this->fail("Exception not thrown");
		} catch (Exception $e) {
			$this->assertExceptionMessage($e, "Not UTF-8 unicode");
		}
	}

	public function test_encode_notUnicode(){
		$binary = "\x00\x01\x83";
		try {
			crypto::encode($binary);
			$this->fail("Exception not thrown");
		} catch (Exception $e) {
			$this->assertExceptionMessage($e,"Not UTF-8 unicode");
		}
	}

	public function test_bencode() {
		$binary = "\x01\x00\x02";
		$expected = "AQAC";
		$result = crypto::bencode($binary);
		$this->assertEquals($expected, $result);
	}

	public function test_bdecode() {
		$encoded = "AQAC";
		$expected = "\x01\x00\x02";
		$result = crypto::bdecode($encoded);
		$this->assertEquals($expected, $result);
	}

	public function test_sha(){
		$sha = crypto::sha($this->plain);
		$this->assertEquals($sha, $this->shahex);
	}

	public function test_sign(){
		$signature = crypto::sign($this->key, $this->plain);
		$this->assertEquals($signature, $this->signed);
	}

	public function test_sign_withNoPrivate_fails(){
		try {
			crypto::sign($this->public, $this->plain);
			$this->fail("Exception not thrown");
		} catch (Exception $e) {
			$this->assertExceptionMessage($e, "No private key available");
		}
	}

	public function test_isAuthentic_whenOk(){
		$result = crypto::isAuthentic($this->public, $this->plain, $this->signed);
		$this->assertTrue($result);
	}

	public function test_isAuthentic_whenPayloadChanged(){
		$badPayload = "this is NOT the content\n";
		$result = crypto::isAuthentic($this->public, $badPayload, $this->signed);
		$this->assertFalse($result);
	}

	public function test_isAuthentic_withNoPublic_fails(){
		$key = new phpseclib\Crypt\RSA();
		try {
			$result = crypto::isAuthentic($key, $this->plain, $this->signed);
			$this->fail("Exception not thrown");
		} catch (Exception $e) {
			$this->assertExceptionMessage($e, "No public key available");
		}
	}

	public function test_uuid(){
		$uuid = crypto::uuid();
		$this->assertRegExp(
			'/[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}/',
			$uuid);
	}
}

// vim: noet ts=4 sw=4
