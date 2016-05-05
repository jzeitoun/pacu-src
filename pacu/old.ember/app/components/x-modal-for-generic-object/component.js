import Ember from 'ember';
import ModalSupport from 'pacu/components/x-modal-for-generic-object/modal-support';

export default Ember.Component.extend({
  classNames: 'ui basic modal',
  initSUI: function() {
    this.$().modal({
      observeChanges: true, // dynamic DOM change
      transition: 'fade up',
      closable: false,
      onShow: () => { },
      onApprove: () => { this.get('object').onApprove(); },
      onDeny: () => { this.get('object').onDeny(); },
      onHidden: () => { this.set('object', null); },
      dimmerSettings: {
        opacity: 0.75
      }
    });
  }.on('didInsertElement'),
  updateModal: function() {
    if (Ember.isNone(this.get('object'))) { return; }
    this.$().modal('show');
  }.observes('object'),
}).reopenClass({
  positionalParams: ['object']
});
