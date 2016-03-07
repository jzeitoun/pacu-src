import Ember from 'ember';

const modname = 'pacu.core.io.scanimage.impl';
const clsname = 'ScanimageIO'

function removePackage(record) {
  this.get('socket').create(
    this, modname, clsname, {path: record.package.path}).then(wsx => {
    wsx.invoke('remove_package').then(pkg => {
      Ember.set(record, 'package', pkg);
    }).catch(error => {
      swal({
        title: 'Remove Failed',
        text: `Please review your data. (${error.detail})`,
        type: 'error',
        allowEscapeKey: false,
        confirmButtonText: 'Okay!',
      });
    }).finally(function() {
      wsx.dnit();
    });
  });
}

function importRaw(record) {
  const $console = Ember.$('#import-progress');
  const messages = this.controller.messages;
  $console.modal('show', {closable: false});
  this.get('socket').create(
    this, modname, clsname, {path: record.package.path}).then(wsx => {
    messages.pushObject({body: 'Please wait...'});
    wsx.invoke('import_raw').then(pkg => {
      Ember.set(record, 'package', pkg);
    }).catch(error => {
      swal({
        title: 'Import Failed',
        text: `Please review your data. (${error.detail})`,
        type: 'error',
        allowEscapeKey: false,
        confirmButtonText: 'Okay!',
      });
    }).finally(function() {
      wsx.dnit();
      Ember.run.later(function() {
        $console.modal('hide');
        messages.clear();
      }, 1000);
    });
  });
}

export default Ember.Route.extend({
  socket: Ember.inject.service(),
  model() {
    const years = this.modelFor('sci-analyses.years');
    const months = this.modelFor('sci-analyses.years.months');
    const days = this.modelFor('sci-analyses.years.months.days');
    return Ember.$.getJSON(
      `/api/json/scanimage/index/${years.year}/${months.month}/${days.day}`);
  },
  setupController(controller, model) {
    this._super(controller, model);
    controller.set('messages', []);
  },
  actions: {
    didTransition() {
      this.controllerFor('application').set(
        'current-feature', 'Scanimage Data Manager');
    },
    importRaw(record) {
      importRaw.call(this, record);
    },
    removePackage(record) {
      swal({
        title: "Are you sure?",
        text: "You will not be able to undo this!",
        type: "warning",
        showCancelButton: true,
        closeOnConfirm: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
      }, () => {
        removePackage.call(this, record);
      });
    }
  },
  on_sse_print: function(msg, err) {
    this.controller.messages.pushObject({body: msg});
  },
});
