# 2025 Gusti Tammam

# noinspection PyUnresolvedReferences,SpellCheckingInspection
{
    "name": """Mass Scrap""",
    "summary": """Enhances the scrap process to allow scrapping multiple products at once.""",
    "category": "Warehouse",
    "version": "17.0.1.0.0",
    "development_status": "Alpha",  # Options: Alpha|Beta|Production/Stable|Mature
    "auto_install": False,
    "installable": True,
    "application": False,
    "author": "Gusti Tammam",
    "support": "dev@tammam.id",
    "website": "https://github.com/gustitammam/odoo-addons",
    "license": "LGPL-3",
    "images": ["publish/images/main_screenshot.png"],
    # "price": 10.00,
    # "currency": "USD",
    "depends": [
        # odoo addons
        "base",
        "stock_account",
        # third party addons
        # developed addons
    ],
    "data": [
        # group
        # 'security/res_groups.xml',
        # data
        "data/ir_sequence.xml",
        # global action
        # 'views/action.xml',
        # view
        "views/stock_scrap_mass_views.xml",
        # qweb template
        # wizard
        # report paperformat
        # 'data/report_paperformat.xml',
        # report/printout template
        # 'views/report/report_tmpl_name.xml',
        # 'views/report/printout_tmpl_name.xml',
        # report/printout action
        # 'views/action/action_report.xml',
        # onboarding action
        # 'views/action/action_onboarding.xml',
        # action menu
        "views/action/action_menu.xml",
        # action onboarding
        # 'views/action/action_onboarding.xml',
        # menu
        "views/menu.xml",
        # security
        "security/ir.model.access.csv",
        # 'security/ir.rule.csv',
        # data
    ],
}
