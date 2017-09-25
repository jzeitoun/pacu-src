import Ember from 'ember';

export default Ember.Route.extend({
  model(p) {
    const mouse = this.modelFor('sbx-analyses.mouse').mouse;
    return Ember.$.getJSON(`/api/json/scanbox/index/${mouse}/${p.day}`);
  },
});
