import Ember from 'ember';
import {
  importRaw, removePackage
} from 'pacu/sci-analyses/years/months/days/index/route';

const modname = 'pacu.core.io.trajectory.impl';
const clsname = 'TrajectoryIO'

export default Ember.Route.extend({
  socket: Ember.inject.service(),
  model() {
    const recordings = this.modelFor('trj-analyses.recordings');
    return Ember.$.getJSON(`/api/json/trajectory/index/${recordings.recording}`);
  },
  setupController(controller, model) {
    this._super(controller, model);
    controller.set('messages', []);
  },
  actions: {
    didTransition() {
      this.controllerFor('application').set(
        'current-feature', 'Trajectory Data Manager');
    },
    importRaw(trial) {
      importRaw.call(this, modname, clsname, trial);
    },
    newSession(trial) {
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
        const path = trial.package.path;
        const session = inputValue;
        const prom = Ember.$.post('/api/json/trajectory/session', {path, session});
        prom.then(data => {
          const pkg = JSON.parse(data);
          Ember.set(trial, 'package', pkg);
          swal.close();
        }).fail(err => {
          swal('Opps...', err.responseText, "error");
        });
      });
    },
    removePackage(trial) {
      swal({
        title: "Are you sure?",
        text: "You will not be able to undo this!",
        type: "warning",
        showCancelButton: true,
        closeOnConfirm: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
      }, () => {
        removePackage.call(this, modname, clsname, trial);
      });
    },
    removeSession(trial, session) {
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
          url: '/api/json/trajectory/session',
          type: 'DELETE',
          data: {
            session: session.path,
            path: trial.package.path
          }
        });
        prom.then(data => {
          Ember.set(trial, 'package', JSON.parse(data));
          swal.close();
        }).fail(err => {
          swal('Opps...', err.responseText, "error");
        });
      });
    },
    openSession(trial, session) {
      this.transitionTo('trj-analysis',
        this.currentModel.recording,
        trial.name,
        session.name
      );
    }
  },
  on_sse_print: function(msg, err) {
    if (10 == msg.charCodeAt() || 32 == msg.charCodeAt()) { return; }
    this.controller.messages.pushObject({body: msg});
  },
});
