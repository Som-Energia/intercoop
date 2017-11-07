<?php 
namespace SomLabs\Intercoop;

class Crypto{
	static function encode($text){
		return base64_encode($text);
	}

	static function decode($b64string){
		return base64_decode($b64string);
	}
}


