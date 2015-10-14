import Ember from 'ember';
import computed from 'ember-computed-decorators';

// onerror: function(ws, msg) {
//   console.log('onerrir', msg);
// },
function log(...msgs) { console.log(...msgs); }
// ws.onopen = this.onopen.bind(this, ws);
// ws.onclose = this.onclose.bind(this, ws);
// ws.onerror = this.onerror.bind(this, ws);
// ws.onmessage = this.onmessage.bind(this, ws);
//
let sequence = 0;
class PromiseEx extends Ember.RSVP.Promise {
  constructor(resolver, label, context) {
    super(resolver, label);
    this.context = context;
  }
  then(onFulfillment, onRejection, label) {
    const onf = onFulfillment ? onFulfillment.bind(this.context) : undefined;
    const onr = onRejection   ? onRejection.bind(this.context)   : undefined;
    const then = super.then(onf, onr, label);
    then.context = this.context;
    return then;
  }
}
class WebSocketEx {
  constructor(context, url, binaryType='arraybuffer') {
    const self = this;
    self.context = context;
    self.promises = {};
    self.firstPromise = new Ember.RSVP.Promise((res/*, rej*/) => {
      const socket = new WebSocket(url);
      socket.binaryType = binaryType;
      socket.onopen = function(/*e*/) { // `this` is websocket instance
        self.inst = this;
        res(this);
      };
      socket.onmessage = this.onmessage.bind(self);
    }).then((ws) => {
      self.firstPromise = null;
    });
  }
  dnit() {
    this.promises = null;
    this.context = null;
  }
  then(func) {
    if (Ember.isNone(this.firstPromise)) {
      console.error('Could not accept promise.');
    } else { this.firstPromise.then(func); }
    return this;
  }
  access(route) {
    return this.makeRequest('access', route);
  }
  accessAsBinary(route) {
    return this.makeRequest('access', route, {as_binary: true});
  }
  invoke(route, ...args) {
    return this.makeRequest('invoke', route, {args, as_binary: false});
  }
  invokeAsBinary(route, ...args) {
    return this.makeRequest('invoke', route, {args, as_binary: true});
  }
  onbinaryFunc(buf) { }
  onbinary(func) {
    this.onbinaryFunc = func.bind(this.context);
    return this;
  }
  makeRequest(type, route, payload={as_binary: false}) {
    return new PromiseEx((res, rej) => {
      this.promises[++sequence] = res;
      this.inst.send(JSON.stringify([sequence, type, route, payload]));
    }.bind(this), null, this.context);
  }
  onmessage(msg) {
    if (msg.data instanceof ArrayBuffer) {
        this.onbinaryFunc(msg.data); return;
    }
    const [seq, argument] = JSON.parse(msg.data);
    const res = this.promises[seq];
    if (delete this.promises[seq]) {
      res(argument);
    }
  }
  static bufAsBin(context, url) {
    return new WebSocketEx(context, url, 'arraybuffer');
  }
  static blobAsBin(context, url) {
    return new WebSocketEx(context, url, 'blob');
  }
}
export default Ember.Service.extend({
  create(context, modname, clsname, src) {
    const url = `ws://${location.host}/ws/${modname}/${clsname}?files=${src}`;
    return new WebSocketEx.bufAsBin(context, url);
  }
});
