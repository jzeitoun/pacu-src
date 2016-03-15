import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('psychopy', function() {
    this.route('prepare');
    this.route('configure');
    this.route('broadcast');
    this.route('review');
    this.route('review-error');
    this.route('review-loading');
    this.route('broadcast-onair');
  });
  this.route('analyses', function() {
    this.route('new');
  });
  this.route('analysis', { path: '/analysis/:analysis_id' });
  this.route('trj-analyses');
  this.route('trj-analysis', { path: '/trj-analysis/:tr-session_id' }, function() {
    this.route('trial', { path: '/trial/:index' });
  });
  this.route('andor', function() {
    this.route('device', { path: ':index' });
  });
  this.route('test-pixi');
  this.route('sci-analyses', function() {
    this.route('years', { path: '/:year' }, function() {
      this.route('months', { path: '/:month' }, function() {
        this.route('days', { path: '/:day' }, function() {
        });
      });
    });
  });
  this.route('sci-analysis',
      { path: '/sci-analysis/:year/:month/:day/:mouse/:image/:session' });
});

export default Router;
