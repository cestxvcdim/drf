from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, get_object_or_404, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from edu.models import Course
from users.models import Payment, Subscription
from users.serializers import PaymentSerializer
from users.services import create_stripe_price, create_stripe_session


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)


class SubscriptionAPiView(APIView):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_list = Subscription.objects.filter(user=user, course=course_item)
        if subs_list.exists():
            sub_item = subs_list.first()
            sub_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'
        return Response({'message': message})


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        price = create_stripe_price(payment.payment_amount)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
