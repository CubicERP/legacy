openerp.account_bank_budget = function(instance) {

    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;
    var budget_post_customize_id={};

    instance.web.account.bankStatementReconciliation.include({

        init: function(parent, context) {
            this._super(parent, context);
            if (this.statement_ids){
                this.model_bank_statement.query(["budget_struct_id"])
                    .filter([['id', '=', this.statement_ids[0]]])
                    .first()
                    .then(function(result) {
                        budget_post_customize_id=result;
                    });
            }

            this.create_form_fields["budget_struct_id"] = {
                id: "budget_struct_id",
                index: 5,
                corresponding_property: "budget_struct_id",
                label: _t("Struct Budget"),
                required: false,
                tabindex: 15,
                constructor: instance.web.form.FieldMany2One,
                field_properties: {
                    relation: "account.budget.post",
                    string: _t("Struct Budget"),
                    type: "many2one",
                }
            };
        },

        start: function() {
            return this._super().then(function() {
            });
        },

        
    });
    instance.web.account.bankStatementReconciliationLine.include({
        
        prepareCreatedMoveLineForPersisting: function(line) {
            var dict = this._super(line);
            if (line.budget_struct_id) dict['budget_struct_id'] = line.budget_struct_id;
            if (dict["budget_struct_id"] !== undefined) delete dict["budget_struct_id"];
            return dict;
        },
        initializeCreateForm: function() {
            this._super();
            var self = this;

            if (budget_post_customize_id.budget_struct_id[0]!==undefined) {
                if (self.budget_struct_id_field) {
                    self.budget_struct_id_field.set("value", budget_post_customize_id.budget_struct_id[0]);
                };
            };
        },
        prepareCreatedMoveLineForPersisting: function(line) {
            var dict = this._super(line);
            dict['budget_struct_id'] = line.budget_struct_id;
            return dict;
        },
    });
};
