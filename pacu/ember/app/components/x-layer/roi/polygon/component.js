import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  tagName: 'polygon',
  attributeBindings: ['points'],
  classNameBindings: [
    'attrs.active', 'attrs.busy', 'attrs.error:error', 'attrs.invalidated'],
  @computed('attrs.polygon.@each.{x,y}') points(pg) {
    if (Ember.isNone(pg)) { return; }
    return pg.map(point => { return `${point.x},${point.y}`; }).join(' ');
  },
  mouseDown({offsetX, offsetY, altKey}) {
    const [originX, originY] = [offsetX, offsetY];
    if (altKey) {
      var derived = this.attrs.onDerive();
    }
    const polygon = this.getAttr('polygon');
    for (let point of polygon) {
      point.originX = point.x;
      point.originY = point.y;
    }
    const xLayer = this.parentView.parentView.parentView.element;
    Ember.$(xLayer).on('mousemove.polygon', ({offsetX, offsetY}) => {
      const deltaX = originX - offsetX;
      const deltaY = originY - offsetY;
      Ember.run(() => {
        for (let point of polygon) {
          Ember.set(point, 'x', point.originX - deltaX);
          Ember.set(point, 'y', point.originY - deltaY);
        }
      });
    });
    Ember.$(document).one('mouseup.polygon', ({offsetX, offsetY}) => {
      Ember.$(xLayer).off('mousemove.polygon');
      if (originX === offsetX && originY === offsetY) {
        if (altKey) {
          this.attrs.onCancel(derived);
          this.attrs.onRemove();
        } else {
          this.attrs.onStaticClick();
        }
      } else { // polygon moved!
        this.attrs.onRefresh();
      }
    });
  },
  contextMenu(e) {
    this.attrs.onRefresh();
    e.preventDefault();
  }
}).reopenClass({
  positionalParams: ['polygon']
});
