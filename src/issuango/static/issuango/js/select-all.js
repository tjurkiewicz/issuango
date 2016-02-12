(function($) {
    $.fn.selectAll = function() {
        $('input', $(this)).change(function() {
            if ($(this).data('item')=="") {
                $('input:not([data-item=""])').prop('checked', this.checked);
            } else {
                if (!this.checked) {
                    $('input[data-item=""]').prop('checked', this.checked);
                } else {
                    /* If all selected, then select main selector */
                    if ($('input:checked:not([data-item=""])').length == $('input:not([data-item=""])').length) {
                        $('input[data-item=""]').prop('checked', this.checked);
                    }
                }
            }
        });
    }
})(window.jQuery);
