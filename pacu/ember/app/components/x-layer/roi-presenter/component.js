import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'svg',
  actions: {
    insertPoint(roi, point) {
      const newPoint = {x: point.x, y: point.y};
      roi.polygon.insertAt(roi.polygon.indexOf(point), newPoint);
      return newPoint;
    },
    removePoint(roi, point) {
      roi.polygon.removeObject(point);
      this.send('updatePoint', roi);
    },
    cancelPoint(roi, point) {
      roi.polygon.removeObject(point);
    },
    updatePoint(roi) {
      this.attrs.onUpdateROI(roi);
    },
    removeROI(rois, roi) {
      rois.removeObject(roi);
    },
    exclusiveToggleROI(rois, roi) {
      for (let one of rois) {
        if (Em.isEqual(one, roi)) {
          if (one.toggleProperty('active')) {
            this.set('curROI', one);
          } else {
            this.set('curROI', null);
          }
        } else {
          one.set('active', false);
        }
      }
    },
  }
});
