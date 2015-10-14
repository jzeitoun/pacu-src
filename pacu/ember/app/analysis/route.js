import Ember from 'ember';
import ajax from 'ic-ajax';

export default Ember.Route.extend({
  actions: {
    didTransition() {
      this.controllerFor('application').set(
        'current-feature', 'Image Stack Analysis');
    },
  }
});
