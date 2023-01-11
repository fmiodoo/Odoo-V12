import unittest
from odoo.tests import tagged
from odoo.tests.common import Form
from odoo import fields, Command
from odoo.addons.account.tests.test_account_move_out_refund import TestAccountMoveOutRefundOnchanges


def test_out_refund_line_onchange_currency_1_mod(self):
    move_form = Form(self.invoice)
    move_form.currency_id = self.currency_data['currency']
    move_form.save()

    self.assertInvoiceValues(self.invoice, [
        {
            **self.product_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 1000.0,
            'debit': 500.0,
        },
        {
            **self.product_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 200.0,
            'debit': 100.0,
        },
        {
            **self.tax_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 180.0,
            'debit': 90.0,
        },
        {
            **self.tax_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 30.0,
            'debit': 15.0,
        },
        {
            **self.term_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -1410.0,
            'credit': 705.0,
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
            'amount_currency': 1000.0,
            'debit': 333.33,
        },
        {
            **self.product_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 200.0,
            'debit': 66.67,
        },
        {
            **self.tax_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 180.0,
            'debit': 60.0,
        },
        {
            **self.tax_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 30.0,
            'debit': 10.0,
        },
        {
            **self.term_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -1410.0,
            'credit': 470.0,
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
            'amount_currency': 0.005,
            'debit': 0.0,
        },
        {
            **self.product_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 200.0,
            'debit': 66.67,
        },
        {
            **self.tax_line_vals_1,
            'price_unit': 30.0,
            'price_subtotal': 30.00,
            'price_total': 30.00,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 30.001,
            'debit': 10.0,
        },
        {
            **self.tax_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 30.0,
            'debit': 10.0,
        },
        {
            **self.term_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'price_unit': -260.01,
            'price_subtotal': -260.01,
            'price_total': -260.01,
            'amount_currency': -260.006,
            'credit': 86.67,
        },
    ], {
        **self.move_vals,
        'currency_id': self.currency_data['currency'].id,
        'date': fields.Date.from_string('2016-01-01'),
        'amount_untaxed': 200.005,
        'amount_tax': 60.001,
        'amount_total': 260.006,
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
            'amount_currency': 0.01,
            'debit': 0.01,
        },
        self.product_line_vals_2,
        {
            **self.tax_line_vals_1,
            'price_unit': 30.0,
            'price_subtotal': 30.0,
            'price_total': 30.0,
            'amount_currency': 30.0,
            'debit': 30.0,
        },
        self.tax_line_vals_2,
        {
            **self.term_line_vals_1,
            'price_unit': -260.01,
            'price_subtotal': -260.01,
            'price_total': -260.01,
            'amount_currency': -260.01,
            'credit': 260.01,
        },
    ], {
        **self.move_vals,
        'currency_id': self.company_data['currency'].id,
        'date': fields.Date.from_string('2016-01-01'),
        'amount_untaxed': 200.01,
        'amount_tax': 60.0,
        'amount_total': 260.01,
    })



TestAccountMoveOutRefundOnchanges.test_out_refund_line_onchange_currency_1 = test_out_refund_line_onchange_currency_1_mod
