import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.reopenClass({
  positionalParams: ['polygon']
}).extend({
  tagName: 'polygon',
  attributeBindings: ['points'],
  @computed('attrs.polygon.@each.{x,y}') points(pg) {
    if (Ember.isNone(pg)) { return; }
    return pg.map(point => { return `${point.x},${point.y}`; }).join(' ');
  },
  mouseDown({offsetX, offsetY, metaKey}) {
    const [originX, originY] = [offsetX, offsetY];
    if (metaKey) {
      console.log('clone roi');
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
        if (metaKey) {
          this.attrs.onCancelROI();
        } else {
          this.staticClick();
        }
      } else { // polygon moved!
        this.attrs.onRefreshROI();
      }
    });
  },
  staticClick() {
    // consider using to avoid redundant action wiring
    // this.get('targetObject').send()
    this.attrs.onExclusiveToggleROI();
  }
});
