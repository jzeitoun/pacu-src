import Ember from 'ember';
import computed, { on } from 'ember-computed-decorators';
import interaction from 'pacu/utils/interaction';
import color from 'pacu/utils/color';

export default Ember.Component.extend({
  store: Ember.inject.service(),
  tagName: 'svg',
  classNameBindings: ['augKeyOn'],
  mouseDown(e) {
    if (this.get('workspace.roisBusy')) {
      console.log('it is busy wait');
      return
    }
    const $target = this.parentView.$();
    return interaction.bindOnce.call(this, $target, e);
  },
  leaving(origin, offset, offsetY) {
    return this.get('workspace').appendROI({polygon: [
      {x: origin.x, y: origin.y},
      {x: offset.x, y: origin.y},
      {x: offset.x, y: offset.y},
      {x: origin.x, y: offset.y},
    ]});
  },
  movingWith(origin, offset, roi) {
    [['1.x', offset.x], ['2.x', offset.x],
     ['2.y', offset.y], ['3.y', offset.y]].forEach(([key, val]) => {
      roi.set(`polygon.${key}`, val);
    });
  },
  left(origin, offset, roi) {
    return roi.save().then(() => {
      const name = roi.constructor.modelName;
      const id = roi.get('id');
      return this.toast.info(`${name} #${id} created.`);
    });
  },
  poked(/* origin, offset */) {
    this.send('unfocus');
  },
  @on('didInsertElement') initialize() {
    Ember.$(document).on('keydown.roi-manager', ({altKey, metaKey}) => {
      this.set('augKeyOn', altKey || metaKey);
    });
    Ember.$(document).on('keyup.roi-manager', () => {
      this.set('augKeyOn', false);
    });
  },
  @on('willDestroyElement') dinitialize() {
    Ember.$(document).off('keydown.roi-manager');
    Ember.$(document).off('keyup.roi-manager');
  },
  @computed('workspace.rois.[]') coloredROIs(rois) {
    return rois.map((r, i) => {
      return {roi: r, color: color.getGoogle20(i)};
    });
  },
  actions: {
    unfocus() {
      this.get('workspace.rois').filterBy('active').forEach(r => {
        r.set('active', false); // r.save();
      });
    },
    focus(roi) {
      this.send('unfocus');
      roi.set('active', true); // roi.save();
    },
    dupe(roi) {
      return;
      // return this.get('workspace').appendROI({
      //   polygon: roi.get('polygon')
      // });
    }
  }
});
