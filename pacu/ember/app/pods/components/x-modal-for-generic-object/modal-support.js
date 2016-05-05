import Ember from 'ember';

export default Ember.Mixin.create({
  // optional
  headerIcon: '',
  headerText: '',
  approveText: 'OK',
  cancelText: null,
  onApprove: function() {},
  onDeny: function() {},
  // mandatory
  component: null,
  checkInterface: function() {
    if (Ember.isNone(this.get('component'))) {
      throw new Error('Component name should not be null.');
    }
  }.on('init')
});
