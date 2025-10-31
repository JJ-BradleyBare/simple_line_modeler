from django.contrib import admin

from .models import Process, Step, StepIndex, StepParallelization, Swimlane, SwimlaneIndex

admin.site.register(Process)
admin.site.register(Swimlane)
admin.site.register(SwimlaneIndex)
admin.site.register(Step)
admin.site.register(StepIndex)
admin.site.register(StepParallelization)
