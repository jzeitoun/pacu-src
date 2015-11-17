import Ember from 'ember';

export default Ember.Component.extend({
  classNames: 'ui search selection dropdown',
  classNameBindings: ['nofluid::fluid'],
  initSUI: function() {
    const self = this;
    window.ff = this;
    this.$().dropdown({
      onChange(value/*text, $choice*/) { // value is index
        const item = self.getAttr('items').get(value);
        if (Ember.isNone(self.attrs.onChange)) {
          self.attrs.value.update(value);
          if (Ember.isPresent(self.attrs.item)) {
            self.attrs.item.update(item);
          }
        } else {
          self.attrs.onChange(value);
        }
      }
    });
  }.on('didInsertElement'),
  present: function(index) {
    const $item = this.$().dropdown('get item', index);
    if (!$item) { return; }
    const content = $item.clone().contents();
    this.$().dropdown('set text', content);
  },
  valueChanged: function() {
    const index = this.getAttr('value');
    this.present(index);
  }.observes('attrs.value'),
  dnitSUI: function() {
    this.$().dropdown('destroy');
  }.on('willDestroyElement'),
  valuePath: null //'name'
});
