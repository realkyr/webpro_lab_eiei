from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError('%(value)s ไม่ใช่เลขคู่', params={'value': value})


class PollForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="ชื่อโพล", min_length=4, max_length=100, required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label="Email")
    no_questions = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), validators=[validate_even], label="จำนวนคำถาม", min_value=0, max_value=10, required=True)
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    def clean_title(self):
        data = self.cleaned_data['title']

        if 'ไอที' not in data:
            raise forms.ValidationError('คุณลืมชื่อคณะ')

        return data

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if start and not end:
            raise forms.ValidationError('โปรดเลือกวันสิ้นสุด')

        if end and not start:
            raise forms.ValidationError('โปรดเลือกวันเริ่มต้น')
