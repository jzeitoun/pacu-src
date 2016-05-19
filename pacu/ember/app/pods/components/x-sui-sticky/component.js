import Ember from 'ember';
import { on } from 'ember-computed-decorators';

export default Ember.Component.extend({
  @on('didInsertElement') initialize() {
    this.$().height(this.$('> div').height());
    this.$('> div').addClass('sticky').sticky({
    });
  },
  @on('willDestroyElement') dnitialize() { }
});
