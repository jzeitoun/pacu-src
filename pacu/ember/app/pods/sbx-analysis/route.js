import Ember from 'ember';
import actions from 'pacu/pods/sbx-analysis/actions';
import SocketModel from 'pacu/pods/sbx-analysis/socketmodel';
// import computed from 'ember-computed-decorators';

const modname = 'pacu.core.io.scanbox.impl';
const clsname = 'ScanboxIOFetcher';
const moduleName = 'pacu.core.io.scanbox.model.db';
const baseName = 'SQLite3Base';

export default Ember.Route.extend({
  socket: Ember.inject.service(),
  session: Ember.inject.service(),
  actions: actions,
  model(param /*, transition */) {
    this.get('session.jsonapi').setProperties({moduleName, baseName,
      sessionArgs: [param.mouse, param.day, param.io_name]
    });
    this.store.unloadAll(); // important!
    const workspace = this.store.findRecord('workspace', param.workspace_id, { include: 'rois' });
    const conditions = this.store.findAll('condition');
    const socket = new Ember.RSVP.Promise((resolve /*, reject */) => {
      return this.get('socket').create(
        this, modname, clsname, param
      ).then((wsx) => {
        wsx.socket.onclose = () => {
          this.toast.warning('WebSocket connection closed.');
        };
        this.set('wsx', wsx);
        this.toast.success('WebSocket connection estabilished.');
        resolve(SocketModel.create({ wsx }));
      });
    });
    return Ember.RSVP.hash({ workspace, socket, conditions });
  },
  afterModel(model /*, transition */) {
    model.workspace.get('condition').then(c => {
      if (Ember.isNone(c) && model.conditions.get('length')) {
        model.workspace.set('condition', model.conditions.get('firstObject'));
        model.workspace.save();
      }
    });
    model.socket.initialize(this, model.workspace);
  },
  on_sse_print(msg, err) {
    if (10 === msg.charCodeAt() || 32 === msg.charCodeAt()) { return; }
    if(err) {
      return this.toast.error(err);
    }
    this.toast.info(msg);
  }
});
