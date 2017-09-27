from django.conf.urls import url
from . import views

app_name = "ambiente"

urlpatterns = [
    url(r'^novo/$', views.novo_ambiente, name='novo'),
    url(r'^delete_event/$', views.deletar_evento, name='deletar_evento'),
    url(r'^(?P<pk>[0-9]+)/$', views.detalhe_ambiente, name='ambiente'),

    url(r'^(?P<pk>[0-9]+)/participantes/$', views.participantes, name='participantes'),
    url(r'^add_user/$', views.add_user, name='add_user'),
    url(r'^remove_user/$', views.remove_user, name='remove_user'),

    url(r'^(?P<pk>[0-9]+)/eventos/$', views.eventos, name='eventos'),
    url(r'^(?P<pk>[0-9]+)/eventos/novo/$', views.new_evento, name='novoevento'),
    url(r'^(?P<pk>[0-9]+)/eventos/editar/(?P<pkevento>[0-9]+)$', views.editar_evento, name='editar_evento'),
    url(r'^(?P<pk>[0-9]+)/eventos/(?P<pkevento>[0-9]+)/$', views.evento, name='evento'),

    url(r'^(?P<pk>[0-9]+)/tarefa/(?P<pktarefa>[0-9]+)/$', views.tarefa, name='tarefa'),
    url(r'^(?P<pkambiente>[0-9]+)/tarefa/(?P<pktarefa>[0-9]+)/validar$', views.solicitacao_validacao, name='solicitacao_validacao'),
    url(r'^(?P<pkambiente>[0-9]+)/tarefa/(?P<pktarefa>[0-9]+)/refutar$', views.refutacao_validacao, name='refutacao_validacao'),
]
