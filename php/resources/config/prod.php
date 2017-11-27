<?php

// configure your app for the production environment
use Silex\Provider\DoctrineServiceProvider;
use Silex\Provider\FormServiceProvider;
use Silex\Provider\HttpCacheServiceProvider;
use Silex\Provider\HttpFragmentServiceProvider;
use Silex\Provider\MonologServiceProvider;
use Silex\Provider\SecurityServiceProvider;
use Silex\Provider\ServiceControllerServiceProvider;
use Silex\Provider\SessionServiceProvider;
use Silex\Provider\TranslationServiceProvider;
use Silex\Provider\TwigServiceProvider;
use Silex\Provider\ValidatorServiceProvider;
use Silex\Provider\WebProfilerServiceProvider;

use Symfony\Component\Security\Core\Encoder\PlaintextPasswordEncoder;
use Symfony\Component\Security\Http\Authentication\AuthenticationUtils;
use Symfony\Component\Translation\Loader\YamlFileLoader;
use Symfony\Component\Yaml\Yaml;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

$app['twig.path'] = array(__DIR__.'/../templates');
$app['twig.options'] = array('cache' => __DIR__.'/../var/cache/twig');
$app['var_dir'] = $this->rootDir.'/var';
$app['locale'] = 'ca';  
$app->register(new FormServiceProvider());
$app->register(new HttpCacheServiceProvider());
$app->register(new HttpFragmentServiceProvider());
$app->register(new ServiceControllerServiceProvider());
$app->register(new SessionServiceProvider());
$app->register(new ValidatorServiceProvider());
$app->register(new TranslationServiceProvider());
$app['translator'] = $app->extend('translator', function ($translator, $app) {
    $translator->addLoader('yaml', new YamlFileLoader());
    $translator->addResource('yaml', $this->rootDir.'/resources/translations/ca.yml', 'ca');
    return $translator;
});  
$app->register(new TwigServiceProvider(), array(
    'twig.options' => array(
        'cache' => $app['var_dir'].'/cache/twig',
        'strict_variables' => true,
    ),
    'twig.path' => array($this->rootDir.'/resources/templates'),
));

$app['twig'] = $app->extend('twig', function ($twig, $app) {
    // add custom globals, filters, tags, ...
    return $twig;
});
