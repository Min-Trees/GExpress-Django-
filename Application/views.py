from django.shortcuts import render
from rest_framework import viewsets
from .models import Transport, Order , Payment , TransportByEcm 
from .serializers import  Serializers_Transprot , Serializers_Order , Serializers_Transprot_By_Ecm
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Account
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import requests
from django.core.cache import cache
from .mixins import MessagseHandler
import random 
import string

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = Serializers_Order
class TransportViewSet(viewsets.ModelViewSet):
    queryset = Transport.objects.all()
    serializer_class = Serializers_Transprot
class TransportByEcmViewSet(viewsets.ModelViewSet):
    queryset = TransportByEcm.objects.all()
    serializer_class = Serializers_Transprot_By_Ecm 


def body(request):
    return render(request, 'Application/home.html')

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
        email = request.POST['email']
        phone = request.POST['phone']
        
        Account.objects.create(user_name=user_name,email=email, phone=phone)
        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')
       
    
    return render(request, 'Application/signup.html')


 
def generate_otp():
    otp = ''.join(random.choices(string.digits, k=4))
    return otp 
 
def user_login(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')

        phone = request.session.get('phone')
        saved_otp = request.session.get('otp')

        if saved_otp and otp_entered == saved_otp:
            del request.session['phone']
            del request.session['otp']
            messages.success(request, 'Xác thực thành công!')
            return redirect('home')
        else:
            messages.error(request, 'Mã OTP không hợp lệ. Vui lòng thử lại.')
            print('Mã OTP không hợp lệ. Vui lòng thử lại.')
            return redirect('login')
    else:
        return render(request, 'Application/login.html')
    
def send_otp(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if not phone.startswith('+'):
            phone = '+' + phone
        otp = generate_otp()  # Tạo mã OTP mới
        message_handler = MessagseHandler(phone, otp)
        message_handler.send_otp(phone, otp)
        request.session['phone'] = phone
        request.session['otp'] = otp
        return redirect('verify_otp')
    else:
        return redirect('login')

def verify_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        phone = request.session.get('phone')
        saved_otp = request.session.get('otp')

        if saved_otp and otp_entered == saved_otp:
            del request.session['phone']
            del request.session['otp']
            messages.success(request, 'Xác thực thành công!')
            return redirect('homew')  
        else:
            messages.error(request, 'Mã OTP không hợp lệ. Vui lòng thử lại.')
            return redirect('verify_otp')  
    else:
        
        return render(request, 'Application/verify_otp.html')
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
    
def guest(request):
    return render(request, 'Application/guest.html')

def profile(request):
    user = request.user
    print(user)
    return render(request, 'Application/profile.html', {'user': user})

@login_required
def total_order(request, user_id):
    orders = Order.objects.filter(id_customer=user_id)
    context = {
        'orders': orders,
    }
    return render(request, 'Application/total_order.html', context)

from .models import Province, District

def location_select(request):
    provinces = get_provinces()
    selected_province_id = request.GET.get('province_id')
    districts = get_districts(selected_province_id)
    select_district_id = request.GET.get('district_id')
    wards = get_wards(select_district_id)

    return render(request, 'Application/create_transport.html', {'provinces': provinces, 'districts': districts, 'selected_province_id': selected_province_id, 'wards': wards, 'select_district_id': select_district_id})

def get_provinces():
    provinces_response = requests.get("https://vnprovinces.pythonanywhere.com/api/provinces/?basic=true&limit=100")
    if provinces_response.status_code == 200:
        provinces_data = provinces_response.json()
        provinces = provinces_data.get('results', [])
    else:
        provinces = []
    return provinces

def get_districts(selected_province_id):
    districts = []
    if selected_province_id:
        districts_response = requests.get(f"https://vnprovinces.pythonanywhere.com/api/districts/?province_id={selected_province_id}&basic=true&limit=100")
        if districts_response.status_code == 200:
            districts_data = districts_response.json()
            districts = districts_data.get('results', [])
    return districts

def get_wards(selected_district_id):
    wards = []
    if selected_district_id:
        wards_response = requests.get(f"https://vnprovinces.pythonanywhere.com/api/wards/?district_id={selected_district_id}&basic=true&limit=100")
        if wards_response.status_code == 200:
            wards_data = wards_response.json()
            wards = wards_data.get('results', [])
    print("wards:", wards)  
    return wards
