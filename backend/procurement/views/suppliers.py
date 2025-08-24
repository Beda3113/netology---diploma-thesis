from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .utils.import_parser import import_products_from_yaml


class SupplierImportAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.type != "shop":
            return Response({"error": "Только для поставщиков"}, status=403)
        url = request.data.get("url")
        success, msg = import_products_from_yaml(url, request.user)
        if success:
            return Response({"status": msg})
        else:
            return Response({"error": msg}, status=400)
