import Ember from 'ember';

export default Ember.Component.extend({
  actions: {
    acquire: function() {
      this.wsx.invoke('acquire').then(function(data) {
        alert(data);
      });
    }
  },
  socket: Ember.inject.service(),
  initWS: function() {
    window.asd = this;
    const self = this;
    this.wsx = this.get('socket').create(
      this, 'pacu.core.svc.andor', 'AndorBindingService', this.getAttr('src')
    ).then(function() {
      self.wsx.access('features').then(self.setFeatures);
    });
  }.on('didInsertElement'),
  dnitWS: function() { this.wsx.dnit(); }.on('willDestroyElement'),
  setFeatures(features) {
    this.set('features', features);
  },
});
