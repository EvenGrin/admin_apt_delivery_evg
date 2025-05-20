$(document).ready(function () {
  $(".order-item").on("click", function (e) {
    // Проверяем, что клик не попал на кнопку "Отменить заказ"
    if (!$(e.target).closest(".confirm-cancel-order").length) {
      $("#order_modal").modal("show");
    }
  });
  $(document).on("click", ".confirm-cancel-order", function (event) {
    event.preventDefault();

    let button = $(this);
    let orderId = button.data("id");

    // Заполняем номер заказа в модальном окне
    $("#order-number-to-cancel").text(orderId);

    // Показываем модальное окно
    $("#confirmCancelModal").modal("show");

    // Сохраняем ссылку на кнопку, чтобы позже отправить запрос
    window.currentOrderButton = button;
  });
  // Обработка клика на кнопку подтверждения в модальном окне
  $("#confirm-cancel-btn").on("click", function (event) {

        let currentButton = window.currentOrderButton;
        let orderId = currentButton.data('id');

    // Показываем загрузочный индикатор
    currentButton.text("Отмена...").prop("disabled", true);

    $.ajax({
      method: "GET",
      url: "/orders/cancel/" + orderId,
      success: function (response) {
        console.log("Заказ успешно отменён:", response);

        // Закрываем модальное окно
        $("#confirmCancelModal").modal("hide");

        // Скрываем кнопку "Отменить заказ"
        currentButton.closest(".confirm-cancel-order").hide();

        $(`span[data-id = "${orderId}"]`)
          .html("Отменен")
          .parent()
          .addClass("btn-danger")
          .removeClass("btn-primary");

        // Опционально: показать сообщение пользователю
        alert("Заказ успешно отменён!");
      },
      error: function (error) {
        console.error("Ошибка при отмене заказа:", error.responseText);
        button.text("Отменить заказ").prop("disabled", false);
      },
    });
  });
});
