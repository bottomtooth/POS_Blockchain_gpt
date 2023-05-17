from django.urls import path
from . import views
from .views import CreateTransactionView

urlpatterns = [
    path('', views.index, name='index'),
    path('view-blockchain/', views.view_blockchain, name='view-blockchain'),
    #path('create-transaction/', views.create_transaction, name='create-transaction'),
    path('mine/', views.mine, name='mine-block'),
    path('wallet/', views.view_wallet, name='view-wallet'),
    path('validators/', views.manage_validators, name='manage-validators'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create-transaction/', CreateTransactionView.as_view(), name='create-transaction'),
]
