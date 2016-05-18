import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  attributeBindings: ['style', 'width', 'height'],
  @computed('width', 'height') style(w, h) {
    return Ember.String.htmlSafe(`width: ${w}px; height: ${h}px;`);
  },
  initialize: function() {
    $(document).on('keydown.x-layer', (e) => {
      // check if event sender is valid.
      const keyCode = e.keyCode || e.which;
      // 13 enter
      // 32 space bar
      if (keyCode == 9) { // tab
        // e.preventDefault();
        // this.get('do')('rotateFocus');
        // $('html, body').stop(true, true).animate({
        //   scrollTop: $('html').offset().top
        // }, 100);
      }
      if (keyCode == 13) { // enter
        this.get('do')('hitFocus');
      }
    });
  }.on('didInsertElement'),
  dnitialize: function() {
    $(document).off('keydown.x-layer');
  }.on('willDestroyElement'),
  click() {
    // this.get('do')('revokeFocus');
  }
});

