import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  @computed('elementId') eventName(eid) {
    return `keydown.${eid}`;
  },
  initialize: function() {
    this.$(document).on(this.get('eventName'), e => {
      if (e.target.tagName === "INPUT") { return; }
      const tabIndex = e.keyCode - 49;
      this.send('activateTab', tabIndex);
    });
  }.on('didInsertElement'),
  dnitialize: function() {
    this.$(document).off(this.get('eventName'));
  }.on('willDestroyElement'),
  actions: {
    activateTab(index) {
      const tabs = this.$('> div');
      const tab = tabs.get(index);
      if (tab) {
        tabs.removeClass('active');
        tab.classList.add('active');
      }
    }
  }
});
