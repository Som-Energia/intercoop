<?php 
use SomLabs\Intercoop\Crypto as crypto;
use SomLabs\Intercoop\Portal;
use SomLabs\Intercoop\Test\AssertThrows;
use PHPUnit\Framework\TestCase;
use Silex\WebTestCase;
use App\Application;

class PortalTest extends WebTestCase{
	
	private $name="Més opcions";
    private $peerid="mesopcions";
    private $key="testkey.pem";
	
	public function createApplication(){
		return new Portal(
			$this->name,
			$this->peerid,
			$this->key);
	}

	public function test_get_homepage() {
        $client = $this->createClient();
        $client->followRedirects(true);
        $crawler = $client->request('GET', '/');

        $this->assertTrue($client->getResponse()->isOk());
        $this->assertContains($this->name, $crawler->filter('body')->text());
    }
}

// vim: noet ts=4 sw=4
