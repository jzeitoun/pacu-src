import Ember from 'ember';

export default Ember.Route.extend({
  model() {
    return Ember.$.get('/api/json/sparsenoise/config');
  }
});
