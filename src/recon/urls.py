from rest_framework.routers import DefaultRouter

from src.recon.views import ReconciliationViewSet


recon_router = DefaultRouter()
recon_router.register(r"", ReconciliationViewSet, basename="reconciliation")
