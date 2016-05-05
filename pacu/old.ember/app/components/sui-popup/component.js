import Ember from 'ember';

export default Ember.Component.extend({
  offset: 0,
  position: 'left center',
  classNames: 'ui popup',
  initSUI: function() {
    const sel = this.get('selector');
    Ember.$(sel).popup({
      popup: this.$(),
      position: this.get('position'),
      offset: this.get('offset')
    });
  }.on('didInsertElement')
});
