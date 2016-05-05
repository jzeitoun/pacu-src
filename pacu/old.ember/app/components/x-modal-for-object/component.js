import Ember from 'ember';

export default Ember.Component.extend({
  icon: 'user',
  classNames: 'ui basic modal',
  initSUI: function() {
    this.$().modal({
      transition: 'fade up',
      closable: false,
      onShow: () => {
        Ember.run.later(() => {
          this.$('div.input:not(".disabled"):first input').focus();
        }, 800);
      },
      onApprove: () => {
        this.attrs.onApprove();
      },
      onDeny: () => {
      },
      onHidden: () => {
        this.set('object', null);
      },
      dimmerSettings: {
        opacity: 0.5
      }
    });
  }.on('didInsertElement'),
  dnitSUI: function() {}.on('willDestroyElement'),
  updateModal: function() {
    if (Ember.isNone(this.get('object'))) { return; }
    this.$().modal('show');
  }.observes('object'),
  keyDown: function(e) {
    // consider using document bubble once
    const code = e.keyCode || e.which;
    if (code == 13) {
     this.$('.approve.button').click();
    }
    if (code == 27) {
     this.$('.cancel.button').click();
    }
  }
}).reopenClass({
  positionalParams: ['object']
});
