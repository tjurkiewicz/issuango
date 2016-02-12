$('input[type=checkbox][data-selector=true]').change(function() {
    var group = $(this).data('group');
    if ($(this).data('main')) {
        $('input[type=checkbox][data-selector=true][data-main=false][data-group='+group+']').prop('checked', this.checked);
    } else {
        if (!this.checked) {
            $('input[type=checkbox][data-selector=true][data-main=true][data-group='+group+']').prop('checked', this.checked);
        } else {
            /* If all selected, then select main selector */
            if ($('input[type=checkbox][data-selector=true][data-main=false][data-group='+group+']:checked').length ==
                $('input[type=checkbox][data-selector=true][data-main=false][data-group='+group+']').length) {
                $('input[type=checkbox][data-selector=true][data-main=true][data-group='+group+']').prop('checked', this.checked);
            }
        }
    }
});

//
//$('#{{id}}').change(function() {
//    var name = $(this).attr('name');
//    var checked = this.checked;
//
//    $('[name='+name+']:not(#{{id}})').prop('checked', checked);
//});