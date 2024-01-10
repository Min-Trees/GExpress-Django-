from django.shortcuts import render
from rest_framework import viewsets
from .models import Transport, Order , Payment , TransportByEcm
from .serializers import  Serializers_Transprot , Serializers_Order , Serializers_Transprot_By_Ecm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Account
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = Serializers_Order
class TransportViewSet(viewsets.ModelViewSet):
    queryset = Transport.objects.all()
    serializer_class = Serializers_Transprot
class TransportByEcmViewSet(viewsets.ModelViewSet):
    queryset = TransportByEcm.objects.all()
    serializer_class = Serializers_Transprot_By_Ecm 

def TransportByEcm(request):
    try:
        if request.method == 'POST':
            name_product = request.POST['name_product']
            weigth = request.POST['weigth']
            from_send = request.POST['from_send']
            to_send = request.POST['to_send']
            transport_price = request.POST['transport_price']
            if None in [name_product, weigth, from_send, to_send, transport_price]:
                messages.error(request, 'Invalid transport.')
                return JsonResponse({'error': 'Invalid transport'}, status=status.HTTP_400_BAD_REQUEST)
            
            Transport.objects.create(name_product=name_product, weigth=weigth, from_send=from_send, to_send=to_send, transport_price=transport_price)
            messages.success(request, 'Transport inserted successfully.')
            response_data = Serializers_Transprot_By_Ecm.as_view({
                'get': 'list',
                'post': 'create',
                'put': 'update',
                'delete': 'destroy'
            })
            return JsonResponse(response_data, status=status.HTTP_200_OK)
    except:
        messages.error(request, 'Invalid transport.')
        return JsonResponse({'error': 'Invalid transport'}, status=status.HTTP_400_BAD_REQUEST)
   
#xac thuc quyen user ownershop va quyen CRUD order va transport
def manager_order(request , userId):
    try:
        user = get_object_or_404(Account,user_id = userId)
        if(user.role == 'Shop'):
            response_data = OrderViewSet.as_view({
                'get': 'list',
                'post': 'create',
                'put': 'update',
                'delete': 'destroy'
            })
            return JsonResponse(response_data, status=status.HTTP_200_OK)
    except:
        return JsonResponse({'error': 'You do not have permission to view this content'}, status=status.HTTP_400_BAD_REQUEST)
def manager_transport(request , userId):
    try:
        user = get_object_or_404(Account,user_id = userId)
        if(user.role == 'Shop'):
            response_data = OrderViewSet.as_view({
                'get': 'list',
                'post': 'create',
                'put': 'update',
                'delete': 'destroy'
            })
            return JsonResponse(response_data, status=status.HTTP_200_OK)
    except:
        return JsonResponse({'error': 'You do not have permission to view this content'}, status=status.HTTP_400_BAD_REQUEST)
#xac thuc quyen user customer va shipper va quyen xem order va transport
def query_transport(request , userId):
    try:
        user = get_object_or_404(Account,user_id = userId)
        if(user.role == 'Shipper' or user.role == 'Customer'):
            response_data = TransportViewSet.as_view({
                'get': 'list',
                
            })
            return JsonResponse(response_data, status=status.HTTP_200_OK)
    except:
        return JsonResponse({'error': 'You do not have permission to view this content'}, status=status.HTTP_400_BAD_REQUEST)

def query_transport(request , userId):
    try:
        user = get_object_or_404(Account,user_id = userId)
        if(user.role == 'Customer'):
            response_data = OrderViewSet.as_view({
                'get': 'list',
                
            })
            return JsonResponse(response_data, status=status.HTTP_200_OK)
    except:
        return JsonResponse({'error': 'You do not have permission to view this content'}, status=status.HTTP_400_BAD_REQUEST)
    
'''class Update_StatusOder(APIView):
    def patch(self, request, order_id):
        try:
            order_id = Order.objects.get(pk = order_id)
        except:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        new_status = request.data.get('type')
        
        if new_status not in [choice[0] for choice in Order.Status_choices]:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        Order.type = new_status
        Order.save()
        
        serializer = Serializers_Order(Order)
        return Response(serializer.data, status=status.HTTP_200_OK)
'''

def register(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        password = request.POST['password']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        pay = request.POST.get('pay', None)
        role = request.POST['role']
        
        Account.objects.create(user_name=user_name, password=password, email=email, phone=phone, address=address, pay=pay, role=role)
        messages.success(request, 'Account created successfully. Please login.')
            
        return redirect('login')
    return render(request, 'Application/register.html')
 
def user_login(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        password = request.POST['password']

        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'Application/login.html')


def account_baking(request):
    if request.method == 'POST':
        account_pay = request.POST['account_pay']
        account_name = request.POST['account_name']
        cvv_pay  =  request.POST['cvv_pay']
        expiration_month =  request.POST['expiration_month']
        expiration_year =  request.POST['expiration_year']  

        Payment.objects.create(account_pay=account_pay, account_name=account_name, cvv_pay=cvv_pay, expiration_month=expiration_month, expiration_year=expiration_year)
        messages.success(request, 'Account Pay inserted successfully. Please login.')
        return render(request, 'Application/payment.html')

    else:
        messages.error(request, 'Invalid account pay.')
        return render(request, 'Application/payment.html')
        
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('login') 

'''@require_http_methods(["GET"])
def check_order(request):
    if request.method == 'POST':
        order_id = request.POST['order_id']
        try:
            order = Order.objects.get(order_id=order_id)
            return render(request, 'Application/check_order.html', {'order': order})
        except:
            messages.error(request, 'Invalid order id.')
    return render(request, 'Application/check_order.html')'''
    
    

