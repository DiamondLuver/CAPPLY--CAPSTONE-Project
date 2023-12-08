
from django.urls import path
from .views import  list_scholarship,search_tag, scholarship_detail, scrape_data, create_reply, create_comment, add_to_favorite, favorite_list,favorite_delete, delete_comment, delete_reply,create_scholarship,update_scholarship,search_tag_custom
urlpatterns = [
     path('scholarship', list_scholarship, name = 'scholarship'),
     path('scholarship/<slug:slug>/', scholarship_detail, name='scholarship_detail'),
     path('scholarship-create', create_scholarship, name="create_scholarship"),
     path('scholarship-update/<slug:slug>/', update_scholarship, name="update_scholarship"),
     path('scholarship/tag/<str:country>', search_tag, name = 'scholarship_tag'),
     path('scholarship/tag/<str:type>/<str:category>', search_tag_custom, name = 'search_tag_custom'),
     path('scrapping', scrape_data, name="scrape_data"),
     path('comment/<slug:slug>', create_comment, name="create_comment"),
     path('delete-comment/<slug:slug>/',delete_comment, name="delete_comment"),
     path('delete-reply/<int:comment_id>/',delete_reply, name="delete_reply"),
     path('reply/<int:comment_id>', create_reply, name="create_reply"),
     # favorite url
     path('add-to-favorite/<slug:slug>/', add_to_favorite, name='add_to_favorite'),
     path('favorite',favorite_list,name='favorite' ),
     path('favorite-delete/<slug:slug>', favorite_delete, name="favorite_delete"),
     # end of favorite url
]


