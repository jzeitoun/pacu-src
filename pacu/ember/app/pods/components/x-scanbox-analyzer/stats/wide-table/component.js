import Ember from 'ember';
import computed, { on } from 'ember-computed-decorators';
import singleCols from './single-columns';
import multipleCols from './multiple-columns';

export default Ember.Component.extend({
  singleCols,
  multipleCols,
  elementId: 'stats-overview',
  tagName: 'table',
  classNames: `ui celled unstackable selectable
    inverted structured small compact table`,
  @on('didInsertElement') debug() { window.T = this; },
});
