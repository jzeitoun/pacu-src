import Ember from 'ember';

const monthNames = [
  "January", "February", "March",
  "April", "May", "June", "July",
  "August", "September", "October",
  "November", "December"
];

export function fromTimestamp(timestamp /*, hash*/) {
  const date = new Date(timestamp * 1000);
  const day = date.getDate();
  const monthIndex = date.getMonth();
  const year = date.getFullYear();
  return `${day} ${monthNames[monthIndex]} ${year}`
}

export default Ember.HTMLBars.makeBoundHelper(fromTimestamp);
