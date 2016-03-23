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
  this.route('andor', function() {
    this.route('device', { path: ':index' });
  });
  // this.route('analyses', function() { this.route('new'); });
  // this.route('analysis', { path: '/analysis/:analysis_id' });
  this.route('trj-analyses', function() {
    this.route('recordings', { path: '/:recording' }, function() {
      this.route('trials', { path: '/:trial' });
    });
  });
  this.route('trj-analysis',
    { path: '/trj-analysis/:recording/:trial/:session' });
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
