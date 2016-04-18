import Ember from 'ember';

export default Ember.Route.extend({
  model(directory) {
    return Ember.$.getJSON(`/api/json/scanbox/index/${directory.directory}`);
  },
});
