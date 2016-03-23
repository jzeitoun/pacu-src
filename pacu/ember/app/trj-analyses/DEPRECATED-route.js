import Ember from 'ember';

const modname = 'pacu.core.io.trajectory.session';
const clsname = 'TrajectorySession'

export default Ember.Route.extend({
  socket: Ember.inject.service(),
  model() {
    return this.store.findAll('tr-session');
  },
  setupController(controller, model) {
    this._super(...arguments);
    controller.set('messages', []);
  },
  actions: {
    didTransition() {
      this.controllerFor('application').set(
        'current-feature', 'Trajectory Analysis Sessions');
    },
    coldTransition(model) {
      location.href = `trj-analysis/${model.id}`
    },
    importRaw(model) {
      const $console = Ember.$('#import-progress');
      $console.modal({closable: false}).modal('show');
      this.controller.messages.pushObject({body: 'Please wait...'});
      this.get('socket').create(this, modname, clsname).then(wsx => {
        wsx.invoke('import_raw_by_id', model.id).then(() => {
          $console.modal('hide');
          swal({
            title: 'Import Complete',
            text: "Let's go review the result.",
            type: 'success',
            allowEscapeKey: false,
            confirmButtonText: 'Sure!',
          }, () => {
            this.send('coldTransition', model);
          });
        }).catch(error => {
          swal({
            title: 'Import Failed',
            text: `Please review your data. (${error.detail})`,
            type: 'error',
            allowEscapeKey: false,
            confirmButtonText: 'Okay!',
          }, () => {
            $console.modal('hide');
          });
        }).finally(() => {
          this.controller.messages.clear();
          wsx.dnit();
        });
      });
    }
  },
  on_sse_print: function(msg, err) {
    this.controller.messages.pushObject({body: msg});
  },
});
