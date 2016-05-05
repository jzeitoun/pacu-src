import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  index: 0,
  interval: 16,
  width: 400,
  height: 400,
  @computed('width') vpwidth(w) {
    return w + 2;
  },
  @computed('height') vpheight(h) {
    return h + 2;
  },
  @computed('api', 'src') url(api, s) {
    const encoded = encodeURIComponent(s);
    return `ws://${location.host}/${api}/${encoded}`;
  },
  fetch(data) {
    console.log('fetch', data);
    this.ws.send(JSON.stringify(data));
  },
  onopen() {
    console.log('on open...');
    this.fetch({func: 'init_resource'});
    this.set('active', true);
  },
  onclose() {
    console.log('on close...');
    this.set('active', false);
  },
  onerror(msg) { console.log('on error', msg); },
  onmessage(msg) {
    console.log('on message', msg);
    this.ws.send(JSON.stringify(data));
    if (msg.data instanceof ArrayBuffer) {
        this.onbuffer(msg.data);
    } else {
      var data = JSON.parse(msg.data);
      this[`on${data.func}`](data);
    }
  },
  onready(data) {
    console.log('on ready...');
    var [length, height, width] = data.shape;
    var interval = 16;
    this.setProperties({length, height, width, interval});
    this.set('meta', data.meta);
    this.set('filename', data.filename);
    const cmap = this.get('cmap');
    if (!Ember.isNone(cmap)) {
      this.fetch({func: 'set_colormap', cmap});
    }
    this.draw();
  },
  onbuffer(data) {
    this.set('currentBuffer', data);
  },
  nudge: function(by=1) {
    return this.incrementProperty('index', by);
  },
  setCMap: function(cmap) {
    this.set('cmap', cmap);
    this.fetch({func: 'set_colormap', cmap});
  },
  draw: function() {
    var index = parseInt(this.getWithDefault('index', 0));
    this.fetch({func: 'draw', index});
  }.observes('index'),
  initSocket: function() {
    console.log('init socket...');
    this.ws = new WebSocket(this.get('url'));
    this.ws.binaryType = 'arraybuffer';
    ['onopen', 'onclose', 'onerror', 'onmessage'].forEach((event) => {
      this.ws[event] = this[event].bind(this);
    });
  }.on('didInsertElement'),
  dnitSocket: function() {
    console.log('dnit socket...');
    console.log('mms-stream dnit');
    this.ws.close();
    ['onopen', 'onclose', 'onerror', 'onmessage'].forEach((event) => {
      this.ws[event] = null;
    });
    this.set('index', 0);
    this.ws = null;
  }.on('willDestroyElement'),
  reloadSocket: function() {
    if (Ember.isNone(this.ws)) { return; }
    console.log('reload socket');
    Em.run.scheduleOnce('actions', this, () => {
      this.dnitSocket();
      this.initSocket();
    });
  }.observes('url')
});
