import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  classNames: 'ui search fluid selection dropdown',
  initSUI: function() {
    window.zz = this.$();
    this.$().dropdown({
      onChange: Ember.run.bind(this, 'onChange')
    });
  }.on('didInsertElement'),
  dnitSUI: function() {
    this.$().dropdown('destroy');
  }.on('willDestroyElement'),
  prompt: 'Please Select...',
  icon: 'circle thin',
  items: [],
  @computed('value') valueNone(value) {
    // Because value is 0, `if` expression in template may be confused.
    return Ember.isNone(value);
  },
  @computed('value', 'items') initialText(value, items) {
    if (Ember.isPresent(value) && Ember.isPresent(items)) {
      return items[value];
    } else {
      return this.get('prompt');
    }
  },
  onChange(value) {
    const iValue = parseInt(value);
    this.attrs.value.update(iValue);
    this.attrs.onValueChanged(iValue);
  },
});

// `value` as index is treated string index.
