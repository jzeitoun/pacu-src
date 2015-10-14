import Ember from 'ember';

export default Ember.Route.extend({
  model: function(params) {
    const entities = this.modelFor('analysis').entities;
    const model = entities.findBy('id', parseInt(params.id));
    if (Ember.isNone(model)) {
      throw 'there is no model like that.';
    }
    return model;
  },

  actions: {
    error: function(/*error, transition*/) {
      // const thrown = error;
      // debugger
      // Manage your errors
      // Ember.onerror(error);
      // substate implementation when returning `true`
      return true; // so it goes into '.session-error` route.
    }
  }
});
