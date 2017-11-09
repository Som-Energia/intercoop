<?php 
use SomLabs\Intercoop\Crypto as crypto;


class CryptoUnicodeTest extends CryptoTest{

	protected $plain = "ñáéíóúç\n";
	protected $base64 = "w7HDocOpw63Ds8O6w6cK";
	protected $shahex = '7d426ba2a4c4820ab2c16465da66fabec9ae7527';
	protected $signed = (
		"H-4O0KH70jaYshXHcmROBZW09wCpsHb_gbaCrmnxbm3pdV3XYDRwLkY_YmPTab".
		"TizhImcwMCFO-MI4d9dQprS-tbb28hx5xlxZhHhYusSoTkDqMgjjPLBD_WjNvh".
		"aLc2FnRtYwiq4Mk6_OC94wD_zWlrMmAhPE7mQvLROSj1f9s-2HF3gtpfz2qfVo".
		"rwfQR5NfuMVbsuNSEBlgVSUytjShmGLwNIjAQHLVZCrGe5T3oSieHVD1rq2W5n".
		"TC_veaatz7M8UZ5UeqfcS-bzISA0mvOVfeuNZ4UkEgGMGtz7SMCps6qVIyN3UN".
		"iyWKxUpB0Pswa4Xj-iXSk1Po3GnfQWJQ=="
		);
}

// vim: noet ts=4 sw=4
