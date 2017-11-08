<?php 
use SomLabs\Intercoop\Crypto as crypto;  

class CryptoTest extends PHPUnit_Framework_TestCase{

	private $plain = "this is the content\n";
	private $base64 = "dGhpcyBpcyB0aGUgY29udGVudAo=";
	private $signed = (
        "AxmEUIQBd82wC4-9Jm337gWbvMapcLMVvE3Ord9wvnFmvuMUW7qzO-uI8Iac".
        "rW6uPWM-93g9Y6q2YjfeQCZl_JB7lJorY5PLgSXhvu0-TcCPFkaIEAh7-4Tl".
        "lQx_-hwoN1Q3REOy-pB12iJZf9XrrOejfGG83kqXmXElSeS5RAWKwt2FcJFL".
        "IZIRZ9CDHRvX31428YURv-HlmpklwBE_t6WSJmc-b4dCcTDKih-eJ3OteDvM".
        "csN_0H76uzEZTbJf3GwH8m5lCjNkWKVufBP_J2aQ-LvtgKiuyZI6lP9TcffV".
        "da9k4vdM2zoPDtGTAxZQz68suevbGbAM_fYnBge2FA=="
        );
	private $shahex = "a567f5414a110729344c395089d87821310b22f4";
	

	function test_encode_unicode(){
		$encoded = crypto::encode($this->plain);
        	$this->assertEquals($this->base64, $encoded);		
	}

	function test_decode_unicode(){
		$decoded = crypto::decode($this->base64);
        	$this->assertEquals($this->plain, $decoded);		
	}

	function TODO_test_decode_incorrectBase64Padding(){
		try {
			crypto::decode("AA");
			$this->fail("Exception not thrown");
		} catch (Exception $e) {
			$this->assertEquals($e.errorMessage(), "Incorrect Padding");
		}
	}
	function TODO_test_decode_notUnicode(){
		try {
			crypto::decode("ABCD");
			$this->fail("Exception not thrown");
		} catch (Exception $e) {
			$this->assertEquals($e.errorMessage(), "Not UTF-8 unicode");
		}
	}

	function test_sha(){
		$this->assertEquals(
			crypto::sha($this->plain),
			$this->shahex);
	}


}

// vim: noet ts=4
