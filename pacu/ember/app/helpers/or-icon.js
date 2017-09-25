import Ember from 'ember';

export function orIcon(params/*, hash*/) {
  const [classes, value] = params;
  return Ember.isNone(value) ? Ember.String.htmlSafe(`<i class="${classes} icon"></i>`) : value;
}

export default Ember.Helper.helper(orIcon);
