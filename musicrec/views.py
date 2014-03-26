#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from musicrec.models import Song

from sae.storage import Bucket
import random

import ctypes
from ctypes import *
from django.contrib import auth


def player(request):
    
    if request.user.is_authenticated():     #判断用户是否已登录
        user = request.user;          #获取已登录的用户
    else:
        user = request.user;          #非登录用户将返回AnonymousUser对象


    rating_list = [1,2,3,4,5]

    music_local_path =  "http://172.18.217.67:8000/music/"
    userid = random.randint(1,967)

    songid = random.randint(1,967)
    
    #just for sae..
    bucket = Bucket('music')
    
    p = get_object_or_404(Song, pk=songid)
    path = p.path
    singer = p.singer
    title = p.title
    song_name = 'Songs/' + path.encode('utf8')
#    url = bucket.generate_url(song_name)
    url = music_local_path + song_name

    ll = ctypes.cdll.LoadLibrary
    rbmcf = ll("./RunRBMCF.so")
 
    k = 5
    array_int = c_int * k
    rbmcf_top_k = array_int(0,0,0,0,0)
   
    rbmcf.predict_ratings.restype = c_double
    pred = rbmcf.predict_ratings(userid, songid) 

    rbmcf.recommend_top_k(userid, k, rbmcf_top_k)
    for top_movie_id in rbmcf_top_k:
        print top_movie_id

    ahrbmcf = ll("./RunAHRBMCF.so")
    
    ahrbmcf.predict_ratings.restype = c_double
    ah_pred = ahrbmcf.predict_ratings(userid, songid) 
    
    ah_top_k = array_int(0,0,0,0,0)
    ahrbmcf.recommend_top_k(userid, k, ah_top_k)
    for top_movie_id in ah_top_k:
        print top_movie_id
    return render_to_response('player.html', {'rating_list': rating_list, 'url': url, 'id': songid, 'title': title, 'singer': singer, 'pred': pred, 'ah_pred': ah_pred, 'userid': userid}, context_instance=RequestContext(request))


