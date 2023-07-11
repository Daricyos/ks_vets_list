import base64
import logging

from odoo import models, fields
import datetime

from .hisa import HisaAPI

_logger = logging.getLogger()


class KeyHisausapps(models.Model):
    _name = 'ks.hisa.key'
    _description = 'Ks Hisa Key'

    name = fields.Char()
    key = fields.Char()

    ruling_all_text = fields.Char(default=' ', )
    ruling_all_page = fields.Integer()
    ruling_all_page_size = fields.Integer()
    ruling_all_sort_by = fields.Char()
    ruling_all_sort_direction = fields.Integer()

    def button_get_ruling_all(self):
        self.ensure_one()
        api = HisaAPI(key=self.key, )
        params = {
            'text': self.ruling_all_text,
            'pageSize': self.ruling_all_page_size,
        }
        if self.ruling_all_sort_by:
            params['sortBy'] = self.ruling_all_sort_by
        if self.ruling_all_sort_direction:
            params['sortDirection'] = self.ruling_all_sort_direction
        res = api.get_ruling_all(params=params)
        total_pages = eval(res[1]['X-Pagination'])['totalPages']
        if total_pages:
            page = 0
            while page <= total_pages:
                params['page'] = page
                res = api.get_ruling_all(params=params)
                page += 1
                try:
                    self.load_rulings(res[0], api)
                except Exception as e:
                    _logger.info(e)

    def load_rulings(self, data, api):
        ruling_m = self.env['ks.hisa.vets']
        for item in data:
            data_to_create = {
                'vets_list_id': item['vetsListId'] if item['vetsListId'] is not None else None,
                'hisa_horse_id': item['hisaHorseId'] if item['hisaHorseId'] is not None else None,
                'location_id': item['locationId'] if item['locationId'] is not None else None,
                'regulatory_vet_id': item['regulatoryVetId'] if item['regulatoryVetId'] is not None else None,
                'required_diagnostic': item['requiredDiagnostic'] if item['requiredDiagnostic'] is not None else None,
                'required_diagnostic_complete_date': item['requiredDiagnosticCompleteDate'] if item['requiredDiagnosticCompleteDate'] is not None else None,
                'reason': item['reason'] if item['reason'] is not None else None,
                'days_on_list': item['daysOnList'] if item['daysOnList'] is not None else None,
                'date_placed_on_list': item['datePlacedOnList'] if item['datePlacedOnList'] is not None else None,
                'date_to_come_off_list': item['dateToComeOffList'] if item['dateToComeOffList'] is not None else None,
                'jog_past_date': item['jogPastDate'] if item['jogPastDate'] is not None else None,
                'workout_past_date': item['workoutPastDate'] if item['workoutPastDate'] is not None else None,
                'extensions_ids': [(6, 0, self.get_vets_extensions(item['extensions']))] if item['extensions'] is not None else None,
                'current_responsible_person_id': item['currentResponsiblePersonId'] if item['currentResponsiblePersonId'] is not None else None,
                'current_designated_owner': item['currentDesignatedOwner'] if item['currentDesignatedOwner'] is not None else None,
                'current_attending_vet': item['currentAttendingVet'] if item['currentAttendingVet'] is not None else None,
                'hisa_horse_name': item['hisaHorseName'] if item['hisaHorseName'] is not None else None,
                'location_name': item['locationName'] if item['locationName'] is not None else None,
                'is_enforced': item['isEnforced'] if item['isEnforced'] is not None else None,
                'tjc_id': item['tjcId'] if item['tjcId'] is not None else None,
                'release_date': item['releaseDate'] if item['releaseDate'] is not None else None,
                'eligible_to_work': item['eligibleToWork'] if item['eligibleToWork'] is not None else None,
                'other_state_reason': item['otherStateReason'] if item['otherStateReason'] is not None else None,
                'source_horse_medical_id': item['sourceHorseMedicalId'] if item['sourceHorseMedicalId'] is not None else None,
                'source_hisa_injury_id': item['sourceHisaInjuryId'] if item['sourceHisaInjuryId'] is not None else None,
                'is_reg_vet_clear_required': item['isRegVetClearRequired'] if item['isRegVetClearRequired'] is not None else None,
                'notes': item['notes'] if item['notes'] is not None else None,
            }
            rul_id = ruling_m.search([('vets_list_id', '=', item['vetsListId'])])
            if rul_id:
                rul_id.write(data_to_create)
            else:
                rul_id = ruling_m.create(data_to_create)
            is_horse_true = self.env['horse.name'].search(
                [('name', '=', data_to_create['hisa_horse_name']), ('id_horse_name', '=', data_to_create['hisa_horse_id'])],
                limit=1)
            if not is_horse_true:
                is_horse_true.create({
                    'name': data_to_create['hisa_horse_name'],
                    'id_horse_name': data_to_create['hisa_horse_id'],
                })
            horse_name_id = self.env['horse.name'].search([('id_horse_name', '=', rul_id.hisa_horse_id)], limit=1)
            if horse_name_id:
                rul_id.hisa_horse_full_name = horse_name_id.id

            is_location_true = self.env['location.name'].search(
                [('name', '=', data_to_create['location_name']), ('id_location_name', '=', data_to_create['location_id'])],
                limit=1)
            if not is_location_true:
                is_location_true.create({
                    'name': data_to_create['location_name'],
                    'id_location_name': data_to_create['location_id'],
                })
            location_name_id = self.env['location.name'].search([('id_location_name', '=', rul_id.location_id)], limit=1)
            if location_name_id:
                rul_id.location_full_name = location_name_id.id

    def get_vets_extensions(self, data):
        extensions_ids = []
        for item in data:
            extensions_create = {
                'extension_on': item['extensionOn'] if item['extensionOn'] is not None else None,
                'days': item['days'] if item['days'] is not None else None,
            }
            exten_id = self.env['ks.vets.list.extensions'].create(extensions_create)
            extensions_ids.append(exten_id.id)
        return extensions_ids
