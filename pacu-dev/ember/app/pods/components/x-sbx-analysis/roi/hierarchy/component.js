import Ember from 'ember';
import computed, { on, observes } from 'ember-computed-decorators';
import color from 'pacu/utils/color';

export default Ember.Component.extend({
  classNames: 'ui stackable inverted menu',
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
  fullNameChanged: Ember.observer('toggleROIs', function() {
    // deal with the change
    console.log('test');
  }),
  @observes('roi.active') activityChanged(/*active*/) {
    if (this.get('roi.active')) {
      this.element.scrollIntoViewIfNeeded();
    }
  }
});
