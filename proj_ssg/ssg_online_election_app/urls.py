from django.urls import path, include
from . import views


from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.index_view, name="index_view"),
    path('save/',views.save_vote, name="save_vote"),
    path('login/',views.login_view, name="login_view"),
    path('logout/',views.logout_view, name="logout_view"),
    path('dashboard/',views.dashboard_view, name="dashboard_view"),
    path('export/',views.export_page, name="export_page"),
    path('generate_voucher/',views.generate_voucher_view, name="generate_voucher_view"),
    path('candidates/',views.candidates_view, name="candidates_view"),
    path('updatepic/',views.updatepic_view, name="updatepic_view"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)