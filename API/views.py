from http import HTTPStatus
import json
from django.shortcuts import get_object_or_404, render
from django.http import Http404, JsonResponse
from .models import TranSport_API
from rest_framework import status
from .models import TranSport_API
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt




def create(request):
    return render(request, 'Application/create_transport.html')

def info(request):
    return render(request, 'API/info_transport.html')
@csrf_exempt  
def CreateTranSport(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            weight = data.get('weight')
            name_ownerShop = data.get('name_ownerShop')
            name_customer = data.get('name_customer')
            product_name = data.get('product_name')
            quantity = data.get('quantity')
            description = data.get('description')
            customer_phone = data.get('customer_phone')
            from_district = data.get('from_district')
            from_province = data.get('from_province')
            to_district = data.get('to_district')
            to_province = data.get('to_province')
            expected_date = data.get('expected_date')
            transport_price = data.get('transport_price')
            created_at = data.get('created_at')
            updated_at = data.get('updated_at')
            if None in [ weight, name_ownerShop, name_customer, description, customer_phone, from_district, from_province, to_district, to_province, expected_date,transport_price, created_at, updated_at, product_name, quantity]:
                response_data = {
                    "status": HTTPStatus.BAD_REQUEST,
                    "mess": "bad request",
                    "serviceName": "USERSERVICE",
                    "body": {"data": False, "error": "bad request"},
                }
                return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)
            # price of transport
            weight = weight/1000;
            if weight > 1.0:
                mass = weight / 3;
                transport_price = transport_price + (int(mass)*5000)
            if from_province:
                if from_province != to_province:
                    transport_price = transport_price + 10000
            if quantity:
                if quantity > 1 and weight > 2:
                    transport_price = transport_price * (int(quantity)*5000)
                    
            transport = TranSport_API(
                weight=weight,
                name_ownerShop=name_ownerShop,
                name_customer=name_customer,
                product_name = product_name,
                quantity = quantity,
                description=description,
                customer_phone=customer_phone,
                from_district=from_district,
                from_province=from_province,
                to_district=to_district,
                to_province=to_province,
                expected_date=expected_date,
                transport_price=transport_price,
                created_at=created_at,
                updated_at=updated_at
            )
            transport.save()
            
            response_data = {
                "status": HTTPStatus.OK,
                "mess": "success",
                "serviceName": "TransportAPI",
                "body": {
                     "data":{
                        "id": transport.transport_id,
                        "ownershop":{
                            "name_ownerShop": transport.name_ownerShop,
                            "from_district": transport.from_district,
                            "from_province": transport.from_province,
                        },
                        "customer":{
                            "name_customer": transport.name_customer,        
                            "customer_phone": transport.customer_phone,
                            "to_district": transport.to_district,
                            "to_province": transport.to_province,
                        },
                        "order":{                            
                            "transport_code": transport.transprot_code,
                            "product_name": transport.product_name,
                            "quantity": transport.quantity,
                            "description": transport.description,
                            "weight": transport.weight,
                            "expected_date": transport.expected_date,
                            "transport_price": transport.transport_price,
                        },
                        "created_at": transport.created_at,
                        "updated_at": transport.updated_at
                    }
                }
            }
            return JsonResponse(response_data, status=HTTPStatus.CREATED)
        except Exception as e:
            print(e)
            response_data = {
                "status": HTTPStatus.INTERNAL_SERVER_ERROR,
                "mess": "error",
                "serviceName": "TransportAPI",
                "body": {"data": False, "error": "server error"},
            }
            return JsonResponse(response_data, status=HTTPStatus.INTERNAL_SERVER_ERROR)
    else:
        response_data = {
            "status": HTTPStatus.BAD_REQUEST,
            "mess": "bad request",
            "serviceName": "TransportAPI",
            "body": {"data": False, "error": "bad request"},
        }
        return JsonResponse(response_data, status=HTTPStatus.BAD_REQUEST)
    
    
    
@csrf_exempt  
def Price(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            weight = float(data.get('weight'))
            quantity = data.get('quantity')
            from_province = data.get('from_province')
            to_province = data.get('to_province')
            transport_price = 15000
            
            weight = weight/1000
            if weight > 1.0:
                mass = weight / 3
                transport_price = transport_price + (int(mass)*5000)
            if from_province:
                if from_province != to_province:
                    transport_price = transport_price + 10000
            if quantity:
                if quantity > 1 and weight > 2:
                    transport_price = transport_price * (int(quantity)*5000)
                
            response_data = {
                "status": HTTPStatus.OK,
                "mess": "success",
                "serviceName": "TransportAPI",
                "body": {
                    "data":{
                        "transport_price": transport_price
                    }
                }
            }
            return JsonResponse(response_data, status=HTTPStatus.CREATED)
        except Exception as e:
            print(e)
            response_data = {
                "status": HTTPStatus.INTERNAL_SERVER_ERROR,
                "mess": "error",
                "serviceName": "TransportAPI",
                "body": {"data": False, "error": "server error"},
            }
            return JsonResponse(response_data, status=HTTPStatus.INTERNAL_SERVER_ERROR)
    return JsonResponse({"error": "Invalid request method"}, status=HTTPStatus.BAD_REQUEST)



@csrf_exempt  
def UpdateTranSportAPI(request, transport_id):
    if request.method == "PATCH":
        try:
            transport = get_object_or_404(TranSport_API, uuid=transport_id)
            data = json.loads(request.body)
            new_weight = data.get('weight')
            new_name_ownerShop = data.get('name_ownerShop')
            new_name_customer = data.get('name_customer')
            new_product_name = data.get('product_name')
            new_quantity = data.get('quantity')
            new_description = data.get('description')
            new_customer_phone = data.get('customer_phone')
            new_from_district = data.get('from_district')
            new_from_province = data.get('from_province')
            new_to_district = data.get('to_district')
            new_to_province = data.get('to_province')
            new_expected_date = data.get('expected_date')
            new_transport_price = data.get('transport_price')
            new_created_at = data.get('created_at')
            new_updated_at = data.get('updated_at')

            if new_weight:
                transport.weight = new_weight
            if new_product_name:
                transport.product_name = new_product_name
            if new_quantity:
                transport.quantity = new_quantity
            if new_name_ownerShop:
                transport.name_ownerShop = new_name_ownerShop
            if new_name_customer:
                transport.name_customer = new_name_customer
            if new_description:
                transport.description = new_description
            if new_customer_phone:
                transport.customer_phone = new_customer_phone
            if new_from_district:
                transport.from_district = new_from_district
            if new_from_province:
                transport.from_province = new_from_province
            if new_to_district:
                transport.to_district = new_to_district
            if new_to_province:
                transport.to_province = new_to_province
            if new_expected_date:
                transport.expected_date = new_expected_date
            if new_transport_price:
                transport.transport_price = new_transport_price
            if new_created_at:
                transport.created_at = new_created_at
            if new_updated_at:
                transport.updated_at = new_updated_at
            transport.save()
            
            response_data = {
                "status": HTTPStatus.OK,
                "mess": "success",
                "serviceName": "TransportAPI",
                "body": {
                    "data":{
                        "id": transport.transport_id,
                        "ownershop":{
                            "name_ownerShop": transport.name_ownerShop,
                            "from_district": transport.from_district,
                            "from_province": transport.from_province,
                        },
                        "customer":{
                            "name_customer": transport.name_customer,        
                            "customer_phone": transport.customer_phone,
                            "to_district": transport.to_district,
                            "to_province": transport.to_province,
                        },
                        "order":{                            
                            "transport_code": transport.transprot_code,
                            "product_name": transport.product_name,
                            "quantity": transport.quantity,
                            "description": transport.description,
                            "weight": transport.weight,
                            "expected_date": transport.expected_date,
                            "transport_price": transport.transport_price,
                        },
                        "created_at": transport.created_at,
                        "updated_at": transport.updated_at
                    }
                }
            }
            
        except Exception as e:
            print(e)
            response_data = {
                "status": HTTPStatus.NOT_FOUND,
                "mess": "not found",
                "serviceName": "TransportAPI",
                "body": {"data": False, "error": "not found"},
            }
            return JsonResponse(response_data, status=HTTPStatus.NOT_FOUND)
        
        
        
def manager(request):
    return render(request, 'API/manager.html')
        

# @csrf_exempt
# def info_transport(request):
#     try:
#         transport = get_object_or_404(TranSport_API, transport_code=transport_code)
#         context = {
#             'transport': transport
#         }
#         print(context)
#         return render(request, 'API/info_transport.html', context)
    
            
#     except:
#         response_data = {
#             "status": HTTPStatus.NOT_FOUND,
#             "mess": "not found",
#             "serviceName": "TransportAPI",
#             "body": {"data": False, "error": "not found"},
#         }
#         return JsonResponse(response_data, status=HTTPStatus.NOT_FOUND)

def home(request):
    return render(request, 'API/base.html')

@csrf_exempt
def info_transport(request):
    if request.method == "POST":
        transport_code = request.POST.get('transport_code', '')
        try:
            transport = get_object_or_404(TranSport_API, transport_code=transport_code)
            context = {
                'transport': transport
            }
            print(context)
            return render(request, 'Application/info_transport.html', context)
        except:
            return render(request, 'Application/info_transport.html')
    else:
        # Xử lý trường hợp GET nếu cần
        return render(request, 'Application/info_transport.html')

@csrf_exempt        
def Search_Transport(request):
    try:
        keyword = request.GET.get('keyword', '')
        
        if not keyword:
            return render(request, 'API/manager.html', {'transport_code': keyword})

        transport = get_object_or_404(TranSport_API, transprot_code=keyword)
        
        response_data = {
            "status": HTTPStatus.OK,
            "mess": "success",
            "serviceName": "TransportAPI",
            "body": {
                "data": {
                    "id": transport.transport_id,
                    "ownershop": {
                        "name_ownerShop": transport.name_ownerShop,
                        "from_district": transport.from_district,
                        "from_province": transport.from_province,
                        "address_sender": transport.address_sender
                    },
                    "customer": {
                        "name_customer": transport.name_customer,
                        "customer_phone": transport.customer_phone,
                        "to_district": transport.to_district,
                        "to_province": transport.to_province,
                        "address_receiver": transport.address_receiver
                    },
                    "order": {
                        "transport_code": transport.transport_code,
                        "product_name": transport.product_name,
                        "quantity": transport.quantity,
                        "description": transport.description,
                        "weight": transport.weight,
                        "expected_date": transport.expected_date,
                        "transport_price": transport.transport_price,
                    },
                    "created_at": transport.created_at,
                    "updated_at": transport.updated_at
                }
            }
        }
        
        return JsonResponse(response_data, status=HTTPStatus.OK)
    
    except Exception as e:
        print(e)
        response_data = {
            "status": HTTPStatus.NOT_FOUND,
            "mess": "not found",
            "serviceName": "TransportAPI",
            "body": {"data": False, "error": "not found"},
        }
        return JsonResponse(response_data, status=HTTPStatus.NOT_FOUND)