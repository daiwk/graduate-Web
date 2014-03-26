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

from django.contrib.auth import authenticate,login,logout

def login_view(request):        
    user = authenticate(username=request.POST['username'], password=request.POST['password'])    
    if user is not None:        
        login(request, user)
        print request.user          
        return player(request)    
    else:        #验证失败，暂时不做处理        
        return player(request)

def logout_view(request):    
    logout(request)    
    return player(request)


def player(request):
 
    # 读取模型
    ll = ctypes.cdll.LoadLibrary
    rbmcf = ll("./RunRBMCF.so")
 
    ahrbmcf = ll("./RunAHRBMCF.so")
    
    # 设定top k
    k = 5
    array_int = c_int * k
  
    userid = random.randint(1,967)
    if request.user.is_authenticated():     #判断用户是否已登录
        user = request.user;          #获取已登录的用户
        userid = user.id
        print user
    else:
        user = request.user;          #非登录用户将返回AnonymousUser对象
        print user


    rating_list = [1,2,3,4,5]

    music_local_path =  "http://172.18.217.67:8000/music/"
    
    
    #just for sae..
#    bucket = Bucket('music')
    
    songid = random.randint(1,967)
    p = get_object_or_404(Song, pk=songid)
    path = p.path
    singer = p.singer
    title = p.title
    song_name = 'Songs/' + path.encode('utf8')
#    url = bucket.generate_url(song_name)
    url = music_local_path + song_name

    #用于预测用户对当前音乐的可能评分
#    rbmcf.predict_ratings.restype = c_double
#    pred = rbmcf.predict_ratings(userid, songid) 
#
#    ahrbmcf.predict_ratings.restype = c_double
#    ah_pred = ahrbmcf.predict_ratings(userid, songid) 
 
    rbmcf_top_k = array_int(0,0,0,0,0)
    rbmcf.recommend_top_k(userid, k, rbmcf_top_k)
   
    ah_top_k = array_int(0,0,0,0,0)
    ahrbmcf.recommend_top_k(userid, k, ah_top_k)

    # 选择使用哪一种模型的预测结果
    top_k = ah_top_k #或者rbmcf_top_k等结果

    rec_list = []

    for top_music_id in top_k:

        if top_music_id > 0:
            music_id = top_music_id % 963
        else:
            music_id = 1
        rec_p = get_object_or_404(Song, pk=music_id)
        rec_path = rec_p.path
        rec_singer = rec_p.singer

        rec_title = rec_p.title

        rec_song_name = 'Songs/' + rec_path.encode('utf8')
    #    url = bucket.generate_url(song_name)
        rec_url = music_local_path + rec_song_name

        rec_id = rec_singer.encode('utf8') + '<a href="' + rec_url +'">' + rec_title.encode('utf8') + '</a>'
        
        rec_list.append(rec_id)
        bg_id = random.randint(1,10)
    bg_src = "http://172.18.217.67:8000/imgs/bg" + str(bg_id) +".png"

# 如果还需要显示预测的评分
#return render_to_response('player.html', {'bg_src': bg_src, 'rating_list': rating_list, 'url': url, 'id': songid, 'title': title, 'singer': singer, 'pred': pred, 'ah_pred': ah_pred, 'userid': userid, 'rec_list': rec_list}, context_instance=RequestContext(request))
    return render_to_response('player.html', {'bg_src': bg_src, 'rating_list': rating_list, 'url': url, 'id': songid, 'title': title, 'singer': singer,  'rec_list': rec_list}, context_instance=RequestContext(request))


