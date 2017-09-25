import Ember from 'ember';

export default Ember.Component.extend({
  setViewport: function() {
    this.viewport = this.$()[0];
    this.updateScroll();
    // const websocket = this.getAttr('websocket');
    // websocket.addConsoleMessage = this.addConsoleMessage.bind(this);
    // Ember.run.scheduleOnce('render', this, function() {
    //   websocket.fetch('init_console_stream');
    // });
  }.on('didInsertElement'),
  // unregister: function() {
  //   this.messages.clear();
  // }.on('willDestroyElement'),
  // API entry for websocket
  // addConsoleMessage: function({epoch, message}) {
  //   const date = new Date(0);
  //   date.setUTCSeconds(epoch);
  //   const time = date.toLocaleTimeString();
  //   this.messages.addObject(`${time}: ${message}`);
  // },
  updateScroll: function() {
    this.viewport.scrollTop = this.viewport.scrollHeight;
    // Ember.run.scheduleOnce('afterRender', this, function() {
    // });
  }.on('didUpdate').observes('messages.[]')
});
