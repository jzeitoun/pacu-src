import Ember from 'ember';

export default Ember.Route.extend({
  model() {
    return Ember.$.getJSON('api/metamodule/pacu.core.andor/ember');
  },
  actions: {
    refreshModel: function() {
      this.refresh();
    }
  }
});
