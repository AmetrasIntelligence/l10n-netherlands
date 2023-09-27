# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from . import model

from odoo import SUPERUSER_ID
from odoo.api import Environment


def _post_init(cr, _):
    env = Environment(cr, SUPERUSER_ID, {})
    # Here we define to clear connector logs after 730 hours by default
    env["ir.config_parameter"].sudo().set_param("partner_names_order", "first_last")
