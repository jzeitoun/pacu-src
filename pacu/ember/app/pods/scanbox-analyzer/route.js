import Ember from 'ember';
import actions from 'pacu/pods/scanbox-analyzer/actions';
import SocketStream from 'pacu/pods/scanbox-analyzer/socketstream';

const modname = 'pacu.core.io.scanbox.impl2';
const clsname = 'ScanboxIOStream';
const moduleName = 'pacu.core.io.scanbox.model.db';
const baseName = 'SQLite3Base';
const include = 'condition,condition.trials,dtoverallmeans,rois,rois.dtorientationsmeans,rois.dtorientationbestprefs,rois.dtorientationsfits,rois.dtanovaeachs,rois.dtsfreqfits,rois.dtanovaalls';
const queryParam = { include };

export default Ember.Route.extend({
  activate() {
    Ember.$(document).on('keyup.conditions', e => {
      var esName, eName;
      const ws = this.currentModel.workspace;
      const cd = this.currentModel.condition;
      switch (e.keyCode) {
        case 83: // s
          esName = 'sfrequencies';
          eName = 'cur_sfreq';
          break;
        case 67: // c
          esName = 'contrasts';
          eName = 'cur_contrast';
          break;
        default:
          return false;
      }
      var elements = cd.get(esName);
      var element = ws.get(eName);
      var index = elements.indexOf(element);
      var next = elements[(index+1)%elements.length];
      ws.set(eName, next);
    });
  },
  deactivate() {
    Ember.$(document).off('keyup.conditions');
  },
  socket: Ember.inject.service(),
  session: Ember.inject.service(),
  actions: actions,
  model(param) {
    window.R = this;
    const hops = param.hops.split('/');
    const wsName = hops.pop();
    const ioName = hops.join('/');
    this.get('session.jsonapi').setProperties({moduleName, baseName,
      sessionArgs: [ioName]
    });
    const kw = {iopath:ioName, wsname: wsName};
    const workspace = new Ember.RSVP.Promise((resolve/*, reject*/) => {
      Ember.$.getJSON('/api/json/scanbox_manager/workspace_id', kw).then(id => {
        resolve(this.store.findRecord('workspace', id, queryParam));
      });
    });
    let cur_pane;
    const condition = workspace.then(ws => {
      if (wsName !== ws.get('name')) {
        swal(
          'Reference error',
          'Session seems to refer a wrong workspace. Please restart Pacu process in backend!',
          'error'
        )
        this.transitionTo('scanbox-manager');
      }
      cur_pane = ws.get('cur_pane') || 0;
      return ws.get('condition');
    });
    const stream = condition.then(() => {
      return new Ember.RSVP.Promise((resolve /*, reject */) => {
        return this.get('socket').create(
          this, modname, clsname, ioName
        ).then((wsx) => {
          wsx.invoke('setup_focal_pane', cur_pane);
          wsx.socket.onclose = () => {
            this.toast.warning('WebSocket connection closed.');
          };
          this.set('wsx', wsx);
          this.toast.success('WebSocket connection estabilished.');
          Ember.run.later(() => {
            resolve(SocketStream.create({ wsx }));
          }, 1000); // necessary
        });
      });
    });
    const name = { io: ioName, ws: wsName };
    return Ember.RSVP.hash({ condition, workspace, stream, name });
  },
  afterModel(/*model, transition */) {
    this._super(...arguments);
    // window.M = model; window.S = this.store; window.R = this;
    // if (Ember.isEmpty(model.rois)) {
    //   this.toast.info(`Hey buddy, you have no ROIs in this workspace. 
    //     How about drawing some?`);
    // }
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
