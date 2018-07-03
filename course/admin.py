from django.contrib import admin
from .models import UnitAssessmentCompleted

class UnitAssessmentCompletedAdmin(admin.ModelAdmin):
    pass

admin.site.register(UnitAssessmentCompleted, UnitAssessmentCompletedAdmin)