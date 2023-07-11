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
    hisa_horse_name = fields.Char()
    horse_id_display = fields.Char(string='Display Horse ID', readonly=True, )
    hisa_horse_full_name = fields.Many2one(string='Horse ID', comodel_name='horse.name', readonly=False, searchable=True,
                                           options="{'no_create': True}")
    location_full_name = fields.Many2one(string='Location ID', comodel_name='location.name', readonly=False, searchable=True,
                                         options="{'no_create': True}")
    location_id_display = fields.Char(string='Display Location ID', readonly=True, )
    location_name = fields.Char()
    is_enforced = fields.Boolean()
    tjc_id = fields.Integer()
    release_date = fields.Char()
    eligible_to_work = fields.Char()
    other_state_reason = fields.Char()
    source_horse_medical_id = fields.Char()
    source_hisa_injury_id = fields.Char()
    is_reg_vet_clear_required = fields.Boolean()
    notes = fields.Char()

    @api.onchange('hisa_horse_full_name')
    def _onchange_horse_id(self):
        for obj in self:
            if obj.hisa_horse_full_name:
                obj.horse_id_display = obj.hisa_horse_full_name.id_horse_name
            else:
                obj.horse_id_display = ''

    @api.onchange('location_full_name')
    def _onchange_location_id(self):
        for obj in self:
            if obj.location_full_name:
                obj.location_id_display = obj.location_full_name.id_location_name
            else:
                obj.location_id_display = ''


class HorseName(models.Model):
    _name = 'horse.name'
    _rec_name = 'display_name'

    name = fields.Char()
    id_horse_name = fields.Char()
    display_name = fields.Char(compute='_compute_display_name')

    def _compute_display_name(self):
        for obj in self:
            obj.display_name = f'{obj.id_horse_name} ({obj.name})'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('id_horse_name', operator, name)]
        records = self.search(domain + args, limit=limit)
        return records.name_get()


class LocationName(models.Model):
    _name = 'location.name'
    _rec_name = 'display_name'

    name = fields.Char()
    id_location_name = fields.Char()
    display_name = fields.Char(compute='_compute_display_name')

    def _compute_display_name(self):
        for obj in self:
            obj.display_name = f'{obj.id_location_name} ({obj.name})'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('id_location_name', operator, name)]
        records = self.search(domain + args, limit=limit)
        return records.name_get()


class VetsListExtensions(models.Model):
    _name = 'ks.vets.list.extensions'
    _description = 'ks.vets.list.extensions'

    extension_on = fields.Char()
    days = fields.Integer()
