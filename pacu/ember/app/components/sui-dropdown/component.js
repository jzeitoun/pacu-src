import Ember from 'ember';

export default Ember.Component.extend({
  classNames: ['ui', 'floating', 'labeled', 'icon', 'dropdown', 'button', 'inverted'],
  initSUI: function() {
    this.$().dropdown(this.bindOptions(this));
    const preset = this.get('preselect');
    if (!Ember.isNone(preset)) {
      this.$(`.item:nth(${preset})`).click();
    }
  }.on('didInsertElement'),
  dnitSUI: function() {
    this.$().dropdown('destroy');
  }.on('willDestroyElement'),
  bindOptions: function(self) { return {
    onChange: function(value, text, $selectedItem) {
      const val = $selectedItem.find('>div').data('value');
      self.set('value', val);
    }
  }; }
});
