from odoo import fields, models


class StockScrap(models.Model):
    _inherit = "stock.scrap"

    mass_scrap_line_id = fields.Many2one(
        comodel_name="stock.scrap.mass.line", string="Mass Scrap Line", required=False, ondelete="set null"
    )
    mass_scrap_id = fields.Many2one(related="mass_scrap_line_id.mass_scrap_id", store=True)
