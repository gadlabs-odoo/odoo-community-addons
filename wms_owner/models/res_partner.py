from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_warehouse_owner = fields.Boolean('Is Warehouse Owner')
    owner_code = fields.Char('Owner Code', copy=False)
    billing_rules = fields.One2many('wms.billing.rule', 'owner_id', 'Billing Rules')
    storage_fee_rate = fields.Float('Storage Fee Rate (per day per unit)')
    inbound_fee = fields.Float('Inbound Handling Fee')
    outbound_fee = fields.Float('Outbound Handling Fee')
    min_charge = fields.Float('Minimum Charge')
    billing_cycle = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ], 'Billing Cycle', default='monthly')