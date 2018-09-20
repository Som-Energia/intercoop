<?php
// namespace SomLabs\Intercoop\ApiClient;

// namespace SomLabs\Intercoop;

require_once('Crypto.php');
require_once('Packaging.php');
// use SomLabs\Intercoop\Crypto;
// use SomLabs\Intercoop\Packaging;

function post_request($url, $params) {
    // $query_content = http_build_query($params);
    $fp = fopen($url, 'r', FALSE, // do not use_include_path
      stream_context_create([
      'http' => [
        'header'  => [ // header array does not need '\r\n'
          'Content-type: application/yaml',
          'Content-Length: ' . strlen($params)
        ],
        'method'  => 'POST',
        'content' => $params
      ]
    ]));
    if ($fp === FALSE) {
      fclose($fp);
      return json_encode(['error' => 'Failed to get contents...']);
    }
    $result = stream_get_contents($fp); // no maxlength/offset
    fclose($fp);
    return $result;
}

class ApiClient {
  private $targetUrl;
  private $keyfile;
  
	public function __construct($apiurl, $key){
    $this->targetUrl = $apiurl;
    $this->keyfile = $key;
  }

	public function activateService($service, $personalData){
    $package = new Packaging();
    $privateKey = Crypto::loadKey($this->keyfile);
    $package = $package->generate($privateKey, $personalData);
    $response = post_request($this->targetUrl.'/activateService', $package);
    return $response;
  }
}
?>