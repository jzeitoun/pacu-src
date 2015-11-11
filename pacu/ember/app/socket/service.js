import Ember from 'ember';
import computed from 'ember-computed-decorators';

function log(...msgs) { console.log(...msgs); }

let sequence = 0;

class PromiseEx extends Ember.RSVP.Promise {
  constructor(resolver, label, context) {
    super(resolver, label);
    this.context = context;
  }
  then(onFulfillment, onRejection, label) {
    console.log('load then');
    const onf = onFulfillment ? onFulfillment.bind(this.context) : undefined;
    const onr = onRejection   ? onRejection.bind(this.context)   : undefined;
    const then = super.then(onf, onr, label);
    then.context = this.context;
    return this;
  }
  catch(onRejection, label) {
    console.log('load actch ');
    const onr = onRejection   ? onRejection.bind(this.context)   : undefined;
    const catchy = super.catch(onr, label);
    catchy.context = this.context;
    return this;
  }
  finally(callback, label) {
    console.log('load finalyl ');
    const cb = callback   ? callback.bind(this.context)   : undefined;
    const finallie = super.catch(cb, label);
    finallie.context = this.context;
    return this;
  }
}
class WebSocketEx {
  constructor(context, url, binaryType='arraybuffer') {
    const self = this;
    self.context = context;
    self.promises = {};
    self.constructionThens = [];
    self.constructionCatches = [];
    self.constructionFinallys = [];
    self.constructionPromise = new Ember.RSVP.Promise(function(res, rej) {
      self.socket = new WebSocket(url);
      self.socket.binaryType = binaryType;
      self.socket.onmessage = self.onmessage.bind(self);
      self.socket.onopen = res.bind(self);
      self.socket.onerror = rej.bind(self);
      self.socket.onclose = function() {};
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
    return this.makeRequest('access', route).then(function(data) {
      this.set(route, data);
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
  onbinaryFunc(buf) { }
  onbinary(func) {
    this.onbinaryFunc = func.bind(this.context);
    return this;
  }
  makeRequest(type, route, payload={as_binary: false}) {
    return new PromiseEx((res, rej) => {
      this.promises[++sequence] = {res, rej};
      // this.promises[++sequence] = res;
      this.socket.send(JSON.stringify([sequence, type, route, payload]));
    }.bind(this), null, this.context);
  }
  onmessage(msg) {
    if (msg.data instanceof ArrayBuffer) {
        this.onbinaryFunc(msg.data); return;
    }
    const [seq, argument, error] = JSON.parse(msg.data);
    log('msg return', seq, argument, error);
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
