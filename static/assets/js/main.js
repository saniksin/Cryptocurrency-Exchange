$(document).ready(function() {
    // Инициализация Select2 для выпадающих списков
    $('.select2').select2({
        templateResult: formatOption, // Функция для форматирования опций
        templateSelection: formatSelectedOption // Функция для форматирования выбранной опции
    });

    // Функция для форматирования опций с картинками
    function formatOption(option) {
        if (!option.id) {
            return option.text;
        }

        var optionImage = $(option.element).data('image');
        if (!optionImage) {
            return option.text;
        }

        var $option = $(
            '<div class="d-flex align-items-center">' +
            '<img class="mr-2" src="' + optionImage + '" alt="" style="height: 30px;" />' +
            '<span>' + option.text + '</span>' +
            '</div>'
        );

        return $option;
    }
  
    // Функция для форматирования выбранной опции
    function formatSelectedOption(option) {
        if (!option.id) {
            return option.text;
        }

        var optionImage = $(option.element).data('image');
        if (!optionImage) {
            return option.text;
        }

        var $option = $(
            '<div class="d-flex align-items-center">' +
            '<img class="mr-2" src="' + optionImage + '" alt="" style="height: 30px;" />' +
            '<span>' + option.text + '</span>' +
            '</div>'
        );

        return $option;
    }
});
