import logging, json

from odoo import http
from odoo.http import request
from werkzeug.wrappers import Response

_logger = logging.getLogger(__name__)


class VetsListMod(http.Controller):
    # POST
    @http.route(
        type='json', csrf=False, website=True, cors='*', auth='public',
        methods=['POST'], route=['/ks_vets_list/update_vets/'], )

    def ks_update_vets(self, **kwargs):
        api_id = request.env['ks.api.key'].sudo()
        res = api_id.get_api_key()
        if not res['api_key']:
            data = json.dumps({'message': 'API key not correct'})
            response = Response(data, status=400, mimetype='application/json')
            return response
        vets_id = request.env['ks.hisa.vets'].sudo()
        items = kwargs.get('vets', [])
        for item in items:
            data_to_write = {
                'vets_list_id': item.get('vetsListId', False),  # char
                'hisa_horse_id': item.get('hisaHorseId', False),
                'location_id': item.get('locationId'),
                'regulatory_vet_id': item.get('regulatoryVetId'),
                'required_diagnostic': item.get('requiredDiagnostic'),
                'required_diagnostic_complete_date': item.get(
                    'requiredDiagnosticCompleteDate'),
                'reason': item.get('reason'),
                'days_on_list': item.get('daysOnList'),
                'date_placed_on_list': item.get('datePlacedOnList'),
                'date_to_come_off_list': item.get('dateToComeOffList'),
                'jog_past_date': item.get('jogPastDate'),
                'workout_past_date': item.get('workoutPastDate'),
                'extensions_ids': [(6, 0, request.env[
                    'ks.hisa.key'].sudo().get_vets_extensions(
                    item.get('extensions')))],
                'current_responsible_person_id': item.get(
                    'currentResponsiblePersonId'),
                'current_designated_owner': item.get('currentDesignatedOwner'),
                'current_attending_vet': item.get('currentAttendingVet'),
                'hisa_horse_name': item.get('hisaHorseName'),
                'location_name': item.get('locationName'),
                'is_enforced': item.get('isEnforced'),
                'tjc_id': item.get('tjcId'),
                'release_date': item.get('releaseDate'),
                'eligible_to_work': item.get('eligibleToWork'),
                'other_state_reason': item.get('otherStateReason'),
                'source_horse_medical_id': item.get('sourceHorseMedicalId'),
                'source_hisa_injury_id': item.get('sourceHisaInjuryId'),
                'is_reg_vet_clear_required': item.get('isRegVetClearRequired'),
                'notes': item.get('notes'),
            }
            vet_id = request.env['ks.hisa.vets'].sudo().search(
                [('vets_list_id', '=', data_to_write['vets_list_id'])],
                limit=1)
            vet_id.write(data_to_write)
        data = json.dumps({'message': 'success!'})
        response = Response(data, status=200, mimetype='application/json')
        return response
