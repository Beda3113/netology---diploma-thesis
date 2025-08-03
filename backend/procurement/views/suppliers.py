from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .utils.import_parser import import_products_from_yaml

class SupplierImportAPI(APIView):
    """Импорт товаров поставщиками через YAML"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'supplier':
            return Response({'error': 'Только для поставщиков'}, status=403)
        
        yaml_url = request.data.get('url')
        try:
            import_products_from_yaml(yaml_url, request.user)
            return Response({'status': 'Импорт завершён'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)
