from rest_framework.generics import GenericAPIView
from rest_framework import permissions,response
from .serializers import SendDateTimeSerializer
from django_celery_beat.models import ClockedSchedule, PeriodicTask


class SendDateTimeAPI(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SendDateTimeSerializer

    def post(self,request,**kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        clocked,_ = ClockedSchedule.objects.get_or_create(clocked_time=request.data.get('datetime'))

        try:
            task = PeriodicTask.objects.get(name='task',task='task.celery.clean')
        except PeriodicTask.DoesNotExist:
            task = PeriodicTask.objects.create(name=f'task-{PeriodicTask.objects.count() + 1}',task='task.celery.clean',clocked_id=clocked.id,one_off=True)

        return response.Response(status=200)

        
