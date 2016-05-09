import Ember from 'ember';
import actions from 'pacu/trj-analysis/actions';
import SocketModel from 'pacu/trj-analysis/socketmodel';

const modname = 'pacu.core.io.trajectory.impl';
const clsname = 'TrajectoryIOFetcher'

export default Ember.Route.extend({
  socket: Ember.inject.service(),
  actions: actions,
  model(param, transition) {
    return new Promise((resolve, reject) => {
      return this.get('socket').create(
        this, modname, clsname, param
      ).then((wsx) => {
        wsx.socket.onclose = (wsx) => {
          this.toast.warning('WebSocket connection closed.');
        };
        this.set('wsx', wsx);
        this.toast.success('WebSocket connection estabilished.');
        resolve(SocketModel.create({ wsx }));
      });
    });
  },
  afterModel(model, transition) { model.initialize(this); },
  on_sse_print(msg, err) {
    if (10 == msg.charCodeAt() || 32 == msg.charCodeAt()) { return; }
    console.log(`Backend: ${msg}`);
  }
});