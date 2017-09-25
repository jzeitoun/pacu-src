import Ember from 'ember';

export function ifEqThenClass(params/*, hash*/) {
  const [a, b, cls] = params;
  return a == b ? cls : '';
}

export default Ember.Helper.helper(ifEqThenClass);
