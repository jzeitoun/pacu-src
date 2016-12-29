import Ember from 'ember';

function newWorkspace(io, name) {
  const payload = {iopath: io.info.iopath, name};
  Ember.$.ajax('/api/json/scanbox_manager/workspace', {
    type: 'POST',
    data: payload,
    dataType: 'json'
  }).then(data => {
    io.workspaces.pushObject(data.name);
    swal.close();
  }).fail((err, text, statusText) => {
    this.toast.error(err.responseText, err.statusText);
  });
}

function removeImported(io) {
  Ember.$.ajax('/api/json/scanbox_manager/io', {
    type: 'DELETE',
    data: { iopath: io.info.iopath },
    dataType: 'json',
  }).then(data => {
    this.currentModel.ios.removeObject(io);
  }).fail((err, text, statusText) => {
    this.toast.error(err.responseText, err.statusText);
  });
}

function removeWorkspace(io, name) {
  Ember.$.ajax('/api/json/scanbox_manager/workspace', {
    type: 'DELETE',
    data: { iopath: io.info.iopath, name },
    dataType: 'json',
  }).then(() => {
    io.workspaces.removeObject(name);
  }).fail((err, text, statusText) => {
    this.toast.error(err.responseText, err.statusText);
  });
}

export default Ember.Route.extend({
  model() {
    return Ember.RSVP.hash({
      path: Ember.$.getJSON('/api/json/miniscope_manager/path'),
      conditions: Ember.$.getJSON('/api/json/miniscope_manager/conditions'),
      ios: Ember.$.getJSON('/api/json/miniscope_manager/ios'),
    });
  },
  actions: {
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
        newWorkspace.call(this, io, inputValue);
      });
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
      }, removeImported.bind(this, io));
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
      }, removeWorkspace.bind(this, io, ws));
    },
    openWorkspace(io, ws) {
      const path = `${io.info.iopath}/${ws}`;
      this.transitionTo('scanbox-analyzer', path);
    }
  }
});
