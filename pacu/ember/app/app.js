import Ember from 'ember';
import Resolver from './resolver';
import loadInitializers from 'ember-load-initializers';
import config from './config/environment';

let App;

import Inflector from 'ember-inflector';
const inflector = Inflector.inflector;
inflector.irregular('dtanovaeach', 'dtanovaeachs');

Ember.MODEL_FACTORY_INJECTIONS = true;

App = Ember.Application.extend({
  modulePrefix: config.modulePrefix,
  podModulePrefix: config.podModulePrefix,
  Resolver,
  customEvents: {
    focusedIn: 'focusedIn',
    focusedOut: 'focusedOut',
    focusHit: 'focusHit'
  }
});

loadInitializers(App, config.modulePrefix);

export default App;
