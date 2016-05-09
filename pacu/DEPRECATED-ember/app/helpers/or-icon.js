import Ember from 'ember';

export function orIcon(params/*, hash*/) {
  const [classes, value] = params;
  return Ember.isNone(value) ? new Ember.Handlebars.SafeString(`<i class="${classes} icon"></i>`) : value;
}

export default Ember.Helper.helper(orIcon);
