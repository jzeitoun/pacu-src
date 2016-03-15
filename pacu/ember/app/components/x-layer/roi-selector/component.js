import Ember from 'ember';
import computed from 'ember-computed-decorators';
import ROI from '../roi/roi';

export default Ember.Component.extend({
  tagName: 'svg',
  @computed() interimROIs() { return []; },
  mouseDown({offsetX, offsetY}) {
    const roi = ROI.fromPoint(offsetX, offsetY);
    const [originX, originY] = [offsetX, offsetY];
    this.get('interimROIs').pushObject(roi);
    this.$().on('mousemove.roi-selector', ({offsetX, offsetY}) => {
      roi.initialExpand(offsetX, offsetY);
    });
    Ember.$(document).one('mouseup.roi-selector', ({offsetX, offsetY}) => {
      this.$().off('mousemove.roi-selector');
      this.get('interimROIs').removeObject(roi); // anyway
      if (!(originX === offsetX && originY === offsetY)) {
        this.attrs.onExportROI(roi);
      }
    });
  },
});
