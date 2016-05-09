import Ember from 'ember';

export function splitLines(value /*, hash*/) {
  // return value.replace(/(?:\r\n|\r|\n)/g, '<br />';
  return value[0].split('\n');
}

export default Ember.Helper.helper(splitLines);
// export default Ember.HTMLBars.makeBoundHelper(splitLines);
