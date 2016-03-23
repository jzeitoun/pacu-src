import Ember from 'ember';

const modname = 'pacu.core.io.trajectory.session';
const clsname = 'TrajectoryTrialFetcher'

export default Ember.Route.extend({
  socket: Ember.inject.service(),
  actions: {
    willTransition: function(transition) {
      this.controller.cleanup(transition);
    }
  },
  model({index}) {
    const session = this.modelFor('trj-analysis');
    return {session, index};
  },
  afterModel(model, transition) {
    this._super(model, transition);
    const controller = this.controllerFor('trj-analysis.trial');
    return this.get('socket').create(
      controller, modname, clsname, [model.session.id, model.index]
    ).then(function(wsx) {
      wsx.socket.onclose = (wsx) => {
        this.toast.warning('WebSocket connection closed.');
      };
      controller.set('session', wsx);
    }).then(function(wsx){
      this.toast.success('WebSocket connection estabilished.');
    });
  }
});
