import Ember from 'ember';

export default Ember.Component.extend({
  actions: {
    acquire: function() {
      const self = this;
      this.wsx.invoke('acquire').then(function(data) {
        if (data.error) {
          alert(data.detail);
        } else {
          self.setFeature(data.detail);
        }
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
