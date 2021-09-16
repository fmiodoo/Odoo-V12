# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Users(models.Model):
    _inherit = 'res.users'

    discount_limit = fields.Float('Discount limit')
    approver_ids = fields.Many2many('res.users', 'users_approver_rel', 'user_id1', 'user_id2', string='Approver')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirm_so = fields.Boolean('Allow to confirm sale order', default=True, compute='_compute_confirm_so', store=True, readonly=True)
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('wait', 'Waiting for Approval'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('approved', 'SO is Approved'),
        ('rejected', 'SO is Rejected')
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    show_authorization = fields.Boolean(string='Authorized?', compute='_compute_show_authorization')

    def _compute_show_authorization(self):
        for order in self:
            if self.env.user in order.user_id.approver_ids:
                order.show_authorization = True
            else:
                order.show_authorization = False

    @api.depends('order_line.discount')
    def _compute_confirm_so(self):
        for order in self:
            order.confirm_so = False if order.order_line.filtered(lambda o: o.discount > order.user_id.discount_limit) else True
            if order.confirm_so and order.state in ('wait', 'rejected'):
                order.state = 'draft'

    def action_quotation_send(self):
        if self.state == 'approved' or self.confirm_so == True:
            return super(SaleOrder, self).action_quotation_send()
        else:
            if self.confirm_so == False:
                if self.state in ('draft', 'sent'):
                    self.write({'state': 'wait'})
                    return

    def action_confirm(self):
        if self.state == 'approved' or self.confirm_so == True:
            return super(SaleOrder, self).action_confirm()
        else:
            if self.confirm_so == False:
                if self.state in ('draft', 'sent'):
                    self.write({'state': 'wait'})
                    return

    def action_request_discout_email_send(self):
        if self.confirm_so:
            self.action_confirm()
        else:
            self.write({'state': 'wait'})
            template = self.env.ref('fiber_sale_discount.email_template_sale_discount_approval', raise_if_not_found=False)
            res = self.env['res.users'].search_read([('id', 'in', self.user_id.approver_ids.ids)], ['email'])
            emails = set(r['email'] for r in res if r.get('email'))
            email_values = {
                'email_to': ','.join(emails)
            }
            if template and self.env.user.email and self.id:
                template.with_context(is_reminder=True).send_mail(
                    self.id,
                    force_send=True,
                    raise_exception=False,
                    email_values=email_values,
                    notif_layout="mail.mail_notification_paynow")
                return {'toast_message': _("A sample email has been sent to %s.") % self.env.user.email}

    def action_authorize_discout_approve_email_send(self):
        if (self.env.user in self.user_id.approver_ids):
            template = self.env.ref('fiber_sale_discount.email_template_sale_discount_approve', raise_if_not_found=False)

            if template and self.env.user.email and self.id:
                template.with_context(is_reminder=True).send_mail(
                    self.id,
                    force_send=True,
                    raise_exception=False,
                    email_values={'recipient_ids': []},
                    notif_layout="mail.mail_notification_paynow")
                self.write({'confirm_so': True, 'state': 'approved'})
                return {'toast_message': _("A sample email has been sent to %s.") % self.env.user.email}
        else:
            raise ValidationError(_("You can't approve/reject the discount. Only approver has this rights."))

    def action_authorize_discout_reject_email_send(self):
        if (self.env.user in self.user_id.approver_ids):
            template = self.env.ref('fiber_sale_discount.email_template_sale_discount_reject', raise_if_not_found=False)

            if template and self.env.user.email and self.id:
                template.with_context(is_reminder=True).send_mail(
                    self.id,
                    force_send=True,
                    raise_exception=False,
                    email_values={'recipient_ids': []},
                    notif_layout="mail.mail_notification_paynow")
                self.write({'state': 'rejected'})
                return {'toast_message': _("A sample email has been sent to %s.") % self.env.user.email}
        else:
            raise ValidationError(_("You can't approve/reject the discount. Only approver has this rights."))


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('discount')
    def _onchange_discount(self):
        for line in self:
            if line.discount > line.order_id.user_id.discount_limit:
                warning = {
                    'title': 'Discount warning',
                    'message': 'The discount is higher than the allowed discount.',
                }
                return {'warning': warning}
