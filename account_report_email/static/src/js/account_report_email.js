odoo.define('llacox_account_report_email.llacox_account_report_email', function (require) {
'use strict';

    var core = require('web.core');
    var rpc = require('web.rpc')
    var account_report = require('account_reports.account_report');
    var account_report_followup = require('account_reports.account_report_followup');
    
    account_report_followup.include({
        events: _.defaults({
            'click .o_account_reports_subject': 'edit_subject',
            'click .js_account_report_save_subject': 'save_subject',
        }, account_report_followup.prototype.events),
        edit_subject: function(e) {
            var $inputSubject = $(e.target).parents('.o_account_reports_body').find('input');
            $(e.target).parents('.o_account_reports_body').find('.o_account_reports_subject_edit').show();
            $(e.target).parents('.o_account_reports_body').find('.o_account_reports_subject').hide();
        },
        save_subject: function(e) {
            var self = this;
            var text = $(e.target).prevAll("input[type=text]").val();
            var $input = $(e.target).prevAll("input[type=text]");
            $(".reportSubject").html(text);
            return this._rpc({
                    model: 'account.report.manager',
                    method: 'write',
                    args: [this.report_manager_id, {subject: text}],
                    context: this.odoo_context,
                })
                .then(function(result){
                    self.$el.find('.o_account_reports_subject_edit').hide();
                    self.$el.find('.o_account_reports_subject').show();
                });
        },
    });
});


