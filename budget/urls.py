"""budget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from budget_api.views import DespesaViewSet, ReceitaViewSet, DespesasMesViewList, ReceitasMesViewList, ResumoMesView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('despesas', DespesaViewSet, basename='DESPESAS')
router.register('receitas', ReceitaViewSet, basename='RECEITAS')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('despesas/<int:year>/<int:month>/', DespesasMesViewList.as_view(), name='despesas-por-mes'),
    path('receitas/<int:year>/<int:month>/', ReceitasMesViewList.as_view(), name='receitas-por-mes'),
    path('resumo/<int:year>/<int:month>/', ResumoMesView.as_view(), name='resumo-mes'),
]
