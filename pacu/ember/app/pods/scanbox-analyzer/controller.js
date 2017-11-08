import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    addROI(roi, file, workspace) {
      file.save(); // saving roi_count to file to maintain compatibility with sqlite structure
      var newROI = this.get('store').createRecord('fb-roi', roi);
      workspace.get('rois').addObject(newROI);
      newROI.save().then(function() {
        return workspace.save();
      });
    },

    updateROI(roi) {
      roi.save()
    },

    deleteROI(roi) {
      roi.deleteRecord();
      roi.save()
    },

    computeROIs(rois, workspace) {
      var store = this.get('store');
      //var singleROIData = store.findRecord('roi-data', 1);
      var roiData = store.findAll('roi').then(result => {
        var roiDataObjects = result.toArray();
        var existingIDs = roiDataObjects.map(function(roi) {
          return Number(roi.id);
        });
        rois.forEach(function(roi) {
          if (!(roi.get('polygon') == roi.get('lastComputedPolygon'))) {
            roi.set('lastComputedPolygon', 'inProgress');
            roi.save();
          };
        });
        rois.forEach(function(roi) {
          // if roi is already computed, skip
          if (roi.get('polygon') == roi.get('lastComputedPolygon')) {
            return;
          };
          // create sqlite record if none exists
          if (!existingIDs.includes(roi.get('roi_id'))) {
            //console.log(existingIDs);
            //console.log(roi.get('roi_id'));
            var polygon = pointsToArray(roi.get('polygon')).map(function(point) {
              return {x:point[0], y:point[1]};
            });
            var newRecord = store.createRecord('roi', {
              polygon: polygon,
              workspace: workspace
            });
            // compute
            newRecord.save().then(() => {
              newRecord.refreshAll().then(() => {
                roi.set('lastComputedPolygon', roi.get('polygon'));
              });
            });
          } else {
            // record exists, skip to compute
            var roiData = roiDataObjects.filterBy('id', String(roi.get('roi_id'))).get('firstObject');
            return store.createRecord('action', {
              model_name: 'ROI',
              model_id: roiData.id,
              action_name: 'refresh_all'
            }).save().then((action) => {
              if (action.get('status_code') === 500) {
                //console.log(`ROI ${roiData.id} returned an error.`);
                //this.get('toast').error(action.get('status_text'));
              } else {
                //console.log(`Finished computing ${roiData.id}`)
              };
            }).finally(() => {
              roi.set('lastComputedPolygon', roi.get('polygon'));
              roi.save();
            });
          }
        });
      });

      function pointsToArray(strPoints) {
        return strPoints.match(/[^,]+,[^,]+/g).map(function(point) {
          return point.split(',').map(Number);
        });
      }
    },

    ensureWorkspace(file, workspace) {
      file.get('workspaces').then(workspaces => {
        if (!workspaces.includes(workspace)) {
          workspaces.addObject(workspace);
          workspaces.save();
          return file.save();
        };
      });
    }
  }
});
