from django.urls import path
from .views import *
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register('images', FileUploadViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('transform', TransformView.as_view()),
    path('pipeline/<filename>/', pipeline, name='pipeline'),
    path('labels/', labels, name='labels'),
    path('curr_network/',NetworkView.as_view()),
    path('train/',train, name='train'),

    path('data_viz/', data_viz),
    path('net_dis/', net_dis),
    path('net_mod', net_mod),
    path('starttrain', start_training),
    path('starteval', start_evaluation),
    path('getevalresults', get_eval_results),
    path('geteval', get_eval),
    path('getwrongresults/', get_wrong_results),
    path('startgradcamlime/', start_gradcam_lime),
    path('getsuggestions', get_suggestions),
    path('conf_mat/',getConfMatWithLabels),
    path('train_data/', get_train_data)
]
