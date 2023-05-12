from django.urls import path
from rest_framework.routers import DefaultRouter

from builders.views import (
    ManagerApiView, BlockApiView,
    EntranceApiView, FloorApiView, ApartmentApiView, ComplexManagerConnectApi, BlockMainApiView
)
from builders.views.builder import (BuilderApiView, BuilderVerifyView)
from builders.views.resident_complex import (ResidentComplexApiView, ManagerComplexApiView)
from builders.views.sale_manager import (ClientNoticeApartmentApiView, ApartmentBuyApiView )


router = DefaultRouter(trailing_slash=False)
router.register(r'manager-complex', ManagerComplexApiView, basename='manager-complex') #edit
router.register(r'resident-complex', ResidentComplexApiView, basename='resident-complex')
router.register(r'manager', ManagerApiView, basename='manager')
router.register(r'', BuilderApiView, basename='')

urlpatterns = [
    # path('', BuilderApiView.as_view()),
    # path('', include(builder.urls)),
    # path('', include(resident_complex.urls)),
    # path('', include(manager.urls)),
    # path('', include(manager_complex.urls)),
    # path('build/<int:pk>/', BuilderApiViewUpd.as_view()),
    path('complex-manager-join', ComplexManagerConnectApi.as_view({'get': 'list', 'put': 'put'})),
    path('verify', BuilderVerifyView.as_view()),
    path('main', BlockMainApiView.as_view()),
    path('block', BlockApiView.as_view()),
    path('entrance', EntranceApiView.as_view()),
    path('floor', FloorApiView.as_view()),
    path('apartment', ApartmentApiView.as_view()),
    path('client-notice', ClientNoticeApartmentApiView.as_view()),
    path('aprtment-buy', ApartmentBuyApiView.as_view())

]

# print(router.urls)
# urlpatterns += manager_complex.urls
# urlpatterns += resident_complex.urls
# urlpatterns += builder.urls
urlpatterns += router.urls
