import Ember from 'ember';

export default Ember.Route.extend({
  model() {
    return this.modelFor('application');
  },
  actions: {
    didTransition() {
      this.controllerFor('application').set(
        'current-feature', '');
    }
  }
});
