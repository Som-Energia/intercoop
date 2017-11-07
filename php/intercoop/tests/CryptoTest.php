<?php 
use SomLabs\Intercoop as crypto;
$crypto = new SomLabs\Intercoop\Crypto;
  

class CryptoTest extends PHPUnit_Framework_TestCase{

	public $plain = "this is the content\n";
	public $base64 = "dGhpcyBpcyB0aGUgY29udGVudAo=";
	public $signed = (
        "AxmEUIQBd82wC4-9Jm337gWbvMapcLMVvE3Ord9wvnFmvuMUW7qzO-uI8Iac".
        "rW6uPWM-93g9Y6q2YjfeQCZl_JB7lJorY5PLgSXhvu0-TcCPFkaIEAh7-4Tl".
        "lQx_-hwoN1Q3REOy-pB12iJZf9XrrOejfGG83kqXmXElSeS5RAWKwt2FcJFL".
        "IZIRZ9CDHRvX31428YURv-HlmpklwBE_t6WSJmc-b4dCcTDKih-eJ3OteDvM".
        "csN_0H76uzEZTbJf3GwH8m5lCjNkWKVufBP_J2aQ-LvtgKiuyZI6lP9TcffV".
        "da9k4vdM2zoPDtGTAxZQz68suevbGbAM_fYnBge2FA=="
        );
	
	public function test_encode_unicode(){
		$encoded = crypto\encode($this->plain);
        	$this->assertEquals($this->base64, $encoded);		
	}
  
}
