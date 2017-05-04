import Ember from 'ember';

export function promiseSequence(targets, task, done) {
  const targetsCopied = targets.copy();
  const len = targetsCopied.get('length');
  const promise = new Ember.RSVP.Promise((resolve, reject) => {
    let shouldStop = false;
    (function next(index) {
      const target = targetsCopied.shiftObject();
      if (shouldStop || !target) {
        resolve();
        return swal.close();
      }
      swal({
        type: 'info',
        title: 'Batch: Compute All',
        text: `Running ${index}/${len}...`,
        showConfirmButton: false,
        showCancelButton: true,
        focusCancel: true,
        cancelButtonClass: "ui red basic button",
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: false,
      }).catch(dismiss => {
        shouldStop = true;
        swal({
          type: 'warning',
          title: 'Batch: Stop requested',
          text: `It will end after the current process #${index}.
                 Please wait little more...`,
          showConfirmButton: false,
          showCancelButton: false,
          allowOutsideClick: false,
          allowEscapeKey: false,
          allowEnterKey: false,
        });
      });
      target[task]().then(next.bind(null, index + 1));
    })(1);
  });
  return promise;
}
