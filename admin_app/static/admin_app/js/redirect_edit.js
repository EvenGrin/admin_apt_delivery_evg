$(document).ready(function () {
    $(document) .on('click', ".table tbody tr", e => {
      window.location.href = 'edit/' + $(e.currentTarget).data('id');
    });
})