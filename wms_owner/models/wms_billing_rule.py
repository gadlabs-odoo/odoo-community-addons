from odoo import models, fields, api
from odoo.exceptions import ValidationError


class WmsBillingRule(models.Model):
    _name = 'wms.billing.rule'
    _description = 'WMS Billing Rule'

    name = fields.Char('Rule Name', required=True)
    owner_id = fields.Many2one('wms.owner', 'Owner', required=True)
    operation_type = fields.Selection([
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
        ('storage', 'Storage'),
        ('value_added', 'Value Added Service'),
        ('special_handling', 'Special Handling'),
        ('pick_pack', 'Pick & Pack'),
        ('palletizing', 'Palletizing'),
        ('repackaging', 'Repackaging'),
    ], 'Operation Type', required=True)
    service_type = fields.Char('Service Type')
    unit_price = fields.Float('Unit Price', required=True)
    price_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('per_unit', 'Per Unit'),
        ('per_kg', 'Per KG'),
        ('per_cbm', 'Per CBM'),
        ('per_pallet', 'Per Pallet'),
        ('per_hour', 'Per Hour'),
    ], 'Price Type', required=True, default='per_unit')
    min_charge = fields.Float('Minimum Charge')
    calculation_basis = fields.Selection([
        ('quantity', 'Quantity'),
        ('weight', 'Weight'),
        ('volume', 'Volume'),
        ('time', 'Time'),
        ('pallet', 'Pallet'),
        ('order', 'Order'),
    ], 'Calculation Basis')
    active = fields.Boolean('Active', default=True)

    @api.constrains('unit_price')
    def _check_unit_price_positive(self):
        for rule in self:
            if rule.unit_price < 0:
                raise ValidationError("Unit price must be positive.")