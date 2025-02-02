from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockScrapMass(models.Model):
    _name = "stock.scrap.mass"
    _inherit = ["mail.thread"]
    _description = "Stock Scrap Mass"

    STATES = [("draft", "Draft"), ("done", "Done")]

    name = fields.Char(
        string="Reference", required=True, copy=False, readonly=True, index=True, default=lambda self: _("New")
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
        required=True,
        ondelete="restrict",
        default=lambda self: self.env.user,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        ondelete="restrict",
        default=lambda self: self.env.company,
    )
    date_done = fields.Datetime("Date", readonly=True)
    location_id = fields.Many2one(
        "stock.location",
        "Source Location",
        compute="_compute_location_id",
        store=True,
        required=True,
        precompute=True,
        domain="[('usage', '=', 'internal')]",
        check_company=True,
        readonly=False,
    )
    scrap_location_id = fields.Many2one(
        "stock.location",
        "Scrap Location",
        compute="_compute_scrap_location_id",
        store=True,
        required=True,
        precompute=True,
        domain="[('scrap_location', '=', True)]",
        check_company=True,
        readonly=False,
    )
    line_ids = fields.One2many(comodel_name="stock.scrap.mass.line", inverse_name="mass_scrap_id", string="Lines")
    state = fields.Selection(selection=STATES, string="Status", default="draft", readonly=True, tracking=True)

    def action_validate(self):
        self.ensure_one()

        if not self.line_ids:
            raise UserError(_("Please add some products to scrap."))

        self.line_ids.action_do_scrap()
        self.write(
            {
                "name": self.env["ir.sequence"].next_by_code("stock.scrap.mass") or _("New"),
                "state": "done",
                "date_done": self.line_ids[0].scrap_id.date_done,
            }
        )

    @api.depends("company_id")
    def _compute_location_id(self):
        groups = self.env["stock.warehouse"]._read_group(
            [("company_id", "in", self.company_id.ids)], ["company_id"], ["lot_stock_id:array_agg"]
        )
        locations_per_company = {
            company.id: lot_stock_ids[0] if lot_stock_ids else False for company, lot_stock_ids in groups
        }
        for scrap in self:
            scrap.location_id = locations_per_company[scrap.company_id.id]

    # noinspection DuplicatedCode
    @api.depends("company_id")
    def _compute_scrap_location_id(self):
        groups = self.env["stock.location"]._read_group(
            [("company_id", "in", self.company_id.ids), ("scrap_location", "=", True)], ["company_id"], ["id:min"]
        )
        locations_per_company = {company.id: stock_warehouse_id for company, stock_warehouse_id in groups}
        for scrap in self:
            scrap.scrap_location_id = locations_per_company[scrap.company_id.id]


class StockScrapMassLine(models.Model):
    _name = "stock.scrap.mass.line"
    _description = "Stock Scrap Mass Line"

    mass_scrap_id = fields.Many2one(
        comodel_name="stock.scrap.mass", string="Mass Scrap", required=False, ondelete="restrict", index=True
    )
    company_id = fields.Many2one(related="mass_scrap_id.company_id", store=True)
    product_id = fields.Many2one("product.product", "Product", required=True, check_company=True)
    product_uom_id = fields.Many2one(
        "uom.uom",
        "Unit of Measure",
        compute="_compute_product_uom_id",
        store=True,
        readonly=False,
        precompute=True,
        required=True,
        domain="[('category_id', '=', product_uom_category_id)]",
    )
    product_uom_category_id = fields.Many2one(related="product_id.uom_id.category_id")
    scrap_qty = fields.Float("Quantity", required=True, digits="Product Unit of Measure", default=1.0)
    scrap_id = fields.Many2one(comodel_name="stock.scrap", string="Related Scrap", readonly=True, ondelete="restrict")

    @api.depends("product_id")
    def _compute_product_uom_id(self):
        for line in self:
            line.product_uom_id = line.product_id.uom_id

    def action_do_scrap(self):
        for line in self:
            scrap = self.env["stock.scrap"].create(
                {
                    "product_id": line.product_id.id,
                    "scrap_qty": line.scrap_qty,
                    "location_id": line.mass_scrap_id.location_id.id,
                    "scrap_location_id": line.mass_scrap_id.scrap_location_id.id,
                    "company_id": line.company_id.id,
                    "mass_scrap_line_id": line.id,
                }
            )
            scrap.action_validate()
            line.scrap_id = scrap.id
