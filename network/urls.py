from django.urls import path

from network import apps, views

app_name = apps.NetworkConfig.name

urlpatterns = [
    path("elements/", views.NetworkElementList.as_view(), name="elements"),
    path("add_element/", views.NewNetworkElement.as_view(), name="add_element"),
    path("retrieve_element/<int:pk>/", views.RetrieveNetworkElement.as_view(), name="retrieve_element"),
    path("update_element/<int:pk>/", views.UpdateNetworkElement.as_view(), name="update_element"),
    path("delete_element/<int:pk>/", views.DestroyNetworkElement.as_view(), name="delete_element"),
]
