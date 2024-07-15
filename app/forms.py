from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime

class AppointmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Start Time', format='%H:%M', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_time = TimeField('End Time', format='%H:%M', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    private = BooleanField('Private')
    submit = SubmitField('Submit')
    
    def validate_start_date(self, field):
        start = datetime.combine(self.start_date.data, self.start_time.data)
        if start <= datetime.now():
            raise ValidationError("Start date/time must be in the future")
        
    def validate_end_date(self, field):
        start = datetime.combine(self.start_date.data, self.start_time.data)
        end = datetime.combine(self.end_date.data, self.end_time.data)
        if start >= end:
            raise ValidationError("End date/time must come after start date/time")
    
    def validate_start_time(self, field):
        start = datetime.combine(self.start_date.data, self.start_time.data)
        if start <= datetime.now():
            raise ValidationError("Start date/time must be in the future")
    
    def validate_end_time(self, field):
        start = datetime.combine(self.start_date.data, self.start_time.data)
        end = datetime.combine(self.end_date.data, self.end_time.data)
        if end <= start:
            raise ValidationError("End date/time must come after start date/time")
