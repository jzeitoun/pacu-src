import Ember from 'ember';
import actions from 'pacu/pods/sci-analysis/actions';
import SocketModel from 'pacu/pods/sci-analysis/socketmodel';

const modname = 'pacu.core.io.scanimage.impl';
const clsname = 'ScanimageIOFetcher'

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
