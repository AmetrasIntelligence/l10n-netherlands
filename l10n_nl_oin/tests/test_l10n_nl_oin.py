# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestOin(TransactionCase):
    def setUp(self):
        super().setUp()

        self.partner_oin = self.env["res.partner"].create(
            {
                "name": "Partner with OIN",
                "is_company": True,
                "company_id": self.env.company.id,
                "country_id": self.env.ref("base.nl").id,
                "company_type": "company",
            }
        )

    def test_01_oin_not_valid(self):
        self.partner_oin.l10n_nl_oin = "123"
        res = self.partner_oin.onchange_nl_oin()
        self.assertEqual(self.partner_oin.l10n_nl_oin, "123")
        warning = res.get("warning")
        self.assertTrue(warning)
        message = warning.get("message")
        self.assertTrue(message)
        msg_txt = "The OIN you entered (123) is not valid."
        self.assertEqual(message, msg_txt)
        title = warning.get("title")
        self.assertTrue(title)
        self.assertEqual(title, "Warning!")

    def test_02_oin_valid(self):
        self.partner_oin.l10n_nl_oin = "12345678901234567890"
        res = self.partner_oin.onchange_nl_oin()
        self.assertEqual(self.partner_oin.l10n_nl_oin, "12345678901234567890")
        warning = res.get("warning")
        self.assertFalse(warning)

    def test_03_oin_another_partner(self):
        new_partner_oin = self.env["res.partner"].create(
            {
                "name": "Partner with OIN - NEW",
                "is_company": True,
                "l10n_nl_oin": "12345678901234567890",
                "company_id": self.env.company.id,
            }
        )
        self.partner_oin.l10n_nl_oin = "12345678901234567890"
        res = self.partner_oin.onchange_nl_oin()
        self.assertTrue(res.get("warning"))
        warning = new_partner_oin._warn_oin_existing()
        message = warning.get("message")
        self.assertTrue(message)
        msg_txt = (
            "Another partner (Partner with OIN - NEW) has the same OIN "
            "(12345678901234567890)."
        )
        self.assertEqual(message, msg_txt)
        self.assertEqual(message, res["warning"]["message"])
        title = warning.get("title")
        self.assertTrue(title)
        self.assertEqual(title, "Warning!")
        self.assertEqual(title, res["warning"]["title"])
