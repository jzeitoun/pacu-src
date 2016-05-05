import Ember from 'ember';

export default Ember.Component.extend({
  refresh: function() {
    const self = this;
    const type = this.getAttr('type');
    $.getJSON(`/api/condsearch/${type}`).then(function(data) {
      self.set('model', data);
    });
  }.observes('attrs.type'),
  actions: {
    selectID: function(condition) {
      this.attrs.selected.update(condition.id);
      $('#close-conditions-browser').click();
    }
  }
});
