$(document).ready(function() {
    // Поиск блюд
    $('#mealSearch').on('input', function() {
        const searchTerm = $(this).val().toLowerCase();

        $('.meal-item').each(function() {
            const mealText = $(this).text().toLowerCase();

            if (mealText.includes(searchTerm) || searchTerm == '') {
                $(this).show();
            } else {
                $(this).hide();
            }
        });

        // Показываем/скрываем заголовки категорий
        $('.accordion-item').each(function() {
            const visibleMeals = $(this).find('.meal-item:visible').length;
            if (visibleMeals > 0 || searchTerm == '') {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    // Добавляем кнопку "Выбрать все" для каждой категории
    $('.accordion-header').each(function() {
        if (!$(this).find('.select-all').length) {
            const selectAllCheckbox = $('<input>', {
                type: 'checkbox',
                class: 'form-check-input select-all',
                css: { 'margin-left': '10px' }
            });

            const selectAllLabel = $('<label>', {
                class: 'form-check-label small ms-2',
                text: 'Выбрать все',
                css: { cursor: 'pointer' }
            });

            const container = $('<div>', {
                class: 'd-inline-block ms-2'
            }).append(selectAllCheckbox).append(selectAllLabel);

            $(this).find('.accordion-button').append(container);

            // Обработчик для "Выбрать все"
            selectAllCheckbox.on('change', function() {
                const categoryBody = $(this).closest('.accordion-header').next('.accordion-collapse');
                categoryBody.find('.meal-checkbox').prop('checked', $(this).prop('checked'));
            });
        }
    });

    // Закрытие модального окна после успешного добавления
    $('form', '#addMealsModal').on('submit', function(e) {
        console.log(123)
        e.preventDefault();
        const form = $(this);

        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function(data) {
                console.log(data)
                if (data.success) {
                    $('#addMealsModal').modal('hide');
                    location.reload(); // Перезагружаем страницу для обновления списка
                }
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });

    // Сброс поиска и чекбоксов при закрытии модального окна
    $('#addMealsModal').on('hidden.bs.modal', function() {
        $('#mealSearch').val('');
        $('.meal-item').show();
        $('.accordion-item').show();
        $('.meal-checkbox').prop('checked', false);
        $('.select-all').prop('checked', false);
    });
});