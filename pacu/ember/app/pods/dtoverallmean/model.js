import attr from 'ember-data/attr';
import { belongsTo } from 'ember-data/relationships';
import Datatag from 'pacu/pods/datatag/model';
import computed from 'ember-computed-decorators';

export default Datatag.extend({
  value: attr({ defaultValue:[] }),
  roi: belongsTo('roi'),
  @computed('value') valueByFocalPlane(value) {
    const offset = this.get('roi.workspace.cur_pane') || 0;
    const nPanes = this.get('roi.workspace.condition.info.focal_pane_args.n') || 1;
    return value.filter((_, i) => i % nPanes == offset);
  }
});
