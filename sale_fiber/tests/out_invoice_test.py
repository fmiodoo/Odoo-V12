import unittest
from odoo.tests import tagged
from odoo.tests.common import Form
from odoo import fields, Command
from odoo.addons.account.tests.test_account_move_out_invoice import TestAccountMoveOutInvoiceOnchanges


def test_out_invoice_line_onchange_taxes_2_price_unit_tax_included_mod(self):
    tax_price_include = self.env['account.tax'].create({
        'name': 'Tax 5.5% price included',
        'amount': 5.5,
        'amount_type': 'percent',
        'price_include': True,
    })

    move_form = Form(self.invoice)
    move_form.invoice_line_ids.remove(1)
    with move_form.invoice_line_ids.edit(0) as line_form:
        line_form.price_unit = 2300
        line_form.tax_ids.add(tax_price_include)
    move_form.save()

    self.assertInvoiceValues(self.invoice, [
        {
            **self.product_line_vals_1,
            'price_unit': 2300.0,
            'price_subtotal': 2180.09,
            'price_total': 2627.01,
            'tax_ids': (self.product_a.taxes_id + tax_price_include).ids,
            'amount_currency': -2180.09,
            'credit': 2180.09,
        },
        {
            **self.tax_line_vals_1,
            'price_unit': 327.01,
            'price_subtotal': 327.01,
            'price_total': 327.01,
            'amount_currency': -327.01,
            'credit': 327.01,
        },
        {
            'name': tax_price_include.name,
            'product_id': False,
            'account_id': self.product_line_vals_1['account_id'],
            'partner_id': self.partner_a.id,
            'product_uom_id': False,
            'quantity': 1.0,
            'discount': 0.0,
            'price_unit': 119.91,
            'price_subtotal': 119.91,
            'price_total': 119.91,
            'tax_ids': [],
            'tax_line_id': tax_price_include.id,
            'currency_id': self.company_data['currency'].id,
            'amount_currency': -119.91,
            'debit': 0.0,
            'credit': 119.91,
            'date_maturity': False,
        },
        {
            **self.term_line_vals_1,
            'price_unit': -2627.01,
            'price_subtotal': -2627.01,
            'price_total': -2627.01,
            'amount_currency': 2627.01,
            'debit': 2627.01,
        },
    ], {
        **self.move_vals,
        'amount_untaxed': 2180.09,
        'amount_tax': 446.92,
        'amount_total': 2627.01,
    })

    move_form = Form(self.invoice)
    with move_form.invoice_line_ids.edit(0) as line_form:
        line_form.price_unit = -2300
    move_form.save()

    self.assertInvoiceValues(self.invoice, [
        {
            **self.product_line_vals_1,
            'price_unit': -2300.0,
            'price_subtotal': -2180.09,
            'price_total': -2627.01,
            'tax_ids': (self.product_a.taxes_id + tax_price_include).ids,
            'amount_currency': 2180.09,
            'debit': 2180.09,
            'credit': 0.0,
        },
        {
            **self.tax_line_vals_1,
            'price_unit': -327.01,
            'price_subtotal': -327.01,
            'price_total': -327.01,
            'amount_currency': 327.01,
            'debit': 327.01,
            'credit': 0.0,
        },
        {
            'name': tax_price_include.name,
            'product_id': False,
            'account_id': self.product_line_vals_1['account_id'],
            'partner_id': self.partner_a.id,
            'product_uom_id': False,
            'quantity': 1.0,
            'discount': 0.0,
            'price_unit': -119.91,
            'price_subtotal': -119.91,
            'price_total': -119.91,
            'tax_ids': [],
            'tax_line_id': tax_price_include.id,
            'currency_id': self.company_data['currency'].id,
            'amount_currency': 119.91,
            'debit': 119.91,
            'credit': 0.0,
            'date_maturity': False,
        },
        {
            **self.term_line_vals_1,
            'price_unit': 2627.01,
            'price_subtotal': 2627.01,
            'price_total': 2627.01,
            'amount_currency': -2627.01,
            'debit': 0.0,
            'credit': 2627.01,
        },
    ], {
        **self.move_vals,
        'amount_untaxed': -2180.09,
        'amount_tax': -446.92,
        'amount_total': -2627.01,
    })

    # == Multi-currencies ==

    move_form = Form(self.invoice)
    move_form.currency_id = self.currency_data['currency']
    with move_form.invoice_line_ids.edit(0) as line_form:
        line_form.price_unit = 2300
    move_form.save()

    self.assertInvoiceValues(self.invoice, [
        {
            **self.product_line_vals_1,
            'price_unit': 2300.0,
            'price_subtotal': 2180.095,
            'price_total': 2627.014,
            'tax_ids': (self.product_a.taxes_id + tax_price_include).ids,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -2180.095,
            'credit': 1090.05,
        },
        {
            **self.tax_line_vals_1,
            'price_unit': 327.014,
            'price_subtotal': 327.01,
            'price_total': 327.01,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -327.014,
            'credit': 163.51,
        },
        {
            'name': tax_price_include.name,
            'product_id': False,
            'account_id': self.product_line_vals_1['account_id'],
            'partner_id': self.partner_a.id,
            'product_uom_id': False,
            'quantity': 1.0,
            'discount': 0.0,
            'price_unit': 119.905,
            'price_subtotal': 119.91,
            'price_total': 119.91,
            'tax_ids': [],
            'tax_line_id': tax_price_include.id,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -119.905,
            'debit': 0.0,
            'credit': 59.95,
            'date_maturity': False,
        },
        {
            **self.term_line_vals_1,
            'price_unit': -2627.014,
            'price_subtotal': -2627.01,
            'price_total': -2627.01,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 2627.014,
            'debit': 1313.51,
        },
    ], {
        **self.move_vals,
        'currency_id': self.currency_data['currency'].id,
        'amount_untaxed': 2180.095,
        'amount_tax': 446.919,
        'amount_total': 2627.014,
    })

    move_form = Form(self.invoice)
    with move_form.invoice_line_ids.edit(0) as line_form:
        line_form.price_unit = -2300
    move_form.save()

    self.assertInvoiceValues(self.invoice, [
        {
            **self.product_line_vals_1,
            'price_unit': -2300.0,
            'price_subtotal': -2180.095,
            'price_total': -2627.014,
            'tax_ids': (self.product_a.taxes_id + tax_price_include).ids,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 2180.095,
            'debit': 1090.05,
            'credit': 0.0,
        },
        {
            **self.tax_line_vals_1,
            'price_unit': -327.014,
            'price_subtotal': -327.01,
            'price_total': -327.01,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 327.014,
            'debit': 163.51,
            'credit': 0.0,
        },
        {
            'name': tax_price_include.name,
            'product_id': False,
            'account_id': self.product_line_vals_1['account_id'],
            'partner_id': self.partner_a.id,
            'product_uom_id': False,
            'quantity': 1.0,
            'discount': 0.0,
            'price_unit': -119.905,
            'price_subtotal': -119.91,
            'price_total': -119.91,
            'tax_ids': [],
            'tax_line_id': tax_price_include.id,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 119.905,
            'debit': 59.95,
            'credit': 0.0,
            'date_maturity': False,
        },
        {
            **self.term_line_vals_1,
            'price_unit': 2627.014,
            'price_subtotal': 2627.01,
            'price_total': 2627.01,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -2627.014,
            'debit': 0.0,
            'credit': 1313.51,
        },
    ], {
        **self.move_vals,
        'currency_id': self.currency_data['currency'].id,
        'amount_untaxed': -2180.095,
        'amount_tax': -446.919,
        'amount_total': -2627.014,
    })

def test_out_invoice_line_onchange_currency_1_mod(self):
    move_form = Form(self.invoice.with_context(dudu=True))
    move_form.currency_id = self.currency_data['currency']
    move_form.save()

    self.assertInvoiceValues(self.invoice, [
        {
            **self.product_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -1000.0,
            'credit': 500.0,
        },
        {
            **self.product_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -200.0,
            'credit': 100.0,
        },
        {
            **self.tax_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -180.0,
            'credit': 90.0,
        },
        {
            **self.tax_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -30.0,
            'credit': 15.0,
        },
        {
            **self.term_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 1410.0,
            'debit': 705.0,
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
            'amount_currency': -1000.0,
            'credit': 333.33,
        },
        {
            **self.product_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -200.0,
            'credit': 66.67,
        },
        {
            **self.tax_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -180.0,
            'credit': 60.0,
        },
        {
            **self.tax_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -30.0,
            'credit': 10.0,
        },
        {
            **self.term_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': 1410.0,
            'debit': 470.0,
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
            'amount_currency': -200.0,
            'credit': 66.67,
        },
        {
            **self.tax_line_vals_1,
            'price_unit': 30.0,
            'price_subtotal': 30.00,
            'price_total': 30.00,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -30.001,
            'credit': 10.0,
        },
        {
            **self.tax_line_vals_2,
            'currency_id': self.currency_data['currency'].id,
            'amount_currency': -30.0,
            'credit': 10.0,
        },
        {
            **self.term_line_vals_1,
            'currency_id': self.currency_data['currency'].id,
            'price_unit': -260.01,
            'price_subtotal': -260.01,
            'price_total': -260.01,
            'amount_currency': 260.006,
            'debit': 86.67,
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
            'amount_currency': -0.01,
            'credit': 0.01,
        },
        self.product_line_vals_2,
        {
            **self.tax_line_vals_1,
            'price_unit': 30.0,
            'price_subtotal': 30.0,
            'price_total': 30.0,
            'amount_currency': -30.0,
            'credit': 30.0,
        },
        self.tax_line_vals_2,
        {
            **self.term_line_vals_1,
            'price_unit': -260.01,
            'price_subtotal': -260.01,
            'price_total': -260.01,
            'amount_currency': 260.01,
            'debit': 260.01,
        },
    ], {
        **self.move_vals,
        'currency_id': self.company_data['currency'].id,
        'date': fields.Date.from_string('2016-01-01'),
        'amount_untaxed': 200.01,
        'amount_tax': 60.0,
        'amount_total': 260.01,
    })


TestAccountMoveOutInvoiceOnchanges.test_out_invoice_line_onchange_currency_1 = test_out_invoice_line_onchange_currency_1_mod
TestAccountMoveOutInvoiceOnchanges.test_out_invoice_line_onchange_taxes_2_price_unit_tax_included = test_out_invoice_line_onchange_taxes_2_price_unit_tax_included_mod