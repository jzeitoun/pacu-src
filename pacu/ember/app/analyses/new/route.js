import Ember from 'ember';

export default Ember.Route.extend({
  model: function() {
    return this.store.createRecord('analysis');
  },
  actions: {
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
      const {title, host, user, desc, src} = model.toJSON();
      const good = [title, host, user, desc, src].every(Ember.isPresent);
      if (good) {
        model.save().then((model) => {
          self.replaceWith('analysis', model.id);
        }, (reason) => {
          swal('Oops...',
            `Failed to created a record...${reason}`,
            'error');
        });
      } else {
        swal('Oops...',
          'Every field should be provided...',
          'error');
      }
      return false;
    }
  }
});
