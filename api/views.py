import json

from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.versioning import BaseVersioning, QueryParameterVersioning, URLPathVersioning
from django.urls import reverse
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.parsers import JSONParser, FormParser, FileUploadParser
from api import models
from rest_framework import serializers

class UserView(APIView):
    
    def get(self, request, *args, **kwargs):
        
        # self.dispatch
        
        # 第一种写法
        # version = request._request.GET.get('version')
        
        # 第二种写法
        # version = request.query_params.get('version')
        
        # 第三种 ,配合 ParamVersion 类使用
        version = request.version
        print(version)
        
        # rest 反向生成url,不需要指定版本
        ull = request.versioning_scheme.reverse(viewname= 'user', request= request)
        print(ull)
        # http://127.0.0.1:8000/api/v2/user/
        
        # django反向生成url，需要指定版本
        ul = reverse(viewname= 'user', kwargs={'version': 1})
        print(ul)
        # /api/1/user/
        
        return HttpResponse('用户列表')
    
    def post(self, request, *args, **kwargs):
        
        return HttpResponse('POST和BODY')
    
    
class ParserView(APIView):
    # setting 设置全局之后就不用写了
    parser_classes = [JSONParser, FormParser, FileUploadParser]
    
    '''
    JSONParser: 只能解析 Content-Type: application/json
    FormParser: 只能解析 Content-Type: application/x-www-form-urlencoded 
    '''
    
    def post(self, request, *aargs, **kwargs):
        """
        允许客户发送Json数据
            application/json
            { name: alex, age: 18, gender: 男 }
        流程：
            1，获取用户请求
            2，获取用户请求头
            3，根据用户请求头 和 parser_class = [JSONParser, FormParser]中支持的请求头进行比较
            4，JSONParser对象去请求头
            5，request.data
        """
        data = request.data
        file = request.file
        print(data)
        return HttpResponse('Parser')
    


class RolesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()

class RolesView(APIView):

    def get(self, request, *aargs, **kwargs):
        
        # 方法一
        '''
        roles = models.Role.objects.all().values('id', 'title')
        
        roles = list(roles)
        
        ret = json.dumps(roles, ensure_ascii=False)
        '''
        
        # 方法二
        roles = models.Role.objects.all()
        
        ser = RolesSerializer(instance=roles, many=True)  # many=True  多条数据，单挑数据去掉或改为False
        
        ret = json.dumps(ser.data, ensure_ascii=False)
        
        return HttpResponse(ret)

class UserInfoSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()   
    user_type = serializers.IntegerField()   # 原始写法，显示组id 1，2
    xxx = serializers.CharField(source= "user_type")  # 自定义字段名称
    ooo = serializers.CharField(source= "get_user_type_display")  # 自定义字段名称和显示对应的级别  普通用户  VIP
    gp_id = serializers.CharField(source= "group.id")  # 获取组id  
    gp_title = serializers.CharField(source= "group.title")  # 获取组title
    # rls = serializers.CharField(source= "role.all")  # 获取角色
    rls = serializers.SerializerMethodField() # 自定义显示
    
    def get_rls(self, row):
        # 固定写法
        # return [
        #     {'id':1, 'title':'老师'},
        #     {'id':2, 'title':'医生'}
        # ]
        
        # 动态
        role_obj_list = row.role.all()
        
        ret = []
        for item in role_obj_list:
            ret.append({'id':item.id, 'title':item.title})
        return ret

class UserInfoSerializer(serializers.ModelSerializer):
    
    xxx = serializers.CharField(source= "user_type")  # 自定义字段名称
    ooo = serializers.CharField(source= "get_user_type_display")  # 自定义字段名称和显示对应的级别  普通用户  VIP
    gp_title = serializers.CharField(source= "group.title")  # 获取组title
    
    class Meta:
        model = models.UserInfo
        # fields = '__all__'    # 获取所有得字段
        
        fields = ['id', 'username', 'password', 'xxx', 'ooo', 'gp_title']
        
# 方法三        
class MyField(serializers.CharField):
    
    def to_representation(self,value):
        
        return value
        
class UserInfoSerializer(serializers.ModelSerializer):
    
    x1 = MyField(source= "username")
    
    
    class Meta:
        model = models.UserInfo
        # fields = '__all__'    # 获取所有得字段
        
        fields = ['id', 'username', 'password', 'x1']

class UserInfoView(APIView):
    def get(self, request, *aargs, **kwargs):
        
        userinfo = models.UserInfo.objects.all()
        
        ser = UserInfoSerializer(instance=userinfo, many=True)  # many=True  多条数据，单挑数据去掉或改为False
        
        ret = json.dumps(ser.data, ensure_ascii=False)
        
        return HttpResponse(ret)
        