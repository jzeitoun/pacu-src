import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
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
  this.route('andor');
  this.route('andor', function() {
    this.route('device', { path: ':index' });
  });
});

export default Router;
