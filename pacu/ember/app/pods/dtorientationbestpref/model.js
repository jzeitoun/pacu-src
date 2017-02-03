import attr from 'ember-data/attr';
import { belongsTo } from 'ember-data/relationships';
import Datatag from 'pacu/pods/datatag/model';

export default Datatag.extend({
  roi: belongsTo('roi'),
  value: attr(),
});
