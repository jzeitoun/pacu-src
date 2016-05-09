import Ember from 'ember';
import actions from 'pacu/pods/sbx-analysis/actions';
import SocketModel from 'pacu/pods/sbx-analysis/socketmodel';
import computed from 'ember-computed-decorators';

const modname = 'pacu.core.io.scanbox.impl';
const clsname = 'ScanboxIOFetcher';
const moduleName = 'pacu.core.io.scanbox.model.db';
const baseName = 'SQLite3Base';

export default Ember.Route.extend({
  socket: Ember.inject.service(),
  session: Ember.inject.service(),
  actions: actions,
  model(param, transition) {
    this.get('session.jsonapi').setProperties({moduleName, baseName,
      sessionArgs: [param.base, param.io_name]
    });
    const workspace = this.store.findRecord('workspace', param.workspace_id);
    const traces = '';
    // this.store.query('trace', {
    //   view: { workspace_id: param.workspace_id }
    // });
    const socket = new Promise((resolve, reject) => {
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
    return Ember.RSVP.hash({ workspace, socket, traces });
  },
  afterModel(model, transition) {
    model.socket.initialize(this, model.workspace);
  },
  on_sse_print(msg, err) {
    if (10 == msg.charCodeAt() || 32 == msg.charCodeAt()) { return; }
    console.log(`Backend: ${msg}`);
  }
});
