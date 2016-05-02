import Ember from 'ember';

function importRaw(modname, clsname, meta) {
  const $console = Ember.$('#import-progress');
  const messages = this.controller.messages;
  $console.modal('show', {closable: false});
  this.get('socket').create(
    this, modname, clsname, {path: meta.path}).then(wsx => {
    messages.pushObject({body: 'Please wait...'});
    wsx.invoke('import_raw').then(newOne => {
      Ember.setProperties(meta, newOne);
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

function removePackage(modname, clsname, meta) {
  this.get('socket').create(
    this, modname, clsname, {path: meta.path}).then(wsx => {
    wsx.invoke('remove_io').then(newOne => {
      Ember.setProperties(meta, newOne);
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

const modname = 'pacu.core.io.scanbox.impl';
const clsname = 'ScanboxIO';

export default Ember.Route.extend({
  socket: Ember.inject.service(),
  actions: {
    importRaw(meta) {
      importRaw.call(this, modname, clsname, meta);
    },
    removePackage(meta) {
      swal({
        title: "Are you sure?",
        text: "You will not be able to undo this!",
        type: "warning",
        showCancelButton: true,
        closeOnConfirm: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
      }, () => {
        removePackage.call(this, modname, clsname, meta);
      });
    },
    newSession(meta) {
      swal({
        title: "New session...",
        text: 'Provide a unique session name. I suggest "main" as a default name.',
        customClass: "trj-analyses",
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
        const path = meta.path;
        const session = inputValue;
        const prom = Ember.$.post('/api/json/scanbox/session', {path, session});
        prom.then(data => {
          const pkg = JSON.parse(data);
          Ember.set(meta, 'sessions', pkg.sessions);
          swal.close();
        }).fail(err => {
          swal('Opps...', err.responseText, "error");
        });
      });
    },
    removeSession(io, session) {
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
          url: '/api/json/scanbox/session',
          type: 'DELETE',
          data: {
            session_id: session.id,
            path: io.path
          }
        });
        prom.then(data => {
          Ember.set(io, 'sessions', JSON.parse(data).sessions);
          swal.close();
        }).fail(err => {
          swal('Opps...', err.responseText, "error");
        });
      });
    },
    openSession(io, session) {
      this.transitionTo('sbx-analysis',
        ...io.hops.concat(session.id)
      );
    }
  },
  setupController(controller, model) {
    this._super(controller, model);
    controller.set('messages', []);
  },
  on_sse_print(msg, err) {
    if (10 == msg.charCodeAt() || 32 == msg.charCodeAt()) { return; }
    this.controller.messages.pushObject({body: msg});
  },
});
