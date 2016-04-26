import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  tagName: 'svg',
  classNameBindings: ['active:showup:hidden'],
  active: false,
  x: null,
  y: null,
  mouseMove({offsetX, offsetY}) {
    this.set('x', offsetX);
    this.set('y', offsetY);
  },
  click() {
    this.set('active', false);
  },
  @computed('x', 'y') pointAvailable(x, y) { return x && y; }
});
