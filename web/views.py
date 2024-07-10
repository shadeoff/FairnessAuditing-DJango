import json

from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import User
from .serializer import UserSerializer

from IntegratedInterface.main import AuditingFramework
from .singleton_model import SingletonModel


def index(request):
    return HttpResponse("Hello World")


# Create your views here.
@api_view(['POST'])
def create_user(request):
    print(request.data)
    serializer = UserSerializer(data=request.data)
    print(serializer.is_valid())
    if serializer.is_valid():
        print("进入该方法")
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Exp01View(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        request_type = request.query_params.get('type')
        print(request_type)
        if request_type == 'get_features':
            print(request.query_params)
            data = self.get_features()
            return data
        elif request_type == 'get_train_accuracy':
            data = self.get_train_accuracy()
            return data

        elif request_type == 'get_test_accuracy':
            data = self.get_test_accuracy()
            return data

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_features(self):
        data = {
            'age': [17, 90],
            'capital-gain': [0, 99999],
            'capital-loss': [0, 4356],
            'education-num': [1, 16],
            'hours-per-week': [1, 99],
            'race_White': [0, 1],
            'sex_Male': [0, 1],
            'marital-status': ['Divorced', 'Married-AF-spouse', 'Married-civ-spouse', 'Married-spouse-absent',
                               'Never-married', 'Separated', 'Widowed'],
            'workclass': ['Federal-gov', 'Local-gov', 'Private', 'Self-emp-inc', 'Self-emp-not-inc', 'State-gov',
                          'Without-pay']
        }
        return Response(data, status=status.HTTP_200_OK)

    # 预处理
    def process_data(self, data):
        pass
    
    def get_train_accuracy(self):
        """
        注意：初始化模型时dataloader默认为None，需要先定义好dataloader才能调用后面的函数
            在方法中，是先设置了敏感属性，然后才显示得到了loader

        :return:
        """
        print("进入该方法")
        # 得到全局对象模型
        singleton_instance = SingletonModel()
        fw = singleton_instance.auditing_framework

        fw.get_model_info()
        # 不严谨，默认了敏感属性为种族
        fw.set_sensitive_attr('race')
        fw.set_individual_fairness_metric(dx='LR', eps=fw.get_default_eps())
        train_accuracy = fw.accuracy(fw.model, whether_training_set=True).item()
        return Response(train_accuracy, status=status.HTTP_200_OK)

    def get_test_accuracy(self):
        """
        注意：初始化模型时dataloader默认为None，需要先定义好dataloader才能调用后面的函数
            在方法中，是先设置了敏感属性，然后才显示得到了loader
        :return:
        """
        print("进入该方法")

        # 得到全局对象模型
        singleton_instance = SingletonModel()
        fw = singleton_instance.auditing_framework

        fw.get_model_info()
        # 不严谨，默认了敏感属性为种族
        fw.set_sensitive_attr('race')
        fw.set_individual_fairness_metric(dx='LR', eps=fw.get_default_eps())
        test_accuracy = fw.accuracy(fw.model).item()
        return Response(test_accuracy, status=status.HTTP_200_OK)

    def post(self,request, *args, **kwargs):
        """
        注意：同获取准确率，也需要先设置敏感属性
        需要的数据为字典
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        print(request.data)
        data_sample = request.data

        # 得到全局对象模型
        singleton_instance = SingletonModel()
        fw = singleton_instance.auditing_framework

        # fw.set_sensitive_attr('race')
        # fw.set_individual_fairness_metric(dx='LR', eps=fw.get_default_eps())
        result = ''
        probability = fw.query_model(data_sample)
        if probability >= 0.5:
            result = "年收入高于50K"
        else:
            result = "年收入低于50K"
        return Response(result, status=status.HTTP_200_OK)


class Exp02View(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        singleton_instance = SingletonModel()
        fw = singleton_instance.auditing_framework
        action = request.data['action']
        # print(request.data)

        if action == 'set_sensitive_attr':
            sensitive_attr = request.data['data']
            fw.set_sensitive_attr(sensitive_attr)
            return Response(fw.sensitive_attr, status=status.HTTP_200_OK)

        elif action == 'set_range':
            range_dict = self.filter_json_data(data)
            fw.set_data_range(range_dict)
            print(range_dict)
            return Response(fw.range_dict, status=status.HTTP_200_OK)

        else:
            return Response("error", status=status.HTTP_400_BAD_REQUEST)

    def filter_json_data(self, data):
        data_content = data.get('data',{})
        filtered_data_dict = {}
        for key, value in data_content.items():
            scope_value = value.get('scope',[])
            filtered_data_dict[key] = scope_value

        return filtered_data_dict


class Exp03View(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        singleton_instance = SingletonModel()
        fw = singleton_instance.auditing_framework
        dx = data.get('dx')
        eps = data.get('eps')
        print(dx, eps)
        # eps换成float
        eps = float(eps)
        fw.set_individual_fairness_metric(dx, eps)

        return Response("success",status=status.HTTP_200_OK)


class Exp04View(APIView):
    def get(self, request, *args, **kwargs):
        singleton_instance = SingletonModel()
        fw = singleton_instance.auditing_framework
        range_dict = fw.get_data_range()
        sensitive_attr = fw.sensitive_attr
        print(sensitive_attr, range_dict)
        result = {
            "range": range_dict,
            "sensitive_attr": sensitive_attr
        }
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        注意：同获取准确率，也需要先设置敏感属性
        需要的数据为字典
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 获取action
        data = request.data
        action = request.data['action']
        # print(request.data)

        # 得到全局对象模型
        singleton_instance = SingletonModel()
        fw = singleton_instance.auditing_framework

        if action == 'check_result':
            print(request.data)
            data_sample = request.data['data']
            result = ''
            probability = fw.query_model(data_sample)
            if probability >= 0.5:
                result = "年收入高于50K"
            else:
                result = "年收入低于50K"
            return Response(result, status=status.HTTP_200_OK)
        elif action == 'check_fair':
            data_sample1 = request.data['data1']
            data_sample2 = request.data['data2']
            sample_pair = [data_sample1, data_sample2]
            fair_or_not, dx, dy = fw.fair(fw.model, sample_pair)
            eps = fw.unfair_metric.epsilon
            result = {
                "fair_or_not": fair_or_not,
                "dx": '∞' if dx==0 else 1/dx,
                "dy": dy,
                "eps": eps
            }
            return Response(result, status=status.HTTP_200_OK)
        return Response("error", status=status.HTTP_400_BAD_REQUEST)


class Exp05View(APIView):
    def get(self, request, *args, **kwargs):
        request_type = request.query_params.get('type')
        print(request_type)
        singleton_instance = SingletonModel()
        fw = singleton_instance.auditing_framework
        if request_type == 'get_range':
            print(request.query_params)
            range_dict = fw.get_data_range()
            return Response(fw.range_dict, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        singleton_instance = SingletonModel()
        fw = singleton_instance.auditing_framework
        action = request.data['action']
        # print(request.data)
        if action == 'seek_unfair_pair':
            # 转化成字典
            data = request.data['data']
            # 添加字段
            random_sample = self.filter_dict(data)
            # 寻找不公平对并返回
            random_sample = [random_sample]
            unfair_pair = fw.seek_unfair_pair(random_sample)
            print(unfair_pair)
            return Response(unfair_pair, status=status.HTTP_200_OK)
        elif action == 'check_unfair_pair':
            data_sample1 = request.data['data1']
            data_sample2 = request.data['data2']
            # 获取各个表的收入预测
            probability1 = fw.query_model(data_sample1)
            probability2 = fw.query_model(data_sample2)
            if probability1 >= 0.5:
                result1 = "年收入高于50K"
            else:
                result1 = "年收入低于50K"
            if probability2 >= 0.5:
                result2 = "年收入高于50K"
            else:
                result2 = "年收入低于50K"
            result = [result1, result2]

            # 获取评测数据
            sample_pair = [data_sample1, data_sample2]
            fair_or_not, dx, dy = fw.fair(fw.model, sample_pair)
            eps = fw.unfair_metric.epsilon
            fair_data = {
                "fair_or_not": fair_or_not,
                "dx": '∞' if dx==0 else 1/dx,
                "dy": dy,
                "eps": eps
            }
            data = {
                "result": result,
                "fair_data": fair_data
            }
            fw.unfair_pair_judge = data
            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response("error", status=status.HTTP_400_BAD_REQUEST)

    def filter_json_data(self, data):
        data_content = data.get('data',{})
        filtered_data_dict = {}
        for key, value in data_content.items():
            scope_value = value.get('scope',[])
            filtered_data_dict[key] = scope_value

        return filtered_data_dict

    def filter_dict(self, data):
        # 添加 race 字段
        if data.get('race_White') == 1:
            data['race'] = 'White'
        else:
            data['race'] = 'Others'

        # 添加 sex 字段
        if data.get('sex_Male') == 1:
            data['sex'] = 'Male'
        else:
            data['sex'] = 'Female'
        return data


class Exp06View(APIView):
    def get(self, request, *args, **kwargs):
        # 初始化了一个main中AuditingFramework的单例
        singleton_instance = SingletonModel()
        fw = singleton_instance.auditing_framework

        # 获取不公平数据对
        unfair_pair = fw.get_unfair_pair()
        individual_fairness = (fw.local_individual_fairmess_metric(fw.model, unfair_pair[0]) +
                               fw.local_individual_fairmess_metric(fw.model, unfair_pair[1])) / 2

        # global_fairness = '' 待定
        # 得到新模型
        new_model = fw.optimize(fw.model, unfair_pair)

        new_individual_fairness = (fw.local_individual_fairmess_metric(new_model, unfair_pair[0]) +
                                   fw.local_individual_fairmess_metric(new_model, unfair_pair[1])) / 2
        print(f"individual_fairness is {individual_fairness}")
        print(f"new_individual_fairness is {new_individual_fairness}")

        # 另外需要返回敏感属性，数据范围、衡量准则、eps、找到的样本的判别情况
        sensitive_attr = '种族' if fw.sensitive_attr[0] == 'race_White' else '性别'
        data_range = fw.get_data_range()
        eps = fw.unfair_metric.epsilon
        dx_measure = fw.dx_measure
        unfair_pair_judge = fw.unfair_pair_judge
        # the structure of unfair_pair_judge:
        # {   "result": [result1, result2],
        #     "fair_data": {
        #         "fair_or_not": fair_or_not,
        #         "dx": '∞' if dx==0 else 1/dx,
        #         "dy": dy,
        #         "eps": eps
        #      }
        # }

        # 汇总
        result = {
            "unfair_pair": unfair_pair,
            "individual_fairness": individual_fairness,
            "new_individual_fairness": new_individual_fairness,
            "sensitive_attr": sensitive_attr,
            "data_range": data_range,
            "eps": eps,
            "dx_measure": dx_measure,
            "unfair_pair_judge": unfair_pair_judge
        }

        return Response(result, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print(request.data)
        pass
