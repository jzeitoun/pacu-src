import Ember from 'ember';
import { on } from 'ember-computed-decorators';

export default Ember.Component.extend({
  @on('didInsertElement') initialize() {
    this.$('.ui.dropdown').dropdown()
  },
  actions: {
    updateMidPoint(cx, cy, altKey) {
      const cxOK = 0 <= cx && cx <= 100;
      const cyOK = 0 <= cy && cy <= 100;
      return cxOK && cyOK;
    }
  },
}).reopenClass({
  positionalParams: ['model']
});
