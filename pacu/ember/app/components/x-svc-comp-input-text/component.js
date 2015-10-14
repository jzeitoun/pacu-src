import Ember from 'ember';

export default Ember.Component.extend({
  classNames: 'ui inverted input',
  initSUI: function() {
    const tip = this.getAttr('meta').tooltip;
    this.$('input').popup({
      on: 'focus',
      content: tip,
      variation: 'inverted'
    });
  }.on('didInsertElement'),
  dnitSUI: function() {
    this.$('input').popup('destroy');
  }.on('willDestroyElement')
});
