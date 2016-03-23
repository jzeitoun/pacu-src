import Ember from 'ember';

function update(object) {
  this.$(`input[type="radio"][id="${object.filterName}"]`).attr('checked', true);
}

export default Ember.Component.extend({
  initialize: function() {
    const self = this;
    const object = this.get('object');
    update.call(this, object);
    this.$().on('click.filter-component', 'input[type="number"]', function() {
      $(this).parent().parent().find('input[type="radio"]').click();
    });
    this.$().on('change.filter-component', 'input[type="radio"]', function() {
      object.set('filterName', $(this).attr('id'));
    });
  }.on('didInsertElement'),
  dnitialize: function() {
    this.$().off('click.filter-component');
    this.$().off('change.filter-component');
  }.on('willDestroyElement')
});
