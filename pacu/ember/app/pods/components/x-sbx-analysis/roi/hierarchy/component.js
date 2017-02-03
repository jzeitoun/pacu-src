import Ember from 'ember';
import computed, { on, observes } from 'ember-computed-decorators';
import color from 'pacu/utils/color';

export default Ember.Component.extend({
  classNames: 'ui small stackable inverted menu',
  attributeBindings: 'style',
  @computed('colorIndex') style(ci) {
    return Ember.String.htmlSafe(`border: 1px solid ${color.google20[ci%20]}`);
  },
  @on('didInsertElement') initSUI() {
    this.$('.dropdown').dropdown({
      on: 'hover',
      delay : {
        show: 0,
        hide: 0,
      }
    });
  },
  @observes('roi.active') activityChanged(/*active*/) {
    if (this.get('roi.active')) {
      this.element.scrollIntoViewIfNeeded();
    }
  }
});
