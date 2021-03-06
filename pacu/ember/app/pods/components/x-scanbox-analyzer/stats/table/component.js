import Ember from 'ember';
import computed, { observes } from 'ember-computed-decorators';
import Table from 'ember-light-table';

const model = [
  { id: 1, firstName: 'HT', lastName: 'K' },
  { id: 2, firstName: 'SK', lastName: 'P' },
];
const columns = [
{
  label: '',
  align: 'center',
  sortable: false,
  subColumns: [
    {
      label: '#',
      sortable: false,
      valuePath: 'id',
      align: 'center',
      width: '50px'
    }
  ]
},
{
  label: 'Anova All',
  sortable: false,
  align: 'center',
  subColumns: [
    {
      label: 'F',
      sortable: false,
      valuePath: 'dtanovaall.value.f',
      width: '75px'
    },
    {
      label: 'P',
      sortable: false,
      valuePath: 'dtanovaall.value.p',
      width: '75px'
    }
  ]
},
{
  label: 'SF Cutoff',
  sortable: false,
  align: 'center',
  subColumns: [
    {
      label: 'RC10.X',
      sortable: false,
      valuePath: 'dtsfreqfit.value.rc10.0',
      width: '75px'
    },
    {
      label: 'RC10.Y',
      sortable: false,
      valuePath: 'dtsfreqfit.value.rc10.1',
      width: '75px'
    },
    {
      label: 'RC20.X',
      sortable: false,
      valuePath: 'dtsfreqfit.value.rc20.0',
      width: '75px'
    },
    {
      label: 'RC20.Y',
      sortable: false,
      valuePath: 'dtsfreqfit.value.rc20.1',
      width: '75px'
    }
  ]
},
{
  label: 'Orientations Fit',
  sortable: false,
  align: 'center',
  subColumns: [
    {
      label: 'OSI',
      sortable: false,
      valuePath: 'dtorientationsfitBySF.value.osi',
      width: '75px'
    },
    {
      label: 'DSI',
      sortable: false,
      valuePath: 'dtorientationsfitBySF.value.dsi',
      width: '75px'
    },
    {
      label: 'Sigma',
      sortable: false,
      valuePath: 'dtorientationsfitBySF.value.sigma',
      width: '75px'
    },
    {
      label: 'OPref',
      sortable: false,
      valuePath: 'dtorientationsfitBySF.value.o_pref',
      width: '75px'
    },
    {
      label: 'RMax',
      sortable: false,
      valuePath: 'dtorientationsfitBySF.value.r_max',
      width: '75px'
    },
    {
      label: 'Residual',
      sortable: false,
      valuePath: 'dtorientationsfitBySF.value.residual',
      width: '75px'
    },
  ]
}
];
function makeSFcolumn(sfs) {
  return {
    label: 'Anova Each',
    sortable: false,
    align: 'center',
    subColumns: sfs.map((sf, index) => {
      return {
        label: sf,
        sortable: false,
        valuePath: 'dtanovaeachs',
        width: '200px',
        format: function() {
          let o = this.get('row.dtanovaeachs').objectAt(index);
          if (o) {
            const f = o.get('f') || '';
            const p = o.get('p') || '';
            return Ember.String.htmlSafe(`f: ${f} <br/> p: ${p}`);
          }
        }
      }
    })
  }
}
export default Ember.Component.extend({
  model: model,
  @computed() columns() { return columns; },
  @computed() table() {
    const sfs = this.get('condition.sfrequencies');
    const sfc = makeSFcolumn(sfs);
    const columns = this.get('columns');
    const rois = this.get('onlyROIs');
    return new Table([].concat(columns, sfc), rois);
  },
  @computed('rois.[]') onlyROIs(rois) {
    const onlys = rois.filter(r => !r.get('isNew'));
    return onlys
  },
  @observes('onlyROIs.[]') roiUpdated() {
    const rois = this.get('onlyROIs');
    // console.log('ROIUP', rois.get('length'));
    this.get('table').setRows(rois.filter(r => !r.get('isNew')));
  }
});
