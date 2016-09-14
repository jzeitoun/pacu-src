import Ember from 'ember';
import actions from 'pacu/pods/scanbox-analyzer/actions';
import SocketStream from 'pacu/pods/scanbox-analyzer/socketstream';

const modname = 'pacu.core.io.scanbox.impl2';
const clsname = 'ScanboxIOStream';
const moduleName = 'pacu.core.io.scanbox.model.db';
const baseName = 'SQLite3Base';

export default Ember.Route.extend({
  socket: Ember.inject.service(),
  session: Ember.inject.service(),
  actions: actions,
  model(param) {
    window.S = this.store; window.R = this;
    const hops = param.hops.split('/');
    const name = hops.pop();
    const ioName = hops.join('/');
    this.get('session.jsonapi').setProperties({moduleName, baseName,
      sessionArgs: [ioName]
    });
    const workspace = this.get('store').query(
    'workspace', { filter: { name }, }).then(wss => {
      return wss.findBy('name', name);
    });
    const condition = this.store.findRecord('condition', 1);
    // const trials = this.store.findAll('trial');
    const rois = this.store.findAll('roi');
    const stream = new Ember.RSVP.Promise((resolve /*, reject */) => {
      return this.get('socket').create(
        this, modname, clsname, ioName
      ).then((wsx) => {
        wsx.socket.onclose = () => {
          this.toast.warning('WebSocket connection closed.');
        };
        this.set('wsx', wsx);
        this.toast.success('WebSocket connection estabilished.');
        resolve(SocketStream.create({ wsx }));
      });
    });
    return Ember.RSVP.hash({ workspace, condition, rois, /*trials,*/ stream });
  },
  afterModel(model /*, transition */) {
    this._super(...arguments);
    if (Ember.isEmpty(model.rois)) {
      this.toast.info(`Hey buddy, you have no ROIs in this workspace. 
        How about drawing some?`);
    }
  },
  setupController(controller, model) {
    this._super(...arguments);
    controller.set('stream', model.stream);
  },
  on_sse_print(msg, err) {
    if (10 === msg.charCodeAt() || 32 === msg.charCodeAt()) { return; }
    if(err) { return this.toast.error(err); }
    this.toast.info(msg);
  }
});
