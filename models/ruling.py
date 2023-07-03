import logging

from odoo import models, fields, api

_logger = logging.getLogger()


class KeyHisausappsVets(models.Model):
    _name = 'ks.hisa.vets'
    _description = 'Ks Vets List'
    _rec_name = 'vets_list_id'

    vets_list_id = fields.Char(string='Vets List ID')
    hisa_horse_id = fields.Char(string='Horse ID')
    location_id = fields.Char()
    regulatory_vet_id = fields.Char()
    required_diagnostic = fields.Char()
    required_diagnostic_complete_date = fields.Char()
    reason = fields.Char()
    days_on_list = fields.Integer()
    date_placed_on_list = fields.Date()
    date_to_come_off_list = fields.Date()
    jog_past_date = fields.Date()
    workout_past_date = fields.Date()
    extensions_ids = fields.Many2many(comodel_name='ks.vets.list.extensions')
    current_responsible_person_id = fields.Char()
    current_designated_owner = fields.Char()
    current_attending_vet = fields.Char()
    is_enforced = fields.Boolean()
    tjc_id = fields.Integer()
    release_date = fields.Char()
    eligible_to_work = fields.Char()
    other_state_reason = fields.Char()
    source_horse_medical_id = fields.Char()
    source_hisa_injury_id = fields.Char()
    is_reg_vet_clear_required = fields.Boolean()
    notes = fields.Char()


class VetsListExtensions(models.Model):
    _name = 'ks.vets.list.extensions'
    _description = 'ks.vets.list.extensions'

    extension_on = fields.Char()
    days = fields.Integer()
