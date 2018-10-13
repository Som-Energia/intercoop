<?php 
namespace SomLabs\Intercoop\UserInfo;

class MessageError extends \Exception {
	public function __construct(...$args) {
		$message = sprintf($this->message, ...$args);
		parent::__construct($message);
		$this->arguments = $args;
	}
}

class DatadirNotExists extends MessageError {
	protected $message = 'Given datadir not exists';
}

namespace SomLabs\Intercoop;

use SomLabs\Intercoop\Crypto as crypto;
use SomLabs\Intercoop\KeyRing;
use Symfony\Component\Yaml\Yaml;
use Symfony\Component\Yaml\Exception as YamlException;


class UserInfo {
	
	private $users=array();

	public function __construct($datadir){		
		if(file_exists($datadir)){
			$userFiles= scandir($datadir);
			foreach ($userFiles as $user) {
				if(is_file($datadir.'/'.$user)){
					try {
						$temp=Yaml::parse(file_get_contents($datadir."/".$user));				
					    $this->user[$temp['userid']] = $temp;
					} catch (ParseException $e) {
					    printf("Unable to parse YAML file: %s", $e->getMessage());
					}						
				}
			}
		}else{
			throw new UserInfo\DatadirNotExists("The given datadir of users does not exists");
		}
	}

	public function constructor($datadir){

	}

	//get array of all peers
	public function getUsers(){
		return $this->users;
	}

	//get array of a specific peer
	public function getUser($user){
		$users = array();
        foreach ($this->users as $key => $value) {
            $users[]=$key;
        }
        if(!in_array($user,$users)){
            throw new \Exception(sprintf('User %d does not exist', $user));
        }
		return $this->users[$user];
	}

	//parse yaml formatted user
	public function getData($user){
		return Yaml::parse($user);
	}

}


// vim: noet ts=4 sw=4
