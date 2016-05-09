import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  tagName: 'circle',
  classNameBindings: ['attrs.point.moving:moving'],
  attributeBindings: ['cx', 'cy', 'r'],
  cx: Ember.computed.alias('attrs.point.x'),
  cy: Ember.computed.alias('attrs.point.y'),
  r: 2,
  mouseDown({offsetX, offsetY, altKey}) {
    const [originX, originY] = [offsetX, offsetY];
    if (altKey) {
      var curPoint = this.getAttr('point');
      var newPoint = this.attrs.onClone(curPoint);
    }
    const xLayer = this.parentView.parentView.parentView.element;
    Ember.$(xLayer).on('mousemove.circle', ({offsetX, offsetY}) => {
      this.set('attrs.point.x', offsetX);
      this.set('attrs.point.y', offsetY);
    });
    Ember.$(document).one('mouseup.circle', ({offsetX, offsetY}) => {
      Ember.$(xLayer).off('mousemove.circle');
      if (originX === offsetX && originY === offsetY) {
        if (altKey) {
          this.attrs.onCancel(newPoint);
          this.attrs.onRemove(curPoint);
        }
      } else { // point was moved
        this.attrs.onRefresh();
      }
    });
  },
}).reopenClass({
  positionalParams: ['point']
});
