from django import forms

class BallisticsForm(forms.Form):
    initial_velocity = forms.FloatField(label='Начальная скорость (м/с)', min_value=0)
    mass = forms.FloatField(label='Масса снаряда (г)', min_value=0)
    diameter = forms.FloatField(label='Диаметр снаряда (мм)', min_value=0)
    angle_deg = forms.FloatField(label='Угол (градусы)', min_value=0, max_value=90)
    initial_height = forms.FloatField(label='Начальная высота (м)', required=False, initial=0)