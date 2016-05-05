import Ember from 'ember';

export default Ember.Route.extend({
  model: function() {
    return this.store.findAll('analysis');
  },
  actions: {
    didTransition() {
      this.controllerFor('application').set(
        'current-feature', 'Image Stack Analysis Sessions');
    },
  }
});
