import Ember from 'ember';

export default Ember.Component.extend({
  classNames: 'ui fluid search selection dropdown',
  initSUI: function() {
    const self = this;
    this.$().dropdown({
      onChange(value/*, text, $choice*/) { // value is index
        self.attrs.value.update(value);
        const item = self.getAttr('items').get(value);
        self.attrs.item.update(item);
      }
    });
    Ember.run.scheduleOnce('afterRender', () => {
      const value = self.getAttr('value'); // is index
      self.$().dropdown('set selected', value);
    });
  }.on('didInsertElement'),
  dnitSUI: function() {
    this.$().dropdown('destroy');
  }.on('willDestroyElement'),
  valuePath: 'name'
});
