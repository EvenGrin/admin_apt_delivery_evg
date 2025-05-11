$(document).ready(function () {
  $(document).on("click", ".confirm-order", function () {
    const orderId = $(this).data("order-id");
    $.ajax({
      url: `/operator/order/${orderId}/confirm/`,
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
      },
      success: function (data) {
        if (data.status === "success") {
          alert(data.message);
          $(`td[data-id = "${orderId}"]`)
            .html(data.new_status)
            .addClass("table-success")
            .removeClass("table-primary");
          updateOrderActions(data.status_value, orderId);
        } else {
          alert(data.message);
        }
      },
      error: function (xhr) {
        alert("Произошла ошибка: " + xhr.responseJSON.message);
      },
    });
  });

  $(document).on("click", ".cancel-order", function () {
    const orderId = $(this).data("order-id");
    $.ajax({
      url: `/operator/order/${orderId}/cancel/`,
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
      },
      success: function (data) {
        if (data.status === "success") {
          alert(data.message);
          $(`td[data-id = "${orderId}"]`)
            .html(data.new_status)
            .addClass("table-danger")
            .removeClass("table-primary");
          updateOrderActions(data.status_value, orderId);
        } else {
          alert(data.message);
        }
      },
      error: function (xhr) {
        alert("Произошла ошибка: " + xhr.responseJSON.message);
      },
    });
  });

  function updateOrderActions(newStatus, orderId) {
    const $actionsDiv = $("#order-actions");

    if (newStatus === "confirmed") {
      $actionsDiv.html(`
                <button class="cancel-order btn btn-danger" data-order-id="${orderId}">
                    Отменить заказ
                </button>
            `);
    } else if (newStatus === "canceled" || newStatus === "completed") {
      $actionsDiv.html("<p>Действия недоступны для текущего статуса</p>");
    }
  }
});
