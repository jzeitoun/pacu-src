import Ember from 'ember';
import actions from './actions';
import SocketModel from './socketmodel';

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
      // const payload = Ember.getProperties(
      //   param, 'year month day mouse image'.w());
      // {
      //     year: param.year,
      //     month: param.month,
      //     day: param.day,
      //     image: param.image,
      //     mouse: param.mouse,
      //     session: param.session
      // }
