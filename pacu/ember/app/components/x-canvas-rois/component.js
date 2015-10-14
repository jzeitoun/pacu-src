import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  actions: {
    destroyROI(roi) {
      this.attrs.onMouseUpDownSamePoint(roi);
    },
    refreshROI(roi) {
      this.attrs.onMouseUp(roi);
    }
  },
  tagName: 'svg',
  attributeBindings: ['width', 'height'],
  mouseDown({offsetX, offsetY}) {
    const self = this;
    const roi = self.attrs.onMouseDown(offsetX, offsetY);
    if (Ember.isNone(roi)) { return; }
    self.$().on('mousemove', ({offsetX, offsetY}) => {
      roi.setProperties({x2: offsetX, y2: offsetY});
    });
    Ember.$(document).one('mouseup', () => {
      self.$().off('mousemove');
      if (roi.x1 === roi.x2 && roi.y1 === roi.y2) {
        self.attrs.onMouseUpDownSamePoint(roi);
      } else {
        self.attrs.onMouseUp(roi);
      }
    });
  }
});
