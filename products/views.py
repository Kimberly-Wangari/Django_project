from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from category.models import Category

def add_product(request):
    """
    Simple view to add a product using an HTML form (no Django ModelForm required).
    """
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        category_id = request.POST.get("category")
        description = request.POST.get("description", "")
        image = request.FILES.get("image")

        # Basic validation (ensure required fields exist)
        if not name or not price or not category_id:
            categories = Category.objects.all()
            return render(request, "products/add_product.html", {
                "categories": categories,
                "error": "Name, price and category are required."
            })

        category = get_object_or_404(Category, id=category_id)

        Product.objects.create(
            name=name,
            price=price,
            category=category,
            description=description,
            image=image
        )
        return redirect("product_list")

    categories = Category.objects.all()
    return render(request, "products/add_product.html", {"categories": categories})


def product_list(request):
    """
    Display all products.
    """
    products = Product.objects.select_related("category").all().order_by("-created_at")
    return render(request, "products/product_list.html", {"products": products})


def product_detail(request, pk):
    """
    Optional: product detail view.
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {"product": product})
