import Ember from 'ember';

export default {
  willTransition: function(transition) {
    this.wsx.dnit();
    this.wsx = null;
  },
  // upsertROI(roi, ...props) {
  //   const wid = this.currentModel.get('workspace.id');
  //   const baseProps = ['id'];
  //   const defaultProps = ['polygon', 'centroid', 'active'];
  //   baseProps.pushObjects(Ember.isEmpty(props) ? defaultProps : props);
  //   const data = roi.getProperties(...baseProps);
  //   data['workspace_id'] = wid;
  //   return this.get('wsx').invoke('session.ROI.upsert', data).then(data => {
  //     roi.setProperties(data);
  //     return roi;
  //   });
  // },
//   fetchROI(roi) {
//     if (roi.get('busy')) { return; }
//     roi.set('busy', true);
//     return this.get('wsx').invoke('make_response', roi.get('id')).gateTo(
//       this.currentModel, 'roiFetching'
//     ).then(data => {
//       roi.setProperties(data);
//       roi.setProperties({error: null});
//     }).catch(err => {
//       this.toast.error(err.title, err.detail);
//       roi.set('error', err);
//     }).finally(() => {
//       roi.set('busy', false);
//     });
//   },
//   updateAndFetchROI(roi) {
//     this.send('updateROI', roi);
//     this.send('fetchROI', roi);
//     roi.toggleProperty('active');
//   },
  // insertROI(rois, roi) {
  //   roi.set('npEnabled', false);
  //   this.actions.upsertROI.call(this, roi).then(roi => {
  //     rois.pushObject(roi);
  //   });
  // },
  // updateROI(roi) {
  //   this.actions.upsertROI.call(this, roi);
  // },
  // removeROI(rois, roi) {
  //   rois.removeObject(roi);
  //   if (Ember.isPresent(roi.id)) {
  //     this.get('wsx').invoke('session.ROI.delete', {id: roi.id});
  //   }
  // },
  // deriveROI(rois, roi) {// derive makes original ROI primitive state.
  //   return rois.pushObject(roi.derive());
  // },
  // exclToggleROI(rois, roi) { // but do not make it exclusive
  //   return;
  //   // roi.toggleProperty('active');
  //   // upsertROI.call(this, roi, 'active');
  // },
//   exclActivateROI(rois, roi) {
//     for (let one of rois) {
//       if (Em.isEqual(one, roi)) {
//         roi.set('active', true);
//         if (roi.get('invalidated')) {
//           this.send('fetchROI', roi);
//         }
//       } else {
//         one.set('active', false);
//       }
//     }
//   },
  // insertPoint(roi, point) {
  //   const newPoint = {x: point.x, y: point.y};
  //   roi.polygon.insertAt(roi.polygon.indexOf(point), newPoint);
  //   return newPoint;
  // },
  // removePoint(roi, point) {
  //   roi.polygon.removeObject(point);
  //   this.send('upsertROI', roi);
  // },
  // cancelPoint(roi, point) {
  //   roi.polygon.removeObject(point);
  // },
  // fetchTrace(roi, category) {
  //   const traces = roi.get('traces');
  //   const trace = traces.findBy('category', 'df/f0');
  //   const trace_id = trace ? trace.id : null;
  //   this.get('wsx').invoke('fetch_trace', roi.id, trace_id, category).then(data => {
  //     if (trace) {
  //       Ember.setProperties(trace, data);
  //     } else { traces.pushObject(data); }
  //   });
  // },
//   openROIModal(rois, roi) {
//     this.currentModel.set('roiOnDetail', roi);
//     Ember.run.later(this, 'send', 'exclActivateROI', rois, roi, 500);
//   },
//   openModal(genericObject) {
//     this.currentModel.set('objectForModal', genericObject);
//   },
//   updateFilter(filter) {
// 
//     swal({
//       title: "Wait...",
//       text: "After update filter variables, current session will be refreshed. OK?",
//       type: "info",
//       showCancelButton: true,
//       closeOnConfirm: true,
//       confirmButtonColor: "#DD6B55",
//       confirmButtonText: "Yes, reload!",
//     }, () => {
//       const data = {
//         filterName: filter.filterName,
//         activePassValue: filter.activePassValue,
//         passivePassValue: filter.passivePassValue
//       };
//       this.get('wsx').invoke('upsert_filter', data).then(data => {
//         location.reload();
//       });
//     });
// 
//   },
//   sfrequencyIndexChanged(index) {
//     // console.log('sfrequencyIndexChanged')
//     // this.currentModel.get('curroi');
//     // this.currentModel.get('rois').forEach(roi => roi.invalidate());
//     // this..fetch updae roi
//   },
//   nudge() {
//     return this.currentModel.incrementProperty('img.curIndex');
//   },
//   stop() {
//     Ember.run.cancel(this.pid);
//     this.pid = null;
//   },
//   play() {
//     // console.log('play!, last nudge at', this.lastDraw);
//     // const now = +(new Date())
//     // console.log('play!, now', now);
//     // const nextDraw = this.lastDraw ? 1000 : 0;
//     // console.log('play!, next nudge starts in ', nextNudge);
//     this.pid = Ember.run.later(() => {
//       const max = this.currentModel.get('img.maxIndex');
//       const cur = this.currentModel.get('img.curIndex');
//       if (cur >= max) {
//         this.currentModel.set('img.curIndex', 0);
//       } else {
//         this.send('nudge');
//         this.send('play');
//       }
//     }, 1000/7.5);
//   },
//   // drawInterval: 1000
  saveModel(model) {
    return model.save();
  },
  deleteModel(model) {
    return model.destroyRecord();
  },
  duplicateROI(roi) {
    return this.store.createRecord('roi', {
      workspace: this.currentModel.workspace,
      polygon: roi.get('polygon')
    }).save();
  },
  appendROI(payload={}) {
    payload['workspace'] = this.currentModel.workspace;
    return this.store.createRecord('roi', payload);
  },
  fetchTrace(t) {
    return this.get('wsx').invoke('fetch_trace', t.get('id')).gateTo(
      this.currentModel, 'roiFetching'
    ).then(data => {
      t.reload();
    }).catch(err => {
      this.toast.error(err.title, err.detail);
    }).finally(() => {
    });
  },
  do(action, ...args) {
    return this.actions[action].apply(this, args);
  },
  rotateFocus() {
    const registry = Ember.getOwner(this
          ).__container__.lookup('-view-registry:main');
    const rs = Ember.$('.focus-responder');
    const focused = rs.filter('.fr-focused');
    const fIndex = rs.index(focused);
    const curr = Ember.$(rs.get(fIndex));
    const next = Ember.$(rs.get(fIndex+1));
    const v = registry[next.attr('id')];
    Ember.run.once(() => {
      curr.removeClass('fr-focused').trigger('focusedOut');
      next.addClass('fr-focused').trigger('focusedIn');
      Ember.set(this.currentModel, 'focused', v);
    });
  },
  revokeFocus() {
    Ember.$('.fr-focused').removeClass('fr-focused').trigger('focusedOut');
    Ember.set(this.currentModel, 'focused', null);
  },
  locateFocus(v) {
    if (this.get('currentModel.focused') === v) { return; }
    Ember.$('.fr-focused').removeClass('fr-focused').trigger('focusedOut');
    v.$().addClass('fr-focused').trigger('focusedIn');
    Ember.set(this.currentModel, 'focused', v);
    return true;
  },
  hitFocus() {
    const v = this.get('currentModel.focused');
    if (v) {
      v.$().trigger('focusHit');
    }
  },
  noop() { console.log('noop', ...arguments); },
}
