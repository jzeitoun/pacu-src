import Ember from 'ember';
import computed from 'ember-computed-decorators';

// this.getAttr('meta');
export default Ember.Component.extend({
  tagName: 'form',
  classNames: 'ui fitted input',
  classNameBindings: ['meta.readonly:readonly:action'],
  debug: function() {
  }.on('didInsertElement'),
  @computed('meta.something') something(thing) {},
  initSUI: function() {
    this.$('input').popup({
      on: 'focus',
      inline: true
    });
  }.on('didInsertElement'),
  dnitSUI: function() {
    this.$('input').popup('destroy');
  }.on('willDestroyElement'),
  submit: function(e) {
    const meta = this.getAttr('meta');
    this.attrs.onUpdate(meta); // will return a promise?
    return false;
  }
});
