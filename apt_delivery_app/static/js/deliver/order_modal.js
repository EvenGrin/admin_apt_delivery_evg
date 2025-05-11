$(document).ready(function () {
  $(".order-item").on("click", function (ev) {
    if (!$(ev.target).closest(".delivered, .confirm-order, .cancel-order").length) {
      let id = $(this).data("order-id");
      $.get("/deliver/deliver_orders/" + id, function (data) {
        $("#order_modal .modal-body").html(data);
        $("#order_modal").modal("show");
      });
    }
  });
});
