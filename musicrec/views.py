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


music_local_path =  "http://172.18.217.67:8000/music/"
lyric_local_path =  "/home/daiwk/graduate/graduate-Web/music_django/djproj/trunk/music/"

def login_view(request):        
    user = authenticate(username=request.POST['username'], password=request.POST['password'])    
    if user is not None:        
        login(request, user)
        print request.user          
        return index(request)    
    else:        #验证失败，暂时不做处理        
        return index(request)

def logout_view(request):    
    logout(request)    
    return index(request)

def index(request):
    
    bg_id = random.randint(1,20)
    bg_src = "http://172.18.217.67:8000/imgs/bg" + str(bg_id) +".png"
    userid = random.randint(1,967)
    if request.user.is_authenticated():     #判断用户是否已登录
        user = request.user;          #获取已登录的用户
        userid = user.id
        print user
    else:
        user = request.user;          #非登录用户将返回AnonymousUser对象
        print user

    return render_to_response('index.html', {'bg_src': bg_src}, context_instance=RequestContext(request))
        

def recommend(request):
    # 读取模型
    ll = ctypes.cdll.LoadLibrary
    rbmcf = ll("./RunRBMCF.so")
 
    ahrbmcf = ll("./RunAHRBMCF.so")
    
    # 设定top k
    k = 10
    array_int = c_int * k
  
    userid = random.randint(1,967)
    if request.user.is_authenticated():     #判断用户是否已登录
        user = request.user;          #获取已登录的用户
        userid = user.id
        print user
    else:
        user = request.user;          #非登录用户将返回AnonymousUser对象
        print user

    #just for sae..
#    bucket = Bucket('music')
    
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

    rec_ids = set()
    
    for top_music_id in top_k:

        if top_music_id > 0:
            music_id = top_music_id % 963
        else:
            music_id = 1

        rec_ids.add(music_id)

    for music_id in rec_ids:

        rec_p = get_object_or_404(Song, pk=music_id)
        rec_path = rec_p.path
        rec_singer = rec_p.singer

        rec_title = rec_p.title
        rec_lyric = rec_p.lyrics

        rec_song_name = 'Songs/' + rec_path.encode('utf8')
    #    url = bucket.generate_url(song_name)
        rec_url = music_local_path + rec_song_name

#        rec_id = rec_singer.encode('utf8') + '<a href="' + rec_url +'" target="musicframes">' + rec_title.encode('utf8') + '</a>'
        print rec_lyric.encode('utf8')+'tmp'
        rec_id = '<strong>' + rec_singer.encode('utf8') + ' <a href="/musicrec/player.html?url=' + rec_url + '&singer=' + rec_singer.encode('utf8') + '&title=' + rec_title.encode('utf8') + '&lyric=' + rec_lyric.encode('utf8') + '" target="musicframe">' + rec_title.encode('utf8') + '</a></strong>'
        
        rec_list.append(rec_id)

# 如果还需要显示预测的评分
#return render_to_response('player.html', {'bg_src': bg_src, 'rating_list': rating_list, 'url': url, 'id': songid, 'title': title, 'singer': singer, 'pred': pred, 'ah_pred': ah_pred, 'userid': userid, 'rec_list': rec_list}, context_instance=RequestContext(request))
    return render_to_response('recommendation.html', {'rec_list': rec_list}, context_instance=RequestContext(request))

       

def player(request):

    args = {}
    args["url"] = request.GET.get('url')
    args["singer"] = request.GET.get('singer')
    args["title"] = request.GET.get('title')
    args["lyric"] = request.GET.get('lyric')
    url = args.get("url","")
    singer = args.get("singer","")
    #print singer
    title = args.get("title","")
    #print title
    lyric = args.get("lyric","")
    #print lyric

    #print url
    if url is None:
        songid = random.randint(1,967)
        p = get_object_or_404(Song, pk=songid)
        path = p.path
        singer = p.singer
        title = p.title
        lyric = p.lyrics
        song_name = 'Songs/' + path.encode('utf8')
    #    url = bucket.generate_url(song_name)
        url = music_local_path + song_name
    lyric_name = 'Lyrics/' + lyric+'tmp' #tmpfinal有<br/>
    #print lyric_name
    lyric_url = lyric_local_path + lyric_name
    lyric_file = open(lyric_url, 'r')
    lyric_txt = lyric_file.read()
    print lyric_txt
    return render_to_response('player.html', {'url': url,'singer': singer, 'title': title, 'lyric': lyric_txt}, context_instance=RequestContext(request))

