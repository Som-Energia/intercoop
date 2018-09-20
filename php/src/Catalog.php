<?php
namespace SomLabs\Intercoop\Catalog;

class MessageError extends \Exception {
	public function __construct(...$args) {
		$message = sprintf($this->message, ...$args);
		parent::__construct($message);
		$this->arguments = $args;
	}
}

class KeyNotExists extends MessageError {
	protected $message = 'Given key not exists';
}

namespace SomLabs\Intercoop;

use SomLabs\Intercoop\ApiClient;

class Catalog {
    public $peers_obj;
    private $users_obj;
    private $keyfile;
    
	public function __construct($keyfile, $peers, $users){
		if(file_exists($keyfile)){
			$this->peers_obj = $peers;
			$this->users_obj = $users;
            $this->keyfile = $keyfile;
		}else{
			throw new Catalog\KeyNotExists("The given key does not exists");
		}
	}

	public function activate($peer, $service, $user){
        // fields = self.requiredFields(peer, service)
		// data = self.users.getFields(user, fields)
		$peerData = ($this->peers_obj)->getPeer($peer);
		$data = ($this->users_obj)->getData($user);
        $api = new ApiClient($peerData['targetUrl'], $this->keyfile);
        $continuationUrl = $api->activateService($service, $data);
        return $continuationUrl;
    }
}
?>