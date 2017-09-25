import Ember from 'ember';
import { on, observes } from 'ember-computed-decorators';

export default Ember.Component.extend({
  @observes('model.roi_ids')
  @on('didInsertElement') initialize() {
    const self = this;
    const ss = this.get('model.roi_ids').map(i => `${i}`);
    this.$('.ui.dropdown').dropdown('destroy').dropdown('set selected', ss).dropdown({
      onChange(value /*, text, $choice */) {
        const roi_ids = value.map(n => parseInt(n));
        const model = self.get('model');
        model.set('roi_ids', roi_ids);
      }
    });
  },
}).reopenClass({
  positionalParams: ['model']
});
