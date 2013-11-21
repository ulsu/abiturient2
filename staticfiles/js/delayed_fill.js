(function($) {
    $(document).ready(function(){
        function fill_empty(target, label) {
            options = '<option value="">' + label + '</option>';
            target.html(options);
            target.find('option:first').attr('selected', 'selected');
        }

        function fill_field(target, label, url, pk, parent_pk, initial_value) {
            var value = (pk)? pk : 0;
            $.getJSON(url + value + '/' + parent_pk + '/', function(j) {
                var options = '<option value="">' + label + '</option>';
                for (var i = 0; i < j.length; i++) {
                    options += '<option value="' + j[i].value + '">' + j[i].display + '</option>';
                }
                var width = target.outerWidth();
                target.html(options);
                if (navigator.appVersion.indexOf("MSIE") != -1)
                    target.width(width + 'px');
                target.find('option:first').attr('selected', 'selected');
            })
        }

        // find parent select and assign handlers
        $('select.kladr').each(function() {
            var $parent = $('#' + $(this).data('parent-id')),
                $target = $(this),
                url = $(this).data('url'),
                empty_label = $(this).data('empty-label'),
                accept_empty = $(this).data('accept-empty') == 'True';
            $parent.on('change', function() {
                var parent_disabled = this.disabled == true;
                var pk = $(this).val();
                var parent_pk = 0;
                if (pk == 0 && accept_empty && !parent_disabled){
                    var $grandparent = $('#' + $(this).data('parent-id'));
                    parent_pk = $grandparent.val();
                }

                if (!accept_empty && (!pk || pk == '')) {
                    fill_empty($target, empty_label);
                    $target.attr('disabled', true);
                    $target.trigger('change');
                } else {
                    console.log('filling ' + $target.attr('id'));
                    console.log('value: ' + pk);
                    $target.attr('disabled', false);
                    fill_field($target, empty_label, url, pk, parent_pk);
                    $target.trigger('change');
                }
            });
        });
    });
})(jQuery || django.jQuery);






(function($) {
    $(document).ready(function(){
        function fill_empty(target, label, autocomplete_values) {
            window[autocomplete_values] = [{
                'value': "",
                'label': label
            }];
            target.autocomplete('option', 'source', window[autocomplete_values]);
        }

        function clean_fields(target, hidden) {
            target.val('');
            hidden.val('');
        }



        function fill_field(target, label, url, pk, parent_pk, autocomplete_values) {
            var value = (pk)? pk : 0;

            $.getJSON(url + value + '/' + parent_pk + '/', function(j) {
                console.log(j.length);
                window[autocomplete_values] = [{
                    'value': "",
                    'label': label
                }];
                for (var i = 0; i < j.length; i++) {
                    window[autocomplete_values].push({
                        'value': j[i].value,
                        'label': j[i].display
                    });
                }
                target.autocomplete('option', 'source', window[autocomplete_values]);
            });
        }



        $('input[type=text].kladr').each(function() {
            var $parent = $('#' + $(this).data('parent-id')),
                $hidden = $('#' + $(this).data('hidden-id')),
                $target = $(this),
                autocomplete_values = $(this).data('values'),
                url = $(this).data('url'),
                empty_label = $(this).data('empty-label'),
                accept_empty = $(this).data('accept-empty') == 'True';

            $target.autocomplete({
                minLength: 0,
                source: window[autocomplete_values],
                focus: function( event, ui ) {
                    $target.val( ui.item.label );
                    return false;
                },
                select: function( event, ui ) {
                    $target.val( ui.item.label );
                    $hidden.val( ui.item.value );
                    return false;
                }
            })
                .data( "ui-autocomplete" )._renderItem = function( ul, item ) {
                return $( "<li>" )
                    .append( "<a>" + item.label + "</a>" )
                    .appendTo( ul );
            };

            $parent.on('change', function() {
                var parent_disabled = this.disabled == true;
                var pk = $(this).val();
                var parent_pk = 0;
                if (pk == 0 && accept_empty && !parent_disabled){
                    var $grandparent = $('#' + $(this).data('parent-id'));
                    parent_pk = $grandparent.val();
                }

                if (!accept_empty && (!pk || pk == '') || parent_disabled) {
                    fill_empty($target, empty_label, autocomplete_values);
                    $target.attr('disabled', true);
                } else {
                    fill_field($target, empty_label, url, pk, parent_pk, autocomplete_values);
                    $target.attr('disabled', false);
                }
                $target.trigger('change');
                clean_fields($target, $hidden);
            });
        });
    });
})(jQuery || django.jQuery);
