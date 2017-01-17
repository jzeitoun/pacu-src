import Ember from 'ember';
import download from 'pacu/utils/download';

function importROIFileChanged(e) { // `this` is the current route
  const input = e.target;
  const route = this;
  const file = e.target.files[0];
  const fr = new FileReader();
  fr.onload = (e) => {
    const data = JSON.parse(fr.result);
    try {
      data.rois.forEach(r => {
        const roi = route.store.createRecord('roi', r.attrs);
        roi.set('workspace', route.currentModel.workspace);
        roi.save();
      });
    } catch(e) {
      console.log(e);
      this.toast.warning('Invalid file');
    } finally {
      this.toast.info(`${data.rois.length} ROI(s) imported.`);
      $(input).val(null);
    }
  }
  fr.readAsText(file);
}

export default {
  willTransition: function(transition) {
    this.store.unloadAll(); // releasing all data resources. important.
    this.wsx.dnit();
    this.wsx = null;
    $('#roi-import-file').off('change.pacu-roi-import');
  },
  didTransition() {
    Ember.run.schedule('afterRender', () => {
      $('#roi-import-file').on('change.pacu-roi-import', importROIFileChanged.bind(this));
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
  importROIs() {
    $('#roi-import-file').click();
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
  }
}
