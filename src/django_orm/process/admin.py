from django.contrib import admin

from .models import FunctionStep, Process, ProcessStep, StepIndex, StepSynchronization, SwimLane, SwimLaneIndex

admin.site.register(Process)
admin.site.register(SwimLane)
admin.site.register(SwimLaneIndex)
admin.site.register(FunctionStep)
admin.site.register(ProcessStep)
admin.site.register(StepIndex)
admin.site.register(StepSynchronization)
