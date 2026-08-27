from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F
from .models import Asset, AssetCategory, AssetIssue
from .forms import AssetForm, AssetCategoryForm, AssetIssueForm

@login_required
def inventory_dashboard(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
        
    total_assets_count = Asset.objects.count()
    total_quantity = Asset.objects.aggregate(total=Sum('quantity'))['total'] or 0
    total_value = Asset.objects.aggregate(total=Sum(F('quantity') * F('unit_price')))['total'] or 0
    total_issues = AssetIssue.objects.count()
    
    recent_issues = AssetIssue.objects.select_related('asset', 'issued_to__user').order_by('-issue_date')[:5]
    categories = AssetCategory.objects.all()
    
    context = {
        'total_assets_count': total_assets_count,
        'total_quantity': total_quantity,
        'total_value': total_value,
        'total_issues': total_issues,
        'recent_issues': recent_issues,
        'categories': categories,
    }
    return render(request, 'inventory/dashboard.html', context)

@login_required
def asset_list(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    assets = Asset.objects.select_related('category').all().order_by('name')
    return render(request, 'inventory/asset_list.html', {'assets': assets})

@login_required
def asset_create(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Équipement ajouté au stock avec succès.")
            return redirect('inventory:asset_list')
    else:
        form = AssetForm()
    return render(request, 'inventory/form.html', {'form': form, 'title': 'Ajouter un Équipement / Matériel'})

@login_required
def asset_update(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, "Équipement mis à jour.")
            return redirect('inventory:asset_list')
    else:
        form = AssetForm(instance=asset)
    return render(request, 'inventory/form.html', {'form': form, 'title': "Modifier l'Équipement"})

@login_required
def asset_delete(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        asset.delete()
        messages.success(request, "Équipement supprimé.")
        return redirect('inventory:asset_list')
    return render(request, 'inventory/confirm_delete.html', {'object': asset, 'title': "Supprimer l'équipement"})

@login_required
def category_list(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    categories = AssetCategory.objects.all().order_by('name')
    return render(request, 'inventory/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    if request.method == 'POST':
        form = AssetCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie créée avec succès.")
            return redirect('inventory:category_list')
    else:
        form = AssetCategoryForm()
    return render(request, 'inventory/form.html', {'form': form, 'title': 'Ajouter une Catégorie'})

@login_required
def issue_list(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    issues = AssetIssue.objects.select_related('asset', 'issued_to__user').all().order_by('-issue_date')
    return render(request, 'inventory/issue_list.html', {'issues': issues})

@login_required
def issue_create(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    if request.method == 'POST':
        form = AssetIssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            if issue.asset.quantity >= issue.quantity:
                issue.asset.quantity -= issue.quantity
                issue.asset.save()
                issue.save()
                messages.success(request, "Attribution effectuée et stock mis à jour.")
                return redirect('inventory:issue_list')
            else:
                messages.error(request, "Quantité insuffisante en stock.")
    else:
        form = AssetIssueForm()
    return render(request, 'inventory/form.html', {'form': form, 'title': 'Attribuer un Équipement à un Personnel'})
