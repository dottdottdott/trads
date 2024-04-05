from random import random, randrange


def _randvariation(range=3):
    return random() * randrange(-range, range)


# This is dummy module for Trust Evaluation 

def trusteval_post(post_data):
    return post_data['author'].trust_value + _randvariation()

def trusteval_author(author_data):
    if 'trust_value' in author_data.keys():
        return author_data['trust_value'] + _randvariation()
    else:
        return 5 + _randvariation()


def trusteval_message(message_data):
    if not message_data['received']:
        if message_data['correspondent'].trust_value < 12:
            cor = message_data['correspondent'].trust_value
            cor.trust_value += 0.1
            cor.save()

def trusteval_reaction(response_data):
    tpost = response_data['targetpost']
    if tpost.author.trust_value < response_data['author'].trust_value:
        tauth = tpost.author
        tauth.trust_value += 0.1
        tauth.save()

