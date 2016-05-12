import Model from 'ember-data/model';
import attr from 'ember-data/attr';
// import { belongsTo, hasMany } from 'ember-data/relationships';

export default Model.extend({
  model_name: attr(),
  model_id: attr(),
  query_only: attr(),
  action_name: attr(),
  action_args: attr(),
  action_kwargs: attr(),
  status_code: attr(),
  status_text: attr(),
});
