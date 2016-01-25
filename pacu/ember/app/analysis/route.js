import Ember from 'ember';
import ajax from 'ic-ajax';

const modname = 'pacu.core.svc.analysis.i3d';
const clsname = 'I3DAnalysisService'

export default Ember.Route.extend({
  socket: Ember.inject.service(),
  actions: {
    didTransition() {
      this.controllerFor('application').set(
        'current-feature', 'Image Stack Analysis');
    },
    willTransition: function(transition) {
      this.controller.cleanup(transition);
    }
  },
  afterModel(model, transition) {
    this._super(model, transition);
    const controller = this.controllerFor('analysis')
    return this.get('socket').create(
      controller, modname, clsname, model.id
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
