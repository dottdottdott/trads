from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from .views.feed import FeedView
from .views.user import UserView
from .views.users import UsersView
from .views.about import AboutView
from .views.chats import ChatsView
from .views.chat import ChatView
from .views.api.author import AuthorAPI
from .views.api.authors import AuthorsAPI
from .views.api.followee import FolloweeAPI
from .views.api.followees import FolloweesAPI
from .views.api.message import MessageAPI
from .views.api.messages import MessagesAPI
from .views.api.post import PostAPI
from .views.api.posts import PostsAPI
from .views.api.reaction import ReactionAPI
from .views.api.reactions import ReactionsAPI
from .views.api.preview import PreviewAPI
from .views.api.previews import PreviewsAPI
from .views.api.posts_update import PostsUpdateAPI
from .views.api.message_update import MessagesUpdateAPI
from .views.api.feed_update import FeedUpdateAPI
from .views.api.vcard import VcardAPI
from .views.api.vcards import VcardsAPI
from .views.api.demo import DemoAPI

urlpatterns = [
        path('', FeedView, name='Feed'),
        path('feed/', FeedView, name='Feed'),
        path('chats/', ChatsView, name='Chats'),
        path('chat/<int:pk>', ChatView, name='Chat'),
        path('user/<int:pk>', UserView, name='User'),
        path('users/', UsersView, name='Users'),
        path('about/', AboutView, name='About'),
        path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url("images/favicon.ico")), name='Fav'),
        path('logo.svg', RedirectView.as_view(url=staticfiles_storage.url("images/solid-logo-orange.svg")), name='Logo'),
]

urlpatterns += [
        path('api/post/<int:pk>', PostAPI.as_view(), name='post_api'),
        path('api/post', PostAPI.as_view(), name='post_noarg_api'),
        path('api/posts', PostsAPI.as_view(), name='posts_api'),
        path('api/update/posts', PostsUpdateAPI.as_view(), name='posts_update_api'),
        path('api/authors', AuthorsAPI.as_view(), name='authors_api'),
        path('api/author/<int:pk>', AuthorAPI.as_view(), name='author_api'),
        path('api/author', AuthorAPI.as_view(), name='author_api'),
        path('api/vcard/<int:pk>', VcardAPI.as_view(), name='vcard_api'),
        path('api/vcards', VcardsAPI.as_view(), name='vcards_api'),
        path('api/preview', PreviewAPI.as_view(), name='preview_api'),
        path('api/previews', PreviewsAPI.as_view(), name='previews_api'),
        path('api/reaction', ReactionAPI.as_view(), name='reaction_api'),
        path('api/reactions', ReactionsAPI.as_view(), name='reactions_api'),
        path('api/messages', MessagesAPI.as_view(), name='messages_api'),
        path('api/message/<int:pk>', MessageAPI.as_view(), name='message_api'),
        path('api/followee/<int:pk>', FolloweeAPI.as_view(), name='followee_api'),
        path('api/followee', FolloweeAPI.as_view(), name='followee_noarg_api'),
        path('api/followees', FolloweesAPI.as_view(), name='followees_api'),
        path('api/update/messages', MessagesUpdateAPI.as_view(), name='update_messages_api'),
        path('api/update/feed', FeedUpdateAPI.as_view(), name='feed_update_api'),
        path('api/demo', DemoAPI.as_view(), name='demo_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
