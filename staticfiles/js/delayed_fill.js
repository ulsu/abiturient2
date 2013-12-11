$(function(){
    var $fresh_page_indicator = $('#fresh_page');
    var $fresh_page = false;

    if ($fresh_page_indicator.val() == '1') {
        $fresh_page_indicator.val('0');
        $fresh_page = true;
    }

    function is_page_fresh(){
        return $fresh_page;
    }

    $(document).ready(function(){
        function fill_empty(target) {
            var options = '<option value=""></option>';
            target.html(options);
            target.find('option:first').attr('selected', 'selected');
        }

        function fill_field_by_data(target, data, value){
            $.jStorage.set(target.attr('id'), data);
            var options = '<option value=""></option>';
            for (var i = 0; i < data.length; i++) {
                options += '<option'+ ((value && value==data[i].value)?' selected="selected"':'') +' value="' + data[i].value + '">' + data[i].display + '</option>';
            }
            var width = target.outerWidth();
            target.html(options);
            if (navigator.appVersion.indexOf("MSIE") != -1)
                target.width(width + 'px');

            if (!value) target.find('option:first').attr('selected', 'selected');
        }

        function fill_field(target, url, pk, val) {
            $.getJSON(url + pk + '/', function(j) {
                fill_field_by_data(target, j, val);
            })
        }

        $('select.chained').each(function() {
            var $parent = $('#' + $(this).data('parent-id')),
                $target = $(this),
                url = $(this).data('url');

            if (!is_page_fresh()){
                fill_field_by_data(
                    $target,
                    $.jStorage.get($target.attr('id')),
                    $.jStorage.get($target.attr('id') + '_value')
                );
            }

            $target.on('change', function(){
                $.jStorage.set($target.attr('id')+'_value', $target.val());
            });

            $parent.on('change', function() {
                var pk = $(this).val();
                if (!pk || pk == '') {
                    fill_empty($target);
                    $target.attr('disabled', 'disabled');
                } else {
                    fill_field($target, url, pk, $target.val());
                    $target.attr('disabled', false);
                }
                $target.val('').trigger('change');

            });
        });
    });


    $(document).ready(function(){
        function get_source(url, pk){
            return url + pk + '/';
        }

        $('input[type=text].chained').each(function() {
            var $parent = $('#' + $(this).data('parent-id')),
                $hidden = $('#' + $(this).data('hidden-id')),
                $target = $(this),
                url = $(this).data('url'),
                source;
            var parent_exists = !!$parent.length;

            if (!is_page_fresh())
                source = $.jStorage.get($target.attr('id') + '_source');
            else
            if (parent_exists)
                source = get_source(url, $parent.val());
            else
                source = url

            $target.autocomplete({
                minLength: 0,
                source: source,
                focus: function( event, ui ) {
                    $target.val( ui.item.display );
                    return false;
                },
                select: function( event, ui ) {
                    $target.val( ui.item.display );
                    $hidden.val( ui.item.value );
                    $hidden.trigger('change');
                    $target.trigger('change');
                    return false;

                },
                change: function( event, ui ) {
                    if(!ui.item){
                        $target.val( "" );
                        $hidden.val( "" ).change();
                        return false;
                    } else return true;
                }
            }) .data( "ui-autocomplete" )._renderItem = function( ul, item ) {
                return $( "<li>" )
                    .append( "<a>" + item.display + "</a>" )
                    .appendTo( ul );
            };

            if (parent_exists)
                $parent.on('change', function() {
                    var pk = $(this).val();
                    if (!pk || pk == '') {
                        $.jStorage.set($target.attr('id')+'_value', undefined);
                        $target.autocomplete('option', 'source', undefined);
                        $target.attr('disabled', 'disabled');
                    } else {
                        source = get_source(url, pk);
                        $.jStorage.set($target.attr('id')+'_value', source);
                        $target.autocomplete('option', 'source', source);
                        $target.attr('disabled', false);
                    }
                    $target.val('');
                    $hidden.val('').trigger('change');

                });
        });
    });



    $(document).ready(function(){
        $('select.dependent, input[type=text].dependent').each(function() {
            var $parent = $('#' + $(this).data('dependent-field')),
                $value = $(this).data('dependent-value'),
                $target = $(this);

            $parent.on('change', function() {
                $target.val('');
                if ($value)
                    $target.attr('disabled', $(this).val()!=$value);
                else
                    $target.attr('disabled', !$(this).val());
                $target.trigger('change');
            });
        });
    });
});


