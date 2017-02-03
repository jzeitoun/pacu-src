import Ember from 'ember';

export default Ember.Route.extend({
  model(/*params*/) {
    const years = this.modelFor('sci-analyses.years');
    return Ember.$.getJSON(`/api/json/scanimage/index/${years.year}`);
  }
});
