from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes 
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import redirect, get_object_or_404

from auths.permissions import isAdmin, isManager
from .models import Hospital, Doctor, Major, School, SalesHistory, Product
from .serializers import HospitalSerializer, DoctorSerializer, \
                         MajorSerializer, SchoolSerializer, \
                         UserCountSerializer, StatusCountSerializer, \
                         DateCountSerializer, DashboardSerializer,\
                         SalesHistorySerializer, SalesHistoryCreateSerializer, \
                         SalesHistoryRecentSerializer, ProductSerializer
                         

from .utils.hosp_fetch import get_hospinfo_openapi                
                        

class DoctorViewSet(viewsets.ModelViewSet):
    '''
    Doctor ViewSet 
    
    crud operation on doctor model
    permission: Admin
    
    '''
    def get_permissions(self):
        actions = ['update', 'partial_update', 'destroy']

        if self.action in actions:
            permission_classes = [IsAuthenticated & isAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


@extend_schema_view(
    list=extend_schema(
        parameters= [
            OpenApiParameter('class_code', OpenApiTypes.STR, OpenApiParameter.QUERY, required= False, description='Filter hospitals by class_code e.g. 종합병원'),
            OpenApiParameter('manager_id', OpenApiTypes.INT, OpenApiParameter.QUERY, required= False, description='Filter hospitals by manager_id e.g. 1'),
            OpenApiParameter('ordering', OpenApiTypes.STR, OpenApiParameter.QUERY, required= False, description='Orders hospital by param | available fields: hospital_name, established_at'),
            OpenApiParameter('search', OpenApiTypes.STR, OpenApiParameter.QUERY, required= False, description='Search hospital by param | available fields: hospital_name, director_name'),
            OpenApiParameter('page', OpenApiTypes.INT, OpenApiParameter.QUERY, required= False, description= 'Returns hospital based on page, default=1, items_per page=40')
        ],
    responses={200: HospitalSerializer(many=True)},  
    )
)
class HospitalViewSet(viewsets.ModelViewSet):
    '''
    Hospital ViewSet

    crud, pagination, searchfilter, orderfilter 기능을 제공
    
    Default order: hospital_name

    '''
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['class_code', 'manager__id']
    search_fields = ['hospital_name', 'director__name']
    ordering_fields = ['hospital_name', 'established_at']
    ordering = ['hospital_name']
    
    def get_permissions(self):
        actions = ['create', 'update', 'partial_update', 'destroy']

        if self.action in actions:
            permission_classes = [IsAuthenticated & (isManager|isAdmin)]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
        
class MajorViewSet(viewsets.ModelViewSet):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer
    def get_permissions(self):
        actions = ['create', 'update', 'partial_update', 'destroy']

        if self.action in actions:
            permission_classes = [IsAuthenticated & isAdmin]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    
    def get_permissions(self):
        actions = ['create', 'update', 'partial_update', 'destroy']

        if self.action in actions:
            permission_classes = [IsAuthenticated & isAdmin]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

class SalesHistoryListView(APIView):
    '''
    SalesHistoryView List, Post View

    *query performance differs by using select_related, and prefetch related
    '''

    @extend_schema(
    methods=['get'],
    parameters= [
        OpenApiParameter('hospital_id', OpenApiTypes.STR, OpenApiParameter.QUERY, required= False, description='Filters result based on hospital id(요양기호) e.g. JDQ4MTAxMiM1MSMkMSMkMCMkODkkMzgxMzUxIzExIyQyIyQzIyQwMCQyNjE0ODEjNjEjJDEjJDgjJDgz '),
        OpenApiParameter('page', OpenApiTypes.INT, OpenApiParameter.QUERY, required= False, description= 'Returns result based on page, default=1, items_per page=20'),
        OpenApiParameter('ordering', OpenApiTypes.STR, OpenApiParameter.QUERY, required= False, description='Orders result based on fields | available fields: modified_at, (요양기호)hospital, status, (saleshistory)id'),
    ],
    responses={200: SalesHistorySerializer(many=True)},
    # more customizations
    )
    def get(self, request):
        '''
        no parameter:
        
        list: returns The entire list of sales history, ordered by modified date, and hospital id
        
        parameter hospital:
        
        list: returns The filtered list of saleshistory on a hospital id
        params: hospital (hospital_id: str)

        parameter page
        '''
        
        hospital = request.query_params.get('hospital', None)
        
        if hospital is not None:
            queryset = SalesHistory.objects.filter(hospital=hospital)\
                                          .order_by('-modified_at', 'hospital')\
                                          .select_related('hospital__manager', 'hospital__director')
        else:
            queryset = SalesHistory.objects.all().order_by('-modified_at', 'hospital')\
                                                .select_related('hospital__manager', 'hospital__director')
        
        page = request.query_params.get('page', 1)
        ordering = request.query_params.get('ordering', None)

        if ordering is not None:
            ORDERING_FIELDS = [
                'modified_at', '-modified_at',
                'hospital', '-hospital',
                'id', '-id',
                'status', '-status',
                'hospital_name', '-hospital_name'
                ]
            if ordering in ORDERING_FIELDS:
                if ordering == 'hospital_name':
                    ordering = 'hospital__' + ordering
                elif ordering == '-hospital_name':
                    ordering = '-hospital__' + ordering
                    
                queryset = queryset.order_by(ordering)
        
        if page is not None:
            from django.core.paginator import Paginator
            paginator = Paginator(queryset, 20)  # 20 per page
            queryset = paginator.get_page(page)

        serializer = SalesHistorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    @extend_schema(
        methods=['POST'],
        request = SalesHistoryCreateSerializer,
        responses = {201: SalesHistoryCreateSerializer, 400:{'description': 'Invalid Parameters', 'example': {'description': 'Invalid Parameters'}}}
        # more customizations
    )
    def post(self, request, format=None):
        '''
        post: creates new saleshistory

        required: hospital_id, status: (A,B,O,F,P), content
        
        permission: need to be manager of hospital
        '''
        
        serializer = SalesHistoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    allowed_methods = ['get', 'post']


class SalesHistoryDetailsView(APIView):
    '''
    SalesHistoryView Based on saleshistory id(pk)

    ** Requires Permission (Hospital Manager) or Admin
    '''
    
    def get_object(self, pk):
        try:
            return SalesHistory.objects.get(pk=pk)
        except SalesHistory.DoesNotExist:
            return Response({'pk not found'}, status=status.HTTP_404_NOT_FOUND)

    def check_owner(self, obj):
        # Checks if user is the manager of the hospital
        return (obj.hospital.manager == self.request.user) or (self.request.user.is_admin)
    
    @extend_schema(
        methods=['GET'],
        responses = {200: SalesHistorySerializer, 404:{'description': 'Invalid saleshistory id(pk)', 'example': {'description': 'Invalid saleshistory id(pk)'}}},
        # more customizations
    )
    def get(self, request, pk=None):
        '''
        get: returns single saleshistory based on pk(id:int)
        '''
        history = self.get_object(pk)                            
        serializer = SalesHistorySerializer(history)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @extend_schema(
        methods=['PUT'],
        parameters=[
          OpenApiParameter("id (history)", OpenApiParameter.PATH, required=True),
        ],
        request = SalesHistoryCreateSerializer,
        responses = {200: SalesHistorySerializer, 
                     404: {'description': 'Invalid saleshistory id(pk)', 'example': {'description': 'Invalid saleshistory id(pk)'}},
                     403: {'description': 'Insufficient Permission', 'example': {'description': 'Insufficient Permission'}}}
        # more customizations
    )
    def put(self, request, pk):
        '''
        put: updates saleshistory
        permission: need to be manager of hospital & owner of history
        '''
        item = self.get_object(pk)
        
        # Checks for owner permission
        if not self.check_owner(item):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = SalesHistoryCreateSerializer(instance=item, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


    @extend_schema(
        methods=['PATCH'],
        description='partial update saleshistory only requires id',
        parameters=[
          OpenApiParameter("id (history)", OpenApiParameter.PATH, required=True)
        ],
        request = SalesHistoryCreateSerializer,
        responses = {200: SalesHistorySerializer,
                     404: {'description': 'Invalid saleshistory id(pk)', 'example': {'description': 'Invalid saleshistory id(pk)'}},
                     403: {'description': 'Insufficient Permission', 'example': {'description': 'Insufficient Permission'}}}
        # more customizations
    )
    def patch(self, request, pk):
        '''
        patch: 	partially updates saleshistory
        permission: need to be manager of hospital & owner of history 
        
        '''
        item = self.get_object(pk)

        if not self.check_owner(item):
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = SalesHistoryCreateSerializer(instance=item, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(data=serializer.error_messages, status=status.HTTP_404_NOT_FOUND)
    
    @extend_schema(
        methods=['DELETE'],
        parameters = [OpenApiParameter("id (history)", OpenApiParameter.PATH, required=True)],
        responses={204: 'No content',
                   404: {'description': 'Invalid saleshistory id(pk)', 'example': {'description': 'Invalid saleshistory id(pk)'}},
                   403: {'description': 'Insufficient Permission', 'example': {'description': 'Insufficient Permission'}}}
    )
    def delete(self, request, pk):
        '''
        Delete History
        
        permission: need to be manager of hospital & owner of history
        '''
        item = self.get_object(pk)

        if not self.check_owner(item):
            return Response(status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(item)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
    
    allowed_methods = ['get','put','patch','delete']


class SalesHistoryRecentView(APIView):
    '''
    SalesHistoryView List Sales History of current logged in user
    '''
    allowed_methods = ['get']
 
    @extend_schema(
        methods=['GET'],
        parameters= [
            OpenApiParameter('hospital_id', OpenApiTypes.STR, OpenApiParameter.QUERY, required= False, description='Filters result based on hospital id(요양기호) e.g. JDQ4MTAxMiM1MSMkMSMkMCMkODkkMzgxMzUxIzExIyQyIyQzIyQwMCQyNjE0ODEjNjEjJDEjJDgjJDgz '),
            OpenApiParameter('page', OpenApiTypes.INT, OpenApiParameter.QUERY, required= False, description= 'Returns result based on page, default=1, items_per page=20'),
            OpenApiParameter('ordering', OpenApiTypes.STR, OpenApiParameter.QUERY, required= False, description='Orders result based on fields | available fields: modified_at, (요양기호)hospital, status, (saleshistory)id'),
        ],
        responses = {200: SalesHistoryRecentSerializer(many=True)},
        # more customizations
    )
    def get(self, request):
        '''
        get: returns list of saleshistories created by the current user logged in
        '''
        
        hospital = request.query_params.get('hospital_id', None)

        if hospital is not None:
            queryset = SalesHistory.objects.filter(hospital__manager=request.user, hospital=hospital) \
                                            .order_by('-modified_at') \
                                            .select_related('hospital__manager')
        else:
            queryset = SalesHistory.objects.filter(hospital__manager=request.user) \
                                        .order_by('-modified_at') \
                                        .select_related('hospital__manager')



        page = request.query_params.get('page', 1)
        ordering = request.query_params.get('ordering', None)

        if ordering is not None:
            ORDERING_FIELDS = [
                'modified_at', '-modified_at',
                'hospital', '-hospital',
                'id', '-id',
                'status', '-status',
                ]
            if ordering in ORDERING_FIELDS:
                queryset = queryset.order_by(ordering)
        
        if page is not None:
            from django.core.paginator import Paginator
            paginator = Paginator(queryset, 20)  # 20 per page
            queryset = paginator.get_page(page)

        serializer = SalesHistoryRecentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class DashboardView(APIView):
    '''
    Dashboard View various insightful data
    
    '''
    @extend_schema(
    methods=['get'],
    responses={200: DashboardSerializer(many=True)},
    )
    def get(self, request):
        '''
        list: returns various insightful stats in serialized forms  
        '''
        from django.db.models import Count, F
        from django.db.models.functions import TruncDate
    
        # saleshistory count by status:
        status_cnt = SalesHistory.objects.values('status').annotate(count = Count('status'))
        ## 'status' : 'A', 'count': 2 // charfield, integerfield

        status_cnt = StatusCountSerializer(status_cnt, many=True)

        # saleshistory count by date:
        date_cnt = SalesHistory.objects.annotate(date = TruncDate('modified_at')).values('date').annotate(count=Count('date'))

        ## 'date':datetime.date(2023,5,16), 'count':2 // Datefield, integerfield
        date_cnt = DateCountSerializer(date_cnt, many=True)
        
        # saleshistory count by user: 
        user_cnt = SalesHistory.objects.values('hospital__manager').annotate(count=Count('hospital__manager'))
        
        user_cnt = UserCountSerializer(user_cnt, many=True)
        ## 'hospital__manager' : 2, 'count': 2 // integerfield, integerfield

        total_cnt = {
            'user_cnt' : user_cnt.data,
            'date_cnt' : date_cnt.data,
            'status_cnt' : status_cnt.data
        }
        dashboard = DashboardSerializer(total_cnt)

        return Response(dashboard.data, status=status.HTTP_200_OK)
    
class ProductView(generics.ListAPIView):
    '''
    제품정보 (Products View)
    '''
    queryset = 	Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['hospital']
    search_fields = ['name', 'hospital__name']
    ordering_fields = ['name', 'hospital']
    ordering = ['name']

class ProductCreateView(generics.CreateAPIView):
    queryset = 	Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [isAdmin]
    
class ProductDetailsView(generics.RetrieveUpdateDestroyAPIView):
    '''
    제품 단일정보 / 조회, 수정, 삭제
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [isAdmin]
    
        