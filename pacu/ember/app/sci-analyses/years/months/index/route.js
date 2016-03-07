import Ember from 'ember';

export default Ember.Route.extend({
  model() {
    const years = this.modelFor('sci-analyses.years');
    const months = this.modelFor('sci-analyses.years.months');
    return Ember.$.getJSON(`/api/json/scanimage/index/${years.year}/${months.month}`);
  }
});
