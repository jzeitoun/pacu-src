import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  actions: {
    activateROI(roi) {
      if (roi.get('active')) {
        this.attrs.onDeactivateROI(roi);
      } else {
        this.attrs.onActivateROI(roi);
      }
    },
    destroyROI(roi, e) {
      e.preventDefault();
      e.stopPropagation();
      this.attrs.onDestroyROI(roi);
    },
    refreshROI(roi) {
      this.attrs.onRefreshROI(roi);
    }
  },
  tagName: 'svg',
  attributeBindings: ['width', 'height'],
  mouseDown({offsetX, offsetY}) {
    const self = this;
    const roi = self.attrs.onCreateROI(offsetX, offsetY);
    if (Ember.isNone(roi)) { return; }
    self.$().on('mousemove', ({offsetX, offsetY}) => {
      roi.setProperties({x2: offsetX, y2: offsetY});
    });
    Ember.$(document).one('mouseup', () => {
      self.$().off('mousemove');
      if (roi.x1 === roi.x2 && roi.y1 === roi.y2) {
        self.attrs.onDestroyROI(roi);
      } else {
        self.attrs.onRefreshROI(roi);
      }
    });
  }
});
