import Ember from 'ember';

function upsertROI(roi) {
  const data = roi.getProperties('guessParams', 'centroid',
    'bootstrap_sf',
    'vectors', 'polygon', 'neuropil', 'id', 'invalidated', 'npEnabled');
  return this.get('wsx').invoke('upsert_roi', data).then(data => {
    roi.setProperties(data);
  }).catch(err => {
    this.toast.error(err.detail);
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
  fetchROI(roi, heavy=false) {
    if (roi.get('busy')) { return; }
    const msg = `Fetching ROI ${roi.get('id')}`
    this.get('currentModel.logs').pushObject(Ember.Object.create({body: msg}));
    roi.set('busy', true);
    return this.get('wsx').invoke('update_responses', roi.get('id'), heavy).gateTo(
      this.currentModel, 'roiFetching'
    ).then(data => {
      roi.setProperties(data);
      roi.setProperties({error: null});
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
  updateAndFetchROI(roi) {
    this.send('updateROI', roi);
    this.send('fetchROI', roi);
    roi.toggleProperty('active');
  },
  fetchAllROIs(rois) {
    for (let roi of rois) {
      this.send('fetchROI', roi, true);
    }
  },
  removeROI(rois, roi) {
    rois.removeObject(roi);
    if (Ember.isPresent(roi.id)) {
      this.get('wsx').invoke('session.roi.remove', roi.id);
    }
  },
  deriveROI(rois, roi) {// derive makes original ROI primitive state.
    return rois.pushObject(roi.derive());
  },
  exclToggleROI(rois, roi) {
    for (let one of rois) {
      if (Em.isEqual(one, roi)) {
        if (roi.toggleProperty('active')) {
          if (one.get('invalidated')) {
            this.send('fetchROI', roi);
          }
        }
      } else {
        one.set('active', false);
      }
    }
  },
  exclActivateROI(rois, roi) {
    for (let one of rois) {
      if (Em.isEqual(one, roi)) {
        roi.set('active', true);
        if (roi.get('invalidated')) {
          this.send('fetchROI', roi);
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
  },
  openROIModal(rois, roi) {
    window.roi = roi;
    this.currentModel.set('roiOnDetail', roi);
    Ember.run.later(this, 'send', 'exclActivateROI', rois, roi, 500);
  },
  openModal(genericObject) {
    this.currentModel.set('objectForModal', genericObject);
  },
  sfrequencyIndexChanged(index) {
    this.get('wsx').invoke('set_sfrequency_index', index).then(data => {
      const roi = this.currentModel.get('curROI');
      // this.currentModel.get('rois').forEach(roi => roi.invalidate());
      if (Ember.isPresent(roi)) {
        roi.set('active', true);
        // this.send('fetchROI', roi);
      }
    });
  },
  colormapIndexChanged(index) {
    const xmid = this.currentModel.get('xmid');
    const ymid = this.currentModel.get('ymid');
    const name = this.currentModel.get('colormaps')[index];
    this.currentModel.set('cmap', name);
    console.log(name, xmid, ymid);
    this.send('updateColormap', name, xmid, ymid);
  },
  updateSoGInitialGuessForThisSF(roi, params, sfreq) {
    const guessParams = roi.getWithDefault('guess_params', {});
    guessParams[sfreq] = params;
    roi.set('guessParams', guessParams);
    this.send('updateAndFetchROI', roi);
  },
  updateSoGInitialGuessForAllSF(roi, params) {
    const guessParams = roi.getWithDefault('guess_params', {});
    for (let resp of roi.get('sortedResponses')) {
      guessParams[resp.sfreq] = params;
    }
    roi.set('guessParams', guessParams);
    this.send('updateAndFetchROI', roi);
  },
  updateColormap(mapName, xmid, ymid) {
    const p = this.get('wsx').invoke('channel.update_colormap', mapName, xmid, ymid);
    return p.then(data => {
      this.currentModel.indexChanged();
    }).catch(err => {
      this.toast.error(err.detail);
    });
  },
  invalidateTrajectory(roi) {
    roi.set('invalidated', true);
    upsertROI.call(this, roi);
  },
  exportAllAnova(roi) {
    const lines = [];
    for (let rep of roi.anova_all.matrix) {
      lines.push(rep.join('\t'));
    }
    const joined = lines.join('\n');
    swal({
      title: "Please CTRL+A and CTRL+C yourself. (Blank -> Flicker -> Oris)",
      text: `<textarea>${joined}</textarea>`,
      html: true
    });

  }
}
