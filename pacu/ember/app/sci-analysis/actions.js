import Ember from 'ember';

function upsertROI(roi) {
  this.get('wsx').invoke('upsert_roi', roi).then(data => {
    roi.setProperties(data);
  });
}
export default {
  didTransition() {
    this.controllerFor('application').set(
      'current-feature', 'Scanimage Data Analysis');
  },
  willTransition: function(transition) {
    this.wsx.dnit();
    this.wsx = null;
  },
  fetchROI(roi) {
    if (roi.get('busy')) { return; }
    roi.set('busy', true);
    this.get('wsx').invoke('make_response', roi).gateTo(
      this.currentModel, 'roiFetching'
    ).then(data => {
      roi.setProperties(data);
      roi.setProperties({error: null, invalidated: false});
    }).catch(err => {
      this.toast.error(err.title, err.detail);
      roi.set('error', err);
    }).finally(() => {
      roi.set('busy', false);
    });
  },
  insertROI(rois, roi) {
    upsertROI.call(this, rois.pushObject(roi));
  },
  updateROI(roi) {
    roi.invalidate();
    upsertROI.call(this, roi);
  },
  removeROI(rois, roi) {
    rois.removeObject(roi);
    this.get('wsx').invoke('remove_roi', roi);
  },
  deriveROI(rois, roi) {// derive makes original ROI primitive state.
    return rois.pushObject(roi.derive());
  },
  exclToggleROI(rois, roi) {
    for (let one of rois) {
      if (Em.isEqual(one, roi)) {
        if (one.toggleProperty('active')) {
          if (one.get('invalidated')) {
            this.send('fetchROI', one);
          }
        }
      } else {
        one.set('active', false);
      }
    }
  },
  insertPoint(roi, point) {
    const newPoint = {x: point.x, y: point.y};
    roi.polygon.insertAt(roi.polygon.indexOf(point), newPoint);
    return newPoint;
  },
  removePoint(roi, point) {
    roi.polygon.removeObject(point);
    this.send('updateROI', roi);
  },
  cancelPoint(roi, point) {
    roi.polygon.removeObject(point);
  }
}
