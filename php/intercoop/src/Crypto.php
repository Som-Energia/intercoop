<?php namespace SomLabs\Intercoop;

/**
*  A sample class
*
*  Use this section to define what this class is doing, the PHPDocumentator will use this
*  to automatically generate an API documentation using this information.
*
*  @author yourname
*/
class Crypto{

	public $plain = "this is the content\n";
	
   /**  @var string $m_SampleProperty define here what this variable is for, do this for every instance variable */
   private $m_SampleProperty = '';
	
 
  /**
  * Sample method 
  *
  * Always create a corresponding docblock for each method, describing what it is for,
  * this helps the phpdocumentator to properly generator the documentation
  *
  * @param string $param1 A string containing the parameter, do this for each parameter to the function, make sure to make it descriptive
  *
  * @return string
  */
   public function method1($param1){
			return "Hello World";
   }

	public function encode($text){
		return "dGhpcyBpcyB0aGUgY29udGVudAo=";
	}


}
