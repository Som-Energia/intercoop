<?php

namespace SomLabs\Intercoop\Test;

trait AssertThrows {

	public function assertThrows($callable, $exceptionClass, $message) {
		try {
			$callable();
			$this->fail("Expected exception not thrown");
		} catch (\Exception $e) {
			if (get_class($e) != $exceptionClass) throw $e;
			$this->assertEquals($message, $e->getMessage());
		}
	}

}




