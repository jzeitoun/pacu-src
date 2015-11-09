import Ember from 'ember';

export default Ember.Route.extend({
  actions: {
    getFocused() {
      this.fullscreen.toggle();
    },
  },
  model() {
    return Ember.RSVP.hash({
      //platform: Ember.$.getJSON('api/ping/platform')
      platform: {
        system: 'system',
        node: 'node',
        release: 'release',
        machine: 'machine',
        processor: 'processor',
      }
    });
  },
  toast: Ember.inject.service(),
  deferredSetup: function() {
    this.toast.options.positionClass = 'toast-top-center';
    this.toast.preventDuplicates = false;
    this.toast.timeOut = '5000';
  }.on('init')
});
