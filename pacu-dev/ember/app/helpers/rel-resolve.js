import Ember from 'ember';
// import DS from 'ember-data';

// const ObjectPromiseProxy = Ember.ObjectProxy.extend(Ember.PromiseProxyMixin);

export function relResolve(/*params/*, hash*/) {
  // const [model, rel, index, path] = params;
  // const promise = model.get(rel).then(rels => {
  //   return rels.objectAt(index).get(path);
  // })
  // return ObjectPromiseProxy.create({ promise })
}

export default Ember.Helper.helper(relResolve);
