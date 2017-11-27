<?php
namespace SomLabs\Intercoop;

use Silex\Application as App;

use SomLabs\Intercoop\Crypto as crypto;
use SomLabs\Intercoop\Packaging as packaging;

class Portal extends App {
    //config var
    private $rootDir;
    private $env;

    //class var
    private $name;
    private $peerid;
    private $key;
    //private $peers;
    //private $users;

    public function __construct($name,$peerid,$keyfile) {
        parent::__construct();
        $app = $this;
        $this->rootDir=__DIR__.'/../';
        $this->env='prod';

        $this->name = $name;
        $this->peerid = $peerid;
        $this->key = crypto::loadKey($keyfile);
        //$this->peers = $peers;
        //$this->users = $users;        

        //import configuration resources/config/prod.php file
        $configFile = sprintf('%sresources/config/%s.php', $this->rootDir, $this->env);
        if (!file_exists($configFile)) {
            throw new \RuntimeException(sprintf('The configuration file "%s" does not exist.', $configFile));
        }
        require $configFile;     
       

        //  |-----------------|
        //  |      routes     |
        //  |-----------------|

        $app->get('/', [$this, 'index'])->bind('index');

        $app->error(function (\Exception $e, Request $request, $code) use ($app) {
            if ($app['debug']) {
                return;
            }
            // 404.html, or 40x.html, or 4xx.html, or error.html
            $templates = array(
                'errors/'.$code.'.html.twig',
                'errors/'.substr($code, 0, 2).'x.html.twig',
                'errors/'.substr($code, 0, 1).'xx.html.twig',
                'errors/default.html.twig',
            );
            return new Response($app['twig']->resolveTemplate($templates)->render(array('code' => $code)), $code);
        });
    }

        //  |-----------------|
        //  |    functions    |
        //  |-----------------|

    public function index (App $app) {        
        $title="titol";       
        return $app['twig']->render('index.html.twig', array('title' => $title,'name' => $this->name));
    }

}
