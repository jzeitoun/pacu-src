import Ember from 'ember';
import computed from 'ember-computed-decorators';

function log(...msgs) { console.log(...msgs); }

let sequence = 0;

class PromiseEx extends Ember.RSVP.Promise {
  constructor(resolver, label, context) {
    super(resolver, label);
    this.context = context;
    this.gatenames = null;
  }
  gate(...names) {
    if (Ember.isNone(this.gatenames)) {
      this.gatenames = names;
      this.gatenames.forEach((name) => {
        Ember.set(this.context, name, true);
      });
      super.finally(() => {
        this.gatenames.forEach((name) => {
          Ember.set(this.context, name, false);
        });
      });
    }
    return this;
  }
}
class WebSocketEx {
  constructor(context, url, binaryType='arraybuffer') {
    this.context = context;
    this.promises = {};
    this.constructionThens = [];
    this.constructionCatches = [];
    this.constructionFinallys = [];
    this.constructionPromise = new Ember.RSVP.Promise((res, rej) => {
      this.socket = new WebSocket(url);
      this.socket.binaryType = binaryType;
      this.socket.onmessage = this.onmessage.bind(this);
      this.socket.onopen = res.bind(this);
      this.socket.onerror = rej.bind(this);
      this.socket.onclose = function() {};
    }).then(() => {
      for (const f of this.constructionThens) f.call(context, this);
    }).catch((e) => {
      for (const f of this.constructionCatches) f.call(context, e);
    }).finally(() => {
      for (const f of this.constructionFinallys) f.call(context);
      this.constructionPromise = null;
      this.constructionThens = null;
      this.constructionCatches = null;
      this.constructionFinallys = null;
    });
  }
  dnit() {
    this.promises = null;
    this.context = null;
    this.socket.close();
    this.onbinaryFunc = null;
  }
  then(func) {
    if (Ember.isNone(this.constructionThens)) {
      console.error('Could not accept promise.');
    } else { this.constructionThens.push(func); }
    return this; // so that chain can go forth...
  }
  catch(func) {
    if (Ember.isNone(this.constructionCatches)) {
      console.error('Could not accept promise.');
    } else { this.constructionCatches.push(func); }
    return this; // so that chain can go forth...
  }
  finally(func) {
    if (Ember.isNone(this.constructionFinallys)) {
      console.error('Could not accept promise.');
    } else { this.constructionFinallys.push(func); }
    return this; // so that chain can go forth...
  }
  mirror(route) {
    return this.makeRequest('access', route).then((data) => {
      this.context.set(route, data);
    });
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
  oncloseFunc(buf) {}
  onbinaryFunc(buf) {}
  onclose(func) { this.oncloseFunc = func.bind(this.context); return this; }
  onbinary(func) { this.onbinaryFunc = func.bind(this.context); return this; }
  makeRequest(type, route, payload={as_binary: false}) {
    return new PromiseEx((res, rej) => {
      this.promises[++sequence] = {res, rej};
      this.socket.send(JSON.stringify([sequence, type, route, payload]));
    }, null, this.context);
  }
  onmessage(msg) {
    if (msg.data instanceof ArrayBuffer) {
        this.onbinaryFunc(msg.data); return;
    }
    const [seq, argument, error] = JSON.parse(msg.data);
    const {res, rej} = this.promises[seq];
    if (delete this.promises[seq]) {
      if (Ember.isNone(error)) {
        res(argument);
      } else {
        rej(error);
      }
    }
  }
  static asBufBased(context, url) {
    return new WebSocketEx(context, url, 'arraybuffer');
  }
  static asBlobBased(context, url) {
    return new WebSocketEx(context, url, 'blob');
  }
}
export default Ember.Service.extend({
  create(context, modname, clsname, src) {
    const url = `ws://${location.host}/ws/${modname}/${clsname}?files=${src}`;
    return new WebSocketEx.asBufBased(context, url);
  }
});
