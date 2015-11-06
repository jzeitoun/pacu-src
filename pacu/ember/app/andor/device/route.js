import Ember from 'ember';

export default Ember.Route.extend({
  actions: {
    didTransition() {
      this.controllerFor('application').set(
        'current-feature', 'Andor Device Controller');
    },
  }
});
