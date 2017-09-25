import Ember from 'ember';

/* global swal */

function cat(error) {
  swal({
    title: 'Request Failed',
    text: `Please review your data. (${error.detail})`,
    type: 'error',
    allowEscapeKey: false,
    confirmButtonText: 'Okay!',
  });
}

function importRaw(modname, clsname, io) {
  const $console = Ember.$('#import-progress');
  const messages = this.controller.messages;
  $console.modal('show', {closable: false});
  this.get('socket').create(
    this, modname, clsname, {path: io.path}).then(wsx => {
    messages.pushObject({body: 'Please wait...'});
    wsx.invoke('import_raw').then(newOne => {
      Ember.setProperties(io, newOne);
      this.toast.info(`Data imported successfully.
        Click "New Session" to setup your first analysis.`);
    }).catch(cat).finally(function() {
      wsx.dnit();
      Ember.run.later(function() {
        $console.modal('hide');
        messages.clear();
      }, 1000);
    });
  });
}

function removeImported(modname, clsname, io) {
  this.get('socket').create(
    this, modname, clsname, {path: io.path}).then(wsx => {
    wsx.invoke('remove_io').then(newOne => {
      Ember.setProperties(io, newOne);
    }).catch(cat).finally(function() {
      wsx.dnit();
    });
  });
}

const modname = 'pacu.core.io.scanbox.impl';
const clsname = 'ScanboxIO';

export default Ember.Route.extend({
  socket: Ember.inject.service(),
  actions: {
    importRaw(io) {
      importRaw.call(this, modname, clsname, io);
    },
    removeImported(io) {
      swal({
        title: "Are you sure?",
        text: "You will not be able to undo this!",
        type: "warning",
        showCancelButton: true,
        closeOnConfirm: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
      }, () => {
        removeImported.call(this, modname, clsname, io);
      });
    },
    upgradeDBSchema(io) {
      this.get('socket').create(
        this, modname, clsname, {path: io.path}).then(wsx => {
        wsx.invoke('upgrade_db_schema').then(newIO => {
          Ember.setProperties(io, newIO);
        }).catch(cat).finally(() => { wsx.dnit(); });
      });
    },
    newWorkspace(io) {
      swal({
        title: "New session...",
        text: 'Provide a unique session name. I suggest "main" as a default name.',
        customClass: "trj-analyses",
        type: "input",
        showCancelButton: true,
        closeOnConfirm: false,
        animation: "slide-from-top", 
        inputPlaceholder: "Alphanumeric characters including underscore..."
      }, (inputValue) => {
        if (inputValue === false) return false;
        if (inputValue === "") {
          swal.showInputError("Please provide a name.");
          return false;
        }
        this.get('socket').create(
          this, modname, clsname, {path: io.path}).then(wsx => {
          wsx.invoke('session.Workspace.create', {
            name: inputValue,
            iopath: io.path,
          }).then(workspace => {
            io.workspaces.pushObject(workspace);
            swal.close();
          }).catch(cat).finally(() => { wsx.dnit(); });
        });
      });
    },
    removeWorkspace(io, ws) {
      swal({
        title: "Are you sure?",
        text: "You will not be able to undo this!",
        type: "warning",
        showCancelButton: true,
        closeOnConfirm: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
      }, () => {
        this.get('socket').create(
          this, modname, clsname, {path: io.path}).then(wsx => {
          wsx.invoke('session.Workspace.delete', {id: ws.id}).then(/*id*/ ()=> {
            io.workspaces.removeObject(ws);
            swal.close();
          }).catch(cat).finally(() => { wsx.dnit(); });
        });
      });
    },
    openWorkspace(io, ws) {
      this.transitionTo('sbx-analysis', ...io.hops.concat(ws.id));
    }
  },
  setupController(controller, model) {
    this._super(controller, model);
    controller.set('messages', []);
  },
  on_sse_print(msg/*, err*/) {
    if (10 == msg.charCodeAt() || 32 == msg.charCodeAt()) { return; }
    this.controller.messages.pushObject({body: msg});
  },
});
