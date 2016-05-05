import Ember from 'ember';

export default Ember.Route.extend({
});

// model() {
//   const route = this;
//   return {
//     prompt: 'Select one...',
//     name: 'feat',
//     valuePath: 'value',
//     value: 0,
//     items: [
//       {value:'13', sui_icon:'play'},
//       {value:'42', sui_icon:'folder'},
//       {value:'73', sui_icon:'user'}
//     ],
//     change: function(item) {
//       // `this` is auto-generated controller which is almost useless.
//     },
//   };
// }
// {{sui-model-select
//   items=model.items
//   name=model.name
//   prompt=model.prompt
//   valuePath=model.valuePath
//   onChange=(action model.change)}}
