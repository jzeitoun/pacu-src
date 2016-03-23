import Ember from 'ember';

export default Ember.Component.extend({
  classNames: 'ui search selection dropdown',
  classNameBindings: ['nofluid::fluid'],
  initSUI: function() {
    const self = this;
    this.$().dropdown({
      onChange(value/*text, $choice*/) { // value is index
        debugger
        const enumvalue = parseInt(value);
        const item = self.getAttr('items').get(enumvalue);
        if (Ember.isNone(self.attrs.onChange)) {
          self.attrs.value.update(enumvalue);
          if (Ember.isPresent(self.attrs.item)) {
            self.attrs.item.update(item);
          }
        } else {
          self.attrs.onChange(enumvalue);
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
    this.present(parseInt(index));
  }.observes('attrs.value'),
  dnitSUI: function() {
    this.$().dropdown('destroy');
  }.on('willDestroyElement'),
  valuePath: null //'name'
});
