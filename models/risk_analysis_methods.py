# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from ast import literal_eval


class RiskMethod(models.Model):

    _name = 'risk.analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'OHS Risk Analysis'
    _rec_name = 'company_id'

    company_id = fields.Many2one('res.partner', string='Company', required=True)
    company_address = fields.Char(related='company_id.street', string='Company Address', required=True)
    team_id = fields.Many2many('hr.employee', string='Team Member Name', required=True)
    team_department = fields.Many2one(string='Team Member Department', related='team_id.department_id')
    evaluation_date = fields.Date(string='Risk Evaluation Date', required=True)
    method_group = fields.Selection([
        ('fk_evaluation', 'Fine Kinney Method'),
        ('lm_evaluation', 'L Matrix Method'),
    ], string='Methods')

    def set_values(self):
        res = super(RiskMethod, self).set_values()
        self.env['ir.config_parameter'].set_param('risk_analysis.team_id', self.team_id)
        return res

    @api.model
    def get_values(self):
        res = super(RiskMethod, self).get_values()
        team_id = self.env['ir.config_parameter'].sudo().get_param('risk_analysis.team_id')
        res.update(
            team_id=[(6, 0, literal_eval(team_id))],
        )
        return res


# class FkMethod(models.Model):
#
#     _name = 'fk.method'
#     _columns = {
#         'fk_probability': fields.char('Qualification Name', size=100, required=True),
#         'student_id': fields.many2one('student.info', 'Student'),





    fk_probability = fields.Selection([
        ('0.1', '0.1'),
        ('0.2', '0.2'),
        ('0.5', '0.5'),
        ('1', '1'),
        ('3', '3'),
        ('6', '6'),
        ('10', '10'),
    ], string='Probability')
    fk_frequency = fields.Selection([
        ('0.5', '0.5'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('6', '6'),
        ('10', '10'),
    ], string='Frequency')
    fk_effect = fields.Selection([
        ('1', '1'),
        ('3', '3'),
        ('7', '7'),
        ('15', '15'),
        ('40', '40'),
        ('100', '100'),
    ], string='Effect')
    fk_evaluation = fields.Float(string='Risk Value', required=True, compute='_fk_evaluation')

    fk_value = fields.Selection([
        ('1', 'Risk; perhaps acceptable'),
        ('2', 'Possible Risk; attention indicated'),
        ('3', 'Substantial Risk; correction needed'),
        ('4', 'High Risk; immediate correction required'),
        ('5', 'Very High Risk; consider discontinuing operation'),
    ], string='Risk Situation', compute='set_fk_value')

    @api.depends('fk_evaluation')
    def set_fk_value(self):
        for rec in self:
            if rec.fk_evaluation:
                if rec.fk_evaluation < 20:
                    rec.fk_value = '1'
                elif 20 < rec.fk_evaluation < 70:
                    rec.fk_value = '2'
                elif 70 < rec.fk_evaluation < 200:
                    rec.fk_value = '3'
                elif 200 < rec.fk_evaluation < 400:
                    rec.fk_value = '4'
                else:
                    rec.fk_value = '5'

    @api.depends('fk_probability', 'fk_frequency', 'fk_effect')
    def _fk_evaluation(self):
        for record in self:
            record.fk_evaluation = float(record.fk_probability) * float(record.fk_frequency) * int(record.fk_effect)

    lm_probability = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], string='Probability')
    lm_effect = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], string='Effect')
    lm_evaluation = fields.Integer(string='Risk Value', required=True, compute='_lm_evaluation')

    lm_value = fields.Selection([
        ('1', 'Acceptable Risk'),
        ('2', 'Possible Risk; attention indicated'),
        ('3', 'Substantial Risk; correction needed'),
        ('4', 'High Risk; immediate correction required'),
        ('5', 'Non-Acceptable Risk; consider discontinuing operation'),
    ], string='Risk Situation', compute='set_lm_value')

    @api.depends('lm_evaluation')
    def set_lm_value(self):
        for rec in self:
            if rec.lm_evaluation:
                if rec.lm_evaluation <= 2:
                    rec.lm_value = '1'
                elif 2 < rec.lm_evaluation <= 6:
                    rec.lm_value = '2'
                elif 6 < rec.lm_evaluation <= 10:
                    rec.lm_value = '3'
                elif 10 < rec.lm_evaluation <= 16:
                    rec.lm_value = '4'
                else:
                    rec.lm_value = '5'

    @api.depends('lm_probability', 'lm_effect')
    def _lm_evaluation(self):
        for record in self:
            record.lm_evaluation = int(record.lm_probability) * int(record.lm_effect)

    # @api.one
    # @api.constrains('fk_probability', 'fk_frequency')
    # def _check_fk(self):
    #     for rec in self:
    #         if (rec.fk_probability == False) or (rec.fk_frequency == False):
    #             raise ValidationError(_('Please enter a value!'))










