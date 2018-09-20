<?php 
// namespace SomLabs\Intercoop\PeerInfo;

// class MessageError extends \Exception {
// 	public function __construct(...$args) {
// 		$message = sprintf($this->message, ...$args);
// 		parent::__construct($message);
// 		$this->arguments = $args;
// 	}
// }

class DatadirNotExists extends MessageError {
	protected $message = 'Given datadir not exists';
}

// namespace SomLabs\Intercoop;

require_once('Crypto.php');
// use SomLabs\Intercoop\Crypto as crypto;
// use SomLabs\Intercoop\KeyRing;
use Symfony\Component\Yaml\Yaml;
use Symfony\Component\Yaml\Exception as YamlException;

class PeerInfo {
	
	private $peers=array();

	public function __construct($datadir){		
		if(file_exists($datadir)){
			$peerFiles= scandir($datadir);
			foreach ($peerFiles as $peer) {
				if(is_file($datadir.'/'.$peer)){	
					try {
						$temp=Yaml::parse(file_get_contents($datadir."/".$peer));				
					    $this->peers[$temp['peerid']] = $temp;
					} catch (ParseException $e) {
					    printf("Unable to parse YAML file: %s", $e->getMessage());
					}						
				}
			}
		}else{
			throw new PeerInfo\DatadirNotExists("The given datadir of peers does not exists");
		}
	}

	public function constructor($datadir){

	}

	//get array of all peers
	public function getPeers(){
		return $this->peers;
	}

	//get array of a specific peer
	public function getPeer($peer){
		$peers = array();
        foreach ($this->peers as $key => $value) {
            $peers[]=$key;
        }
        if(!in_array($peer,$peers)){
            throw new \Exception(sprintf('Peer %d does not exist', $peer));
        }
		return $this->peers[$peer];
	}

	//get array of a specific service from a peer
	public function getService($peer,$service){
		$peers = array();
        foreach ($this->peers as $key => $value) {
            $peers[]=$key;
        }
        if(!in_array($peer,$peers)){
            throw new \Exception(sprintf('Peer %d does not exist', $peer));
        }
        $services = array();
        foreach ($this->peers[$peer]['services'] as $key => $value) {
            $services[]=$key;           
        }
        if(!in_array($service,$services)){
            throw new \Exception(sprintf('Service %d does not exist', $service));
        }
		return $this->peers[$peer]['services'][$service];
	}

}


// vim: noet ts=4 sw=4