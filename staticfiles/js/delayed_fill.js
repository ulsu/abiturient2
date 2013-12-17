var $fresh_page = false;

$(function(){
    var $fresh_page_indicator = $('#fresh_page');
    if ($fresh_page_indicator.val() == '1') {
        $fresh_page_indicator.val('0');
        $fresh_page = true;
    }
});

function is_page_fresh(){
    return $fresh_page;
}

$(function(){
    bind_stuff();
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


function bind_stuff(){
    $(function(){
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
                url = $(this).data('url'),
                storage_id = $target.attr('id');


            if (!is_page_fresh() && $.jStorage.get(storage_id, false)){
                fill_field_by_data(
                    $target,
                    $.jStorage.get(storage_id),
                    $.jStorage.get(storage_id + '_value')
                );
            } else {
                $.jStorage.deleteKey(storage_id);
                $.jStorage.deleteKey(storage_id + '_value');
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
    $(function(){
        function fill_empty(target) {
            target.html('');
            target.css('display','none');
        }

        function fill_field_by_data(target, data, value, item_prefix){
            target.css('display','');
//            $.jStorage.set(target.attr('id'), data);
            var checkboxes = '';
            for (var i = 0; i < data.length; i++) {
                checkboxes += '<li>' +
                    '<label for="'+item_prefix+'_'+i+'">' +
                    '<input type="checkbox" id="'+item_prefix+'_'+i+'" name="'+item_prefix+'"'+ ((value && value==data[i].value)?' checked="checked"':'') +' value="' + data[i].value + '"> ' + data[i].display + '</label></li>';
            }
            var width = target.outerWidth();
            target.html(checkboxes);
            if (navigator.appVersion.indexOf("MSIE") != -1)
                target.width(width + 'px');

            if (!value) target.find('option:first').attr('selected', 'selected');
        }

        function fill_field(target, url, pk, val, item_prefix) {
            $.getJSON(url + pk + '/', function(j) {
                fill_field_by_data(target, j, val, item_prefix);
            })
        }

        $('ul.chained').each(function() {
            var $parent = $('#' + $(this).data('parent-id')),
                $target = $(this),
                url = $(this).data('url'),
                item_prefix = $(this).data('item-prefix'),
                storage_id = $target.attr('id');

            if (!is_page_fresh() && $.jStorage.get(storage_id, false)){
                fill_field_by_data(
                    $target,
                    $.jStorage.get(storage_id),
                    $.jStorage.get(storage_id + '_value')
                );
            } else {
                $.jStorage.deleteKey(storage_id);
                $.jStorage.deleteKey(storage_id + '_value');
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
                    fill_field($target, url, pk, $target.val(), item_prefix);
                    $target.attr('disabled', false);
                }
                $target.val('').trigger('change');

            });
        });
    });
    $(function(){
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
                source = url;

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
    $(function(){
        console.log(is_page_fresh());
    });
}


