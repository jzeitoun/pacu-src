import Ember from 'ember';
import download from 'pacu/utils/download';
import batch from 'pacu/utils/batch';

function importROIFileAllChanged(e) { // `this` is the current route
  const input = e.target;
  const route = this;
  const file = e.target.files[0];
  const fr = new FileReader();
  fr.onload = (/*e*/) => {
    const data = JSON.parse(fr.result);
    let news;
    try {
      news = data.rois;
      news.forEach(r => {
        const roi = route.store.createRecord('roi', r.attrs);
        roi.set('workspace', route.currentModel.workspace);
        roi.save();
      });
    } catch(e) {
      console.log(e);
      this.toast.warning('Invalid file');
    } finally {
      this.toast.info(`${news.length} ROI(s) imported.`);
      Ember.$(input).val(null);
    }
  }
  fr.readAsText(file);
}

function importROIFileDiffChanged(e) { // `this` is the current route
  const input = e.target;
  const route = this;
  const file = e.target.files[0];
  const fr = new FileReader();
  fr.onload = (/*e*/) => {
    const data = JSON.parse(fr.result);
    let news;
    try {
      const entry = this.currentModel.workspace.get('loadedROIs').getEach('params.cell_id').compact();
      news = data.rois.filterBy('attrs.params.cell_id').filter(roi => {
        return !entry.includes(roi.attrs.params.cell_id);
      });
      news.forEach(r => {
        const roi = route.store.createRecord('roi', r.attrs);
        roi.set('workspace', route.currentModel.workspace);
        roi.save();
      });
    } catch(e) {
      console.log(e);
      this.toast.warning('Invalid file');
    } finally {
      this.toast.info(`${news.length} ROI(s) imported.`);
      Ember.$(input).val(null);
    }
  }
  fr.readAsText(file);
}

export default {
  testalert() {
    alert('Test!');
  },
  do(/*action, ...args*/) {
    // alert('not supported');
    // return this.actions[action].apply(this, args);
  },
  willTransition: function(/*transition*/) {
    this.store.unloadAll(); // releasing all data resources. important.
    this.wsx.dnit();
    this.wsx = null;
    Ember.$('#roi-import-file-all').off('change.pacu-roi-import-all');
    Ember.$('#roi-import-file-diff').off('change.pacu-roi-import-diff');
  },
  didTransition() {
    Ember.run.schedule('afterRender', () => {
      Ember.$('#roi-import-file-all').on('change.pacu-roi-import-all', importROIFileAllChanged.bind(this));
      Ember.$('#roi-import-file-diff').on('change.pacu-roi-import-diff', importROIFileDiffChanged.bind(this));
    });
  },
  updateModel(model) {
    return model.save().then(() => {
      const name = model.constructor.modelName;
      const id = model.get('id');
      return this.toast.info(`${name} #${id} updated.`);
    });
  },
  deleteModel(model) {
    return model.destroyRecord().then(() => {
      const name = model.constructor.modelName;
      const id = model.get('id');
      return this.toast.info(`${name} #${id} deleted.`);
    });
  },
//   roiClicked(roi) {
//     this.currentModel.rois.setEach('active', false);
//     roi.set('active', true);
//   },
  exportROIs() {
    this.toast.info('Export ROIs...');
    const url = '/api/json/scanbox_manager/rois_exported';
    const name = this.currentModel.name;
    Ember.$.get(url, name).then(data => {
      const ts = +(new Date);
      download.fromByteString(data, `${ts}-${name.io}-${name.ws}-rois.json`, 'application/json');
    });
  },
  importROIsAll() {
    Ember.$('#roi-import-file-all').click();
  },
  importROIsDiff() {
    Ember.$('#roi-import-file-diff').click();
  },
  reloadTracePlot() {
    this.toast.info('Update traces...');
    this.currentModel.workspace.get('dtoverallmeans').reload();
  },
  initMPI() {
    const stream = this.currentModel.stream;
    this.set('controller.maxpBusy', true);
    stream.invoke('ch0.create_maxp').finally(() => {
      this.set('controller.maxpBusy', false);
      stream.mirror('ch0.has_maxp');
    });
  },
  overlayMPI() {
    this.toast.info('Locating max projection image...');
    this.currentModel.stream.overlayMPI();
  },
  exportMPI() {
    this.toast.info('Exporting max projection image...');
    const wid = this.currentModel.workspace.id;
    this.currentModel.stream.requestMPITiff().then(data => {
      const ts = +(new Date);
      download.fromArrayBuffer(data, `${ts}-${wid}-max-projection.tiff`, 'image/tiff');
    });
  },
  exportSFreqFitDataAsMat(roi) {
    const wid = this.currentModel.workspace.id;
    const rid = roi.id;
    const contrast = this.currentModel.workspace.get('cur_contrast');
    this.currentModel.stream.invokeAsBinary(
    'export_sfreqfit_data_as_mat', wid, rid, contrast
    ).then(data => {
      const ts = +(new Date);
      download.fromArrayBuffer(data, `${ts}-${wid}-${rid}-sfreqfit.mat`, 'application/json');
    });
  },
  exportROITracesAsMat() {
    const wid = this.currentModel.workspace.id;
    this.currentModel.stream.invokeAsBinary(
    'export_traces_as_mat', wid
    ).then(data => {
      const ts = +(new Date);
      download.fromArrayBuffer(data, `${ts}-${wid}-traces.mat`, 'application/json');
    });
  },
  computeAll() {
    const rois = this.currentModel.workspace.get('loadedROIs');
    batch.promiseSequence(rois, 'refreshAll').then(() => {
      this.toast.info('Batch process complete!');
    });
  },
  setJetCmap() {
    this.currentModel.stream.set('img.cmap', 'jet');
    this.toast.info('Colormap changed to jet.');
  },
  setGrayCmap() {
    this.currentModel.stream.set('img.cmap', 'gray');
    this.toast.info('Colormap changed to gray.');
  },
  neuropilOnAll() {
    const rois = this.currentModel.workspace.get('loadedROIs');
    batch.promiseSequence(rois, 'enableNeuropil').then(() => {
      this.toast.info('Batch process complete!');
    });
  },
  neuropilOffAll() {
    const rois = this.currentModel.workspace.get('loadedROIs');
    batch.promiseSequence(rois, 'disableNeuropil').then(() => {
      this.toast.info('Batch process complete!');
    });
  },
  neuropilRValueAll() {
    const rois = this.currentModel.workspace.get('loadedROIs');

    const factor = prompt("Please enter neuropil R value",
      this.get('neuropil_factor'));
    const fFactor = parseFloat(factor);
    if (isNaN(fFactor)) {
      this.get('toast').warning(`Invalid value ${factor}.`);
    } else {
      rois.setEach('neuropil_factor', fFactor);
      batch.promiseSequence(rois, 'save').then(() => {
        this.toast.info('Batch process complete!');
      });
    }
  },        
  //Added by RA. 
  //Listenes to state o the ROI toggle and changes a bool representing desired ROI visibility to pass to roi-manager
  changeVisibilityROIs() {
    this.controller.set('toggleROIs', !this.controller.get('toggleROIs'));
  },
  //Added by RA.
  //Responds to selecton in Display Mode dropdown and changes a bool representing if should display minimal or full features. true is minimal. 
  //Passes infor ro roi-manager. Should be updated to pass string for >2 options.
  changeModeROIs(mode){
    this.controller.set('MinModeROIs', mode);
    console.log(mode);
  },
  updateFrameShift() {
    const current = this.currentModel.workspace.get('params.frame_shift');
    const url = "https://docs.scipy.org/doc/numpy-1.12.0/reference/generated/numpy.roll.html"
    const message = `<p>Please specify an integer to pass into the function
      <a href="${url}" target="_blank">np.roll</a></p>
      <p>This will apply to an initial trace of an ROI.
         And then "recompute" will make the trace chopped along with all trials.</p>`;
    swal({
      title: 'Frame Shift',
      html: message,
      input: 'number',
      inputValue: current,
      showCancelButton: true,
      inputClass: 'ui input',
      inputValidator: function (value) {
        return new Promise(function (resolve, reject) {
          if (value && isFinite(value) && !isNaN(value)) {
            resolve()
          } else {
            reject(`Cannot send the value "${value}".`)
          }
        })
      }
    }).then(result => {
      const shift = parseInt(result);
      const ws = this.currentModel.workspace;
      const params = ws.get('params');
      ws.set('params', { ...params, frame_shift: shift});
      ws.save().then(() => {
        swal({
          type: 'success',
          title: 'Update success!',
          text: 'To take effect, recompute desired ROIs.',
        })
      });
    }).catch(swal.noop);
  }
}
