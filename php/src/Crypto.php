<?php 
// namespace SomLabs\Intercoop\Crypto;

// class MessageError extends \Exception {
// 	public function __construct(...$args) {
// 		$message = sprintf($this->message, ...$args);
// 		parent::__construct($message);
// 		$this->arguments = $args;
// 	}
// }

class UnicodeError extends MessageError {
	protected $message = 'Bad UTF-8 stream';
}

// namespace SomLabs\Intercoop;

use phpseclib\Crypt\RSA;
use Ramsey\Uuid\Uuid;

class Crypto{

	/// Encode text into base64 (as text)
	static function encode($text){
		if (!\mb_check_encoding($text, 'UTF-8'))
			throw new Crypto\UnicodeError();
		return self::bencode($text);
	}

	/// Decode base64 (as text) back into text
	static function decode($b64string){
		$text = self::bdecode($b64string);
		if (!\mb_check_encoding($text, 'UTF-8'))
			throw new Crypto\UnicodeError();
		return $text;
	}

	/// Encode bytes (binary) into base64 (as text)
	static function bencode($text){
		$encoded = base64_encode($text);
		$encoded = strtr($encoded,'+/','-_'); // TODO: Untested
		return $encoded;
	}

	// Decode base64 (as text) back into bytes (binary)
	static function bdecode($b64string){
		$b64string = strtr($b64string, '-_', '+/'); // TODO: Untested
		$decoded = base64_decode($b64string);
		return $decoded;
	}

	static function sha($text){
		return sha1($text);
	}

	/// Generates a public/private key pair
	static function generateKeys($filename=null, $publicFilename=null){
		$rsa = new RSA();
		$key = $rsa->createKey(2048);
		if ($filename)
			file_put_contents($filename, $key['privatekey']);
		if ($publicFilename)
			file_put_contents($publicFilename, $key['publickey']);
		return $rsa;
	}

	static function loadKey($filename){
		$rsa = new RSA();
		$rsa->loadKey(file_get_contents($filename));
		return $rsa;
	}

	static function sign($privateKey, $text){
		if (! $privateKey->getPrivateKey())
			throw new \Exception("No private key available");

		$privateKey->setSignatureMode(RSA::SIGNATURE_PKCS1);
		$signature = $privateKey->sign($text);
		$encodedSignature = self::bencode($signature);
		return $encodedSignature;
	}

	/// 
	static function isAuthentic($publickey, $text, $signature){
		if (!$publickey->getPublicKey()) {
			throw new \Exception("No public key available");
		}
		$publickey->setSignatureMode(RSA::SIGNATURE_PKCS1);
		return $publickey->verify($text,self::bdecode($signature));
	}

	static function uuid(){
		return (string) Uuid::uuid4();
	}

}


// vim: noet ts=4 sw=4