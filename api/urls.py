from django.urls import path
from . import views

urlpatterns = [
    path('Tags/AddTag', views.add_tag, name='add_tag'),
    path('Tags/GetTags', views.get_tags, name='get_tags'),
    path('Tags/AddSubTag', views.add_subtag, name='add_subtag'),
    path('Tags/GetSubTags', views.get_subtags, name='get_subtags'),
    path('GetBalance', views.get_balance, name='get_balance'),
    path('AddExpense', views.add_expense, name='add_expense'),
    path('GetExpenses', views.get_expenses, name='get_expenses')
]