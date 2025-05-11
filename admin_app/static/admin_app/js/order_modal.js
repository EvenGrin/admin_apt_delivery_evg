$(document).ready(function() {
    $('#order-table tbody tr').on('click', function() {
        const orderId = $(this).attr('data-order-id');
        ajaxOrderDetails(orderId);  // Запрашиваем детальную информацию о заказе
    });
});

// Функция для загрузки деталей заказа через AJAX
function ajaxOrderDetails(orderId) {
    $.ajax({
        url: `/order/${orderId}/`,
        method: 'GET',
        success: function(data) {
            // displayOrderDetails(response);  // Выводим полученные данные
            $('#orderModal').modal('show')
            $('#orderModal .modal-body').html(data)
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error(`Ошибка: ${textStatus}, ${errorThrown}`);
        }
    });
}

// Отображение полученных данных внутри модального окна
function displayOrderDetails(data) {
    $('.modal-body').html(`
        <strong>Номер заказа:</strong> ${data.order_id}<br/>
        <strong>Продукт:</strong> ${data.product_name}<br/>
        <strong>Цена:</strong> ${data.price}<br/>
        <strong>Количество:</strong> ${data.quantity}<br/>
        <strong>Общая сумма:</strong> ${data.total_amount}<br/>
        <strong>Дата оформления:</strong> ${data.created_at}
    `);
    $('#order-modal-id').text(data.order_id);
}