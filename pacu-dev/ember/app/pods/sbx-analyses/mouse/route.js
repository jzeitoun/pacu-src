import Ember from 'ember';

export default Ember.Route.extend({
  model(mouse) {
    return Ember.$.getJSON(`/api/json/scanbox/index/${mouse.mouse}`);
  },
});
