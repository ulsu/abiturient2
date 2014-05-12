(function (e) {
    "use strict";
    var t = "formset";
    var n = function (r, i) {
        var s = this;
        this.opts = e.extend({}, n.defaults, i);
        this.$formset = e(r);
        this.$emptyForm = this.$formset.find(this.opts.emptyForm);
        this.$body = this.$formset.find(this.opts.body);
        this.$add = this.$formset.find(this.opts.add);
        this.formsetPrefix = e(r).data("formset-prefix");
        this.addForm = e.proxy(this, "addForm");
        this.$add.click(this.addForm);
        this.$body.find(this.opts.form).each(function (t, n) {
            var r = e(n);
            s.bindForm(e(this), t)
        });
        this.$formset.data(t, this)
    };
    n.defaults = {
        form: "[data-formset-form]",
        emptyForm: "script[type=form-template][data-formset-empty-form]",
        body: "[data-formset-body]",
        add: "[data-formset-add]",
        deleteButton: "[data-formset-delete-button]",
        upButton: "[data-formset-up-button]",
        downButton: "[data-formset-down-button]",
        order: "[data-formset-order]"
    };

    n.prototype.addForm = function () {
        var t = this.formCount();

        if (this.getActiveFormsCount() >= this.getMaxForms())
            return false;
        this.formCount(t + 1);
        var n = this.$emptyForm.html().replace(new RegExp("__prefix__", "g"), t).replace(new RegExp("<\\\\/script>", "g"), "</script>");
        var r = e(n);
        this.$body.append(r);
        this.bindForm(r, t);
        r.slideUp(0);
        this.renderControls(this);
        r.addClass('display');
        r.toggle();
        bind_stuff();
        console.log(r.previousSibling);
        while (r.previousSibling){
            r.parentNode.insertBefore(r, r.previousSibling);
        }
        return r
    };


    n.prototype.renderControls = function(form) {
        var items = form.$body.children('.display');
        var up, down, order;
        for (var i=0; i<items.length; i++){
            up = $(items[i]).find(form.opts.upButton);
            down = $(items[i]).find(form.opts.downButton);
            order = $(items[i]).find(form.opts.order);
            order.val(i+1);
            if (up.length && down.length){
                if (items.length == 1){
                    up.css('display', 'none');
                    down.css('display', 'none');
                } else {
                    switch (i){
                        case 0:
                            $(items[i]).addClass('first');
                            $(items[i]).removeClass('last');
                            break;
                        case items.length-1:
                            $(items[i]).addClass('last');
                            $(items[i]).removeClass('first');
                            break;
                        default:
                            $(items[i]).removeClass('first');
                            $(items[i]).removeClass('last');
                            break;
                    }
                }
            }
        }
    };


    n.prototype.bindForm = function (e, n) {
        var renderControls = this.renderControls;
        var form = this;

        var r = this.formsetPrefix + "-" + n;
        e.data(t + "__formPrefix", r);
        var s = e.find(this.opts.deleteButton);
        if (s.length) {
            var i = e.find("[name=" + r + "-DELETE]");
            s.bind("click", function () {
                e.removeClass('display');
                e.addClass('hidden');
                var el = e[0];
                while (el.nextSibling) {
                    el.parentNode.insertBefore(el.nextSibling, el);
                }
                i.attr("checked", true);
                renderControls(form);
            });
            if (i.is(":checked")) {
                e.slideUp(0);
                renderControls(form);
            }
        }



        s = e.find(this.opts.upButton);
        if (s.length) {
            s.bind("click", function () {
                var el = e[0];
                el.parentNode.insertBefore(el, el.previousSibling);
                renderControls(form);
            });
        }

        s = e.find(this.opts.downButton);
        if (s.length) {
            s.bind("click", function () {
                var el = e[0];
                el.parentNode.insertBefore(el.nextSibling, el);
                renderControls(form);
            });
        }
        this.renderControls(this);
    };

    n.prototype.managementForm = function (e) {
        return this.$formset.find("[name=" + this.formsetPrefix + "-" + e + "]")
    };

    n.prototype.formCount = function () {
        var e = this.managementForm("TOTAL_FORMS");
        if (arguments.length) {
            e.val(arguments[0]);
            return this
        } else {
            return parseInt(e.val(), 10) || 0
        }
    };

    n.prototype.getActiveFormsCount = function () {
        return this.$body.children('.display').length;
    };

    n.prototype.getMaxForms = function () {
        var e = this.managementForm("MAX_NUM_FORMS");
        return parseInt(e.val(), 10) || 0
    };

    n.getOrCreate = function (r, i) {
        var s = e(r).data(t);
        if (!s) {
            s = new n(r, i)
        }
        return s
    };

    e.fn[t] = function () {
        var t, r, i;
        if (arguments.length === 0 || arguments.length === 1 && e.type(arguments[0]) != "string") {
            t = arguments[0];
            return this.each(function () {
                return n.getOrCreate(this, t)
            })
        }
        r = arguments[0];
        i = e.makeArray(arguments).slice(1);
        if (r in n) {
            i.unshift(this);
            return n[r].apply(n, i)
        } else {
            throw new Error("Unknown function call " + r + " for $.fn.formset")
        }
    }
})(jQuery);