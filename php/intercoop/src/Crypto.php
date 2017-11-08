<?php 
namespace SomLabs\Intercoop;

class Crypto{

	/// Encode text into base64 (as text)
	static function encode($text){
		return base64_encode($text);
	}

	/// Decode base64 (as text) back into text
	static function decode($b64string){
		return base64_decode($b64string);
	}

	static function sha($text){
		return sha1($text);
	}
}


// vim: noet ts=4 sw=4
