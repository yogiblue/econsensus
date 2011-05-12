#-*- coding: utf-8 -*-

"""
Tests for the public website part of the OpenConsent project
"""

from __future__ import absolute_import

import logging
import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse

import openconsent.publicweb
import openconsent.publicweb.views
from openconsent.publicweb.models import Decision
from openconsent.publicweb.forms import DecisionForm

import tinymce.widgets
import django_tables

class PublicWebsiteTest(TestCase):
    # fixtures = ['submission_test_data.json', 'foobar', 'indicator_tests.yaml']
    
    def setUp(self):
        # self.foobar = Agency.objects.get(agency="Foobar")
        # self.mozambique = Country.objects.get(country="Mozambique")
        pass

    def get(self, view_function, **view_args):
        return self.client.get(reverse(view_function, kwargs=view_args))
    
    def test_get_homepage(self):
        response = self.get(openconsent.publicweb.views.home_page)
        self.assertEqual(list(Decision.objects.all()),
            list(response.context['decisions']))
    
    def test_decision_add_page(self):
        """
        Test error conditions for the add decision page. 
        """
        path = reverse(openconsent.publicweb.views.decision_add_page)
    
        # Test that the decision add view returns an empty form
        response = self.client.get(path)
        form = DecisionForm()
        self.assertEqual(form.as_p(),
            response.context['decision_form'].as_p())
    
        # Test that the decision add view validates and rejects and empty post
        response = self.client.post(path, dict())
        self.assertFalse(form.is_valid())   # validates the form and adds error messages
        self.assertEqual(form.as_p(),
            response.context['decision_form'].as_p())
        
        # Test that providing a short name is enough to complete the form,
        # save the object and send us back to the home page
        response = self.client.post(path, {'short_name': 'Feed the dog'},
            follow=True)
        self.assertRedirects(response,
            reverse(openconsent.publicweb.views.home_page),
            msg_prefix=response.content)

    def assert_decision_form_field_uses_tinymce_widget(self, field):
        form = DecisionForm()
        
        self.assertEquals(tinymce.widgets.TinyMCE,
            type(form.fields[field].widget))
    
        mce_attrs = form._meta.widgets[field].mce_attrs
        # check the MCE widget is set to advanced theme with our preferred buttons
        self.assertEquals({'theme': 'advanced',
            'theme_advanced_buttons1': 'bold,italic,underline,link,unlink,' + 
                'bullist,blockquote,undo',
            'theme_advanced_buttons3': '',
            'theme_advanced_buttons2': ''}, mce_attrs)
    
    def test_decision_form_concerns_field_uses_tinymce_widget(self):
        self.assert_decision_form_field_uses_tinymce_widget('concerns')

    def test_decision_form_description_field_uses_tinymce_widget(self):
        self.assert_decision_form_field_uses_tinymce_widget('description')
    
    def test_decisions_table_is_an_instance_of_model_table(self):
        """
        The decisions table is represented using django_tables.ModelTable.
        """
        response = self.get(openconsent.publicweb.views.home_page)
        decisions_table = response.context['decisions']
        self.assertTrue(isinstance(decisions_table, django_tables.ModelTable))
    
    def assert_decisions_table_sorted_by_date_column(self, column):
        # Create test decisions in reverse date order. 
        for i in range(5, 0, -1):
            decision = Decision(short_name='Decision %d' % i)
            setattr(decision, column, datetime.date(2001, 3, i))
            decision.save()
            
        response = self.client.get(reverse(openconsent.publicweb.views.home_page),
            data=dict(sort=column))
        decisions_table = response.context['decisions']    
        
        # Check that decision rows are returned in normal order
        rows = list(decisions_table.rows)
        for i in range(1, 6):
            self.assertEquals(datetime.date(2001, 3, i), getattr(rows[i-1].data, column))
    
    def test_decisions_table_rows_can_be_sorted_by_review_date(self):
        self.assert_decisions_table_sorted_by_date_column('review_date')
        
    def test_descisions_table_rows_can_be_sorted_by_decided_date(self):
        self.assert_decisions_table_sorted_by_date_column('decided_date')
        