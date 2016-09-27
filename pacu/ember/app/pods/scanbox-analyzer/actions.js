import Ember from 'ember';

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
  importROIs() {
    // this.toast.info('Reload datatags...');
    // this.currentModel.workspace.get('dtoverallmeans').reload();
  },
}
