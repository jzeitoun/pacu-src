import ModalSupport from 'pacu/components/x-modal-for-generic-object/modal-support';

export default Ember.Object.extend(ModalSupport, {
  // ModalSupport Implementation
  headerIcon: 'settings',
  headerText: 'Filter',
  approveText: 'Confirm',
  cancelText: 'Cancel',
  component: 'x-trj-analysis/filter',
  //
  getme: function() {
    window.qwe = this;
  }.on('init'),
  filterName: null,
  activePassValue: null,
  passivePassValue: null,
  // for initialization
  modal: null,
  route: null,
  // event
  onApprove: function() {
    this.route.send('updateFilter', this);
  }
});
