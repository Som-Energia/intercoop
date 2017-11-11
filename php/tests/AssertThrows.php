<?php

namespace SomLabs\Intercoop\Test;

trait AssertThrows {

	public function assertThrows($callable, $exceptionClass, $message) {
		try {
			$callable();
			$this->fail("Expected exception not thrown");
		} catch (\Exception $e) {
			print(get_class($e)." vs ".$exceptionClass);
			if (get_class($e) != $exceptionClass) throw $e;
			$this->assertEquals($message, $e->getMessage());
		}
	}

}




