$(document).ready(function () {
    $(document) .on('click', ".table tbody tr", e => {
      window.location.replace('edit/' + $(e.currentTarget).data('id'));
    });
})