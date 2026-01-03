from django.contrib import admin
from .models import (
    RationCard, Beneficiary, FairPriceShop, Stock,
    Transaction, SupplyChain, Warehouse, UserAuth, AuditLog
)

# Register each model to appear in Django Admin
admin.site.register(RationCard)
admin.site.register(Beneficiary)
admin.site.register(FairPriceShop)
admin.site.register(Stock)
admin.site.register(Transaction)
admin.site.register(SupplyChain)
admin.site.register(Warehouse)
admin.site.register(UserAuth)
admin.site.register(AuditLog)

