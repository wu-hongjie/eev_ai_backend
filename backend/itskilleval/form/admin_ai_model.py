from itskilleval.widget.admin_file_field import AdminFileFieldWidget
from itskilleval.models.ai_model import AImodel
from django.contrib.admin.widgets import AdminFileWidget

from django import forms


class AdminAiModelForm(forms.ModelForm):
    
    class Meta:
        model = AImodel
        exclude = []
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['training_file'].widget = AdminFileFieldWidget()
    