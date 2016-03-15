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
      this.toast.info(`Data imported successfully.
        Click "New Session" to setup your first analysis.`);
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
    newSession(record) {
      swal({
        title: "New session...",
        text: "Provide a unique session name.",
        customClass: "sci-analyses",
        type: "input",
        showCancelButton: true,
        closeOnConfirm: false,
        animation: "slide-from-top", 
        inputPlaceholder: "Alphanumeric characters including underscore..."
      }, function(inputValue){
        if (inputValue === false) return false;
        if (inputValue === "") {
          swal.showInputError("Please provide a name.");
          return false;
        }
        const path = record.package.path;
        const session = inputValue;
        const prom = Ember.$.post('/api/json/scanimage/session', {path, session});
        prom.then(data => {
          const pkg = JSON.parse(data);
          Ember.set(record, 'package', pkg);
          swal.close();
        }).fail(err => {
          swal('Opps...', err.responseText, "error");
        });
      });
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
    },
    removeSession(record, session) {
      swal({
        title: "Are you sure?",
        text: "You will not be able to undo this!",
        type: "warning",
        showCancelButton: true,
        closeOnConfirm: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
      }, () => {
        const prom = Ember.$.ajax({
          url: '/api/json/scanimage/session',
          type: 'DELETE',
          data: {
            session: session.path,
            path: record.package.path
          }
        });
        prom.then(data => {
          Ember.set(record, 'package', JSON.parse(data));
          swal.close();
        }).fail(err => {
          swal('Opps...', err.responseText, "error");
        });
      });
    },
    openSession(record, session) {
      this.transitionTo('sci-analysis',
        this.currentModel.year,
        this.currentModel.month,
        this.currentModel.day,
        record.mouse, record.name, session.name
      );
    }
  },
  on_sse_print: function(msg, err) {
    if (10 == msg.charCodeAt() || 32 == msg.charCodeAt()) { return; }
    this.controller.messages.pushObject({body: msg});
  },
});
