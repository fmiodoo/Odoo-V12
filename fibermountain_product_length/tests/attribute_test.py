# -*- coding: utf-8 -*-
import unittest
from odoo.tests import tagged
from odoo.addons.product.tests.test_product_attribute_value_config import TestProductAttributeValueConfig


@unittest.skip('Skip this test')
def skip_test(self):
    pass

'''
Skip these tests because of the new way we invoice the first invoices of
subscriptions
'''
TestProductAttributeValueConfig.test_get_first_possible_combination = skip_test

