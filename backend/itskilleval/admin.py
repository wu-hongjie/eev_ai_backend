from django.contrib import admin

# Register your models here.
from itskilleval.models.ai_model import AImodel
from itskilleval.models.ai_model_input import AImodelInput
from itskilleval.models.eval import Eval
from itskilleval.models.train_history import TrainHistory
from itskilleval.models.job import Job
from itskilleval.service.models.ai_model_lightgbm import AiModelLightGBM
from itskilleval.tasks import training
from itskilleval.enum.eval_status import EvalStatus
from itskilleval.form.admin_ai_model import AdminAiModelForm

from django.contrib import messages
from django.utils.translation import ngettext, gettext_lazy as _

# AI model input
class AImodelInputModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'aimodel', 'name', 'type', 'updated_at', 'updated_by', 'created_at', 'created_by')
    ordering = ('-aimodel',)
    # read only created and updated user
    readonly_fields = ['created_by', 'updated_by']
    search_fields = ['aimodel__name']
    
    # save model    
    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
            obj.updated_by = request.user

        super().save_model(request, obj, form, change)

class AImodelInputModelInline(admin.TabularInline):
    model = AImodelInput
    extra = 0
    exclude = ('created_by', 'updated_by')
    ordering = ['name']

# AI model
class AImodelModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'updated_at', 'updated_by', 'created_at', 'created_by')
    ordering = ('-created_at',)
    # read only created and updated user
    readonly_fields = ['created_by', 'updated_by']
    
    actions = [
        'train_model'
    ]

    inlines = [AImodelInputModelInline,]
    form = AdminAiModelForm

    @admin.action(description=_("Select model to train"))
    def train_model(self, request, queryset):
        for ai_model in queryset:
            training.delay(ai_model.id)
        count = queryset.count()
        self.message_user(request, ngettext(
            _('%d AI model is training.'),
            _('%d AI model is training.'),
            count,
        ) % count, messages.SUCCESS)

    # save model    
    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
            obj.updated_by = request.user

        super().save_model(request, obj, form, change)

# Eval
class EvalModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'system_id', 'aimodel', 'created_at', 'updated_at')
    ordering = ('-created_at',)

# Training History
class TrainHistoryModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'aimodel', 'status', 'accuracy', 'loss', 'started_date', 'ended_date')
    ordering = ('-started_date',)

# Job
class JobModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'eval', 'status_string', 'detail','created_at', 'updated_at')
    ordering = ('-created_at',)
    
    @admin.display(description=_('Status'))
    def status_string(self, obj):
        return _('{value}: {name}'.format(value=obj.status, name=EvalStatus(obj.status).name.lower()))

admin.site.register(AImodel, AImodelModelAdmin)
admin.site.register(AImodelInput, AImodelInputModelAdmin)
admin.site.register(Eval, EvalModelAdmin)
admin.site.register(TrainHistory, TrainHistoryModelAdmin)
admin.site.register(Job, JobModelAdmin)