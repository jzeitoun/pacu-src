import Ember from 'ember';

export default Ember.Route.extend({
  model(/*params, transition*/) {
    const model = this.modelFor('trj-analysis');
    return Ember.$.getJSON(`/api/json/trj/index/${model.id}`);
  }
});
