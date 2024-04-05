from django.shortcuts import render
from solidsocial.models import Post, Author, Vcard, Reaction
from solidsocial.serializers.author import AuthorSerializer
from solidsocial.serializers.post import PostSerializer
from solidsocial.serializers.vcard import VcardSerializer
from solidsocial.serializers.reaction import ReactionSerializer


def UserView(request, pk):
    author = Author.objects.get(pk=pk)
    author_serializer = AuthorSerializer(author)
    vcard = Vcard.objects.get(author=pk)
    vcard_serializer = VcardSerializer(vcard)
    posts = Post.objects.filter(author=pk)
    post_serializer = PostSerializer(posts, many=True)
    posts_data = sorted(post_serializer.data, key=lambda k: k['cdate'], reverse=True)
    for rp in [ p for p in posts_data if p['response'] ]:
        rp['response'] = PostSerializer(Post.objects.get(pk=rp['response'])).data
    authors = Author.objects.all()
    authorserializer = AuthorSerializer(authors, many=True)
    authors_data = {}
    for a in authorserializer.data:
        #index = a.pop('id')
        index = a['id']
        authors_data[index] = a
    reactions = Reaction.objects.all()
    reactionserializer = ReactionSerializer(reactions, many=True)
    reactions_data = {}
    for a in reactionserializer.data:
        index = a['targetpost']
        if index not in reactions_data:
            reactions_data[index] = []
        reactions_data[index].append(a)
    return render(request, "user.html", {
        'current': 'User',
        'author': author_serializer.data,
        'vcard': vcard_serializer.data,
        'posts': posts_data,
        'authors': authors_data,
        'reactions': reactions_data,
        'responded': [],
        })

