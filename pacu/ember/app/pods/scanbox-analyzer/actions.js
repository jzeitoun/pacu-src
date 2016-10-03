import Ember from 'ember';
import download from 'pacu/utils/download';

export default {
  willTransition: function(transition) {
    this.store.unloadAll(); // releasing all data resources. important.
    this.wsx.dnit();
    this.wsx = null;
  },
  didTransition() {
    Ember.run.schedule('afterRender', () => {
      // maybe better place to init websocket & stream?
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
  roiClicked(roi) {
    this.currentModel.rois.setEach('active', false);
    roi.set('active', true);
  },
  exportROIs() {
    this.toast.info('Export ROIs...');
    const url = '/api/json/scanbox_manager/rois_exported';
    const name = this.currentModel.name;
    Ember.$.get(url, name).then(data => {
      const ts = +(new Date);
      download.fromByteString(data, `${ts}-${name.io}-${name.ws}-rois.json`, 'application/json');
    });
  },
}
