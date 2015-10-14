import Ember from 'ember';

export function fromTimestamp(timestamp /*, hash*/) {
  return new Date(timestamp * 1000);
}

export default Ember.HTMLBars.makeBoundHelper(fromTimestamp);
