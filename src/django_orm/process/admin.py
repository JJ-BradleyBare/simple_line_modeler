from django.contrib import admin

from .models import FunctionStep, Process, ProcessStep, StepIndex, StepParallelization, Swimlane, SwimlaneIndex

admin.site.register(Process)
admin.site.register(Swimlane)
admin.site.register(SwimlaneIndex)
admin.site.register(FunctionStep)
admin.site.register(ProcessStep)
admin.site.register(StepIndex)
admin.site.register(StepParallelization)
