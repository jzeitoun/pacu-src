import Ember from 'ember';

export function orIcon(params/*, hash*/) {
  const [classes, value] = params;
  return value || new Ember.Handlebars.SafeString(`<i class="${classes} icon"></i>`);
}

export default Ember.Helper.helper(orIcon);
