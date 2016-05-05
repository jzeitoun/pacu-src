import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  attributeBindings: ['style', 'width', 'height'],
  @computed('width', 'height') style(w, h) {
    return Ember.String.htmlSafe(`width: ${w}px; height: ${h}px;`);
  },
  initialize: function() {
    this.$().on('keydown', 'a.focus-responder', (e) => {
      const keyCode = e.keyCode || e.which;
      if (keyCode == 9 || keyCode == 32) { // tab or spacebar
        return true; // bubbles
      }
      e.preventDefault();
      // $(e.target).find('> polygon').trigger('something');
      // this
      // debugger
    }).on('click', 'a.focus-responder', (e) => {
      e.preventDefault();
    });
    $(document).on('keydown.x-layer', (e) => {
      const keyCode = e.keyCode || e.which;
      if (keyCode == 9) {
        e.preventDefault();
        const focused = this.$('a.focus-responder:focus:first');
        if (Ember.isEmpty(focused)) {
          this.$('.focus-responder:first').focus();
        } else {
          focused.blur();
          focused.parent().next().find('a.focus-responder').focus();
        }
        $('html, body').stop(true, true).animate({
          scrollTop: $('html').offset().top
        }, 100);
      }
    });
  }.on('didInsertElement'),
  dnitialize: function() {
    $(document).off('keydown.x-layer');
  }.on('willDestroyElement')
});

