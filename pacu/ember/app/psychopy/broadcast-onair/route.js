import Ember from 'ember';

/*global swal*/

export default Ember.Route.extend({
  addMessage(message) {
    this.currentModel.messages.pushObject(message);
  },
  svcComplete(result) {
    if (Ember.$.isEmptyObject(result)) { return; }
    const self = this;
    const model = self.modelFor('psychopy');
    const by = model.handler.fields[1].attrs.item.name;
    const friend = (by === 'Anonymous') ? 'buddy' : by;
    Ember.set(model, 'result', result);
    swal({
      title: 'Session Complete',
      text: `Great job, ${friend}! Let's go review the result!`,
      type: 'success',
      showCancelButton: true,
      cancelButtonText: 'Maybe later.',
      confirmButtonText: 'Sure!',
    }, function() {
      self.replaceWith('psychopy.review');
    });
  },
  beforeModel: function() {
    console.log('before model');
  },
  model() {
    console.log('model');
    const self = this;
    return Ember.RSVP.hash({
      messages: [],
      websocket: new Ember.RSVP.Promise((resolve/*, reject*/) => {
        const ws = new WebSocket(`ws://${location.host}/socket/vstim`);
        ws.onopen = function() {
          console.log('on open');
          resolve(this); // `this` is websocket.
        };
        ws.fetch = function(name, payload) {
          console.log('fetch', name, payload, this);
          this.send(JSON.stringify([name, payload]));
        };
        ws.onmessage = function(msg) {
          console.log('on msg', msg);
          if (msg.data instanceof ArrayBuffer) {
              this.onbuffer(msg.data);
          } else {
            const [name, data] = JSON.parse(msg.data);
            self[name](data);
          }
        };
      })
    });
  },
  afterModel(model) {
    console.log('after model');
    const payload = this.modelFor('psychopy').payload || {};
    model.websocket.fetch('run', payload);

    // Ember.run.scheduleOnce('afterRender', this, function() {
    //   console.log('schedue fetch:run...', payload);
    //   window.qwe = model.websocket;
    //   model.websocket.fetch('run', payload);
    // });
  },
  actions: {
    willTransition: function(/*transition*/) {
      if (!Ember.isNone(this.currentModel.websocket)) {
        this.currentModel.websocket.close();
      }
    }
  }
});
