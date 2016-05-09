import Ember from 'ember';

export default Ember.Route.extend({
  model: function() {
    return this.store.createRecord('analysis');
  },
  setupController(controller, model) {
    this._super(controller, model);
    controller.set('expTypes', ['ScanImage', 'ScanBox']);
    controller.set('actions', {
      experimentTypeEnumChanged: function(model, index) {
        model.set('conditionid', null);
        model.set('type', index);
      }
    });
  },
  actions: {
    searchCondition: function(model) {
      const type = model.get('type');
      if (Ember.isNone(type)) {
        this.toast.warning('Please select experiment type...');
        return;
      }
      $('#search-condition').modal({
        closable  : false,
        onDeny    : function() { return true; },
        onApprove : function() { return true; }
      }).modal('show');
    },
    willTransition: function(transition) {
      const model = this.get('currentModel');
      if (model.get('isNew')) {
        if (Ember.$.isEmptyObject(model.changedAttributes())) {
          model.deleteRecord();
        } else {
          transition.abort();
          swal({
            title: 'Are you sure?',
            text: 'You are about to discard your data.',
            type: 'warning',
            showCancelButton: true,
            cancelButtonText: 'No',
            confirmButtonText: 'Yes',
          }, function(confirm) {
            if (confirm) {
              model.deleteRecord();
              transition.retry();
            }
          });
        }
      }
    },
    focusSubmit: function() {
      Em.$('#submit-new-analysis').focus();
    },
    save: function(model) {
      const self = this;
      const {title, user, desc, imagesrc, conditionid} = model.toJSON();
      const good = [title, user, imagesrc, conditionid].every(Ember.isPresent);
      if (good) {
        model.save().then((model) => {
          self.controller.set('steps', []);
          self.replaceWith('analysis', model.id);
        }, (reason) => {
          swal('Oops...',
            `Failed to created a record...${reason}`,
            'error');
        });
      } else {
        swal('Oops...',
          'Some fields are missing...',
          'error');
      }
      return false;
    }
  }
});
