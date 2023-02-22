import unittest
from odoo.tests import tagged
from odoo.tests.common import Form
from odoo import fields, Command
from odoo.addons.account.tests.test_account_move_in_refund import TestAccountMoveInRefundOnchanges


def test_in_refund_line_onchange_currency_1_mod(self):
    move_form = Form(self.invoice)
    move_form.currency_id = self.currency_data['currency']
    move_form.save()

    self.assertInvoiceValues(self.invoice, [
        {
            **self.product_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -800.0,
            'credit': 400.0,
        },
        {
            **self.product_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -160.0,
            'credit': 80.0,
        },
        {
            **self.tax_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -144.0,
            'credit': 72.0,
        },
        {
            **self.tax_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -24.0,
            'credit': 12.0,
        },
        {
            **self.term_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 1128.0,
            'debit': 564.0,
        },
    ], {
        **self.move_vals,
        'currency_id': self.currency_data['currency'].id,
    })

    move_form = Form(self.invoice)
    # Change the date to get another rate: 1/3 instead of 1/2.
    move_form.date = fields.Date.from_string('2016-01-01')
    move_form.save()

    self.assertInvoiceValues(self.invoice, [
        {
            **self.product_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -800.0,
            'credit': 266.67,
        },
        {
            **self.product_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -160.0,
            'credit': 53.33,
        },
        {
            **self.tax_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -144.0,
            'credit': 48.0,
        },
        {
            **self.tax_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -24.0,
            'credit': 8.0,
        },
        {
            **self.term_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 1128.0,
            'debit': 376.0,
        },
    ], {
        **self.move_vals,
        'currency_id': self.currency_data['currency'].id,
        'date': fields.Date.from_string('2016-01-01'),
    })

    move_form = Form(self.invoice)
    with move_form.invoice_line_ids.edit(0) as line_form:
        # 0.045 * 0.1 = 0.0045. As the foreign currency has a 0.001 rounding,
        # the result should be 0.005 after rounding.
        line_form.quantity = 0.1
        line_form.price_unit = 0.045
    move_form.save()

    self.assertInvoiceValues(self.invoice, [
        {
            **self.product_line_vals_1,
            'quantity': 0.1,
            'price_unit': 0.05,
            'price_subtotal': 0.005,
            'price_total': 0.006,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -0.005,
            'credit': 0.0,
        },
        {
            **self.product_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -160.0,
            'credit': 53.33,
        },
        {
            **self.tax_line_vals_1,
            'price_unit': 24.0,
            'price_subtotal': 24.00,
            'price_total': 24.00,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -24.001,
            'credit': 8.0,
        },
        {
            **self.tax_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -24.0,
            'credit': 8.0,
        },
        {
            **self.term_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'price_unit': -208.01,
            'price_subtotal': -208.01,
            'price_total': -208.01,
            'amount_currency': 208.006,
            'debit': 69.33,
        },
    ], {
        **self.move_vals,
        'currency_id': self.currency_data['currency'].id,
        'date': fields.Date.from_string('2016-01-01'),
        'amount_untaxed': 160.005,
        'amount_tax': 48.001,
        'amount_total': 208.006,
    })

    # Exit the multi-currencies.
    move_form = Form(self.invoice)
    move_form.currency_id = self.company_data['currency']
    move_form.save()

    self.assertInvoiceValues(self.invoice, [
        {
            **self.product_line_vals_1,
            'quantity': 0.1,
            'price_unit': 0.05,
            'price_subtotal': 0.01,
            'price_total': 0.01,
            'amount_currency': -0.01,
            'credit': 0.01,
        },
        self.product_line_vals_2,
        {
            **self.tax_line_vals_1,
            'price_unit': 24.0,
            'price_subtotal': 24.0,
            'price_total': 24.0,
            'amount_currency': -24.0,
            'credit': 24.0,
        },
        self.tax_line_vals_2,
        {
            **self.term_line_vals_1,
            'price_unit': -208.01,
            'price_subtotal': -208.01,
            'price_total': -208.01,
            'amount_currency': 208.01,
            'debit': 208.01,
        },
    ], {
        **self.move_vals,
        'currency_id': self.company_data['currency'].id,
        'date': fields.Date.from_string('2016-01-01'),
        'amount_untaxed': 160.01,
        'amount_tax': 48.0,
        'amount_total': 208.01,
    })



TestAccountMoveInRefundOnchanges.test_in_refund_line_onchange_currency_1 = test_in_refund_line_onchange_currency_1_mod