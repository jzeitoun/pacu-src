import Ember from 'ember';
import { on } from 'ember-computed-decorators';

export default Ember.Component.extend({
  classNames: 'ui compact dropdown',
  @on('didInsertElement') initialize() {
    const self = this;
    this.$().dropdown({
      onChange(value, text, /*$choice*/) {
        self.attrs.value.update(parseFloat(value));
      }
    });
  },
  @on('willDestroyElement') dnitialize() {
    this.$().dropdown('destroy');
  }
});
