from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from requests import request
from .models import UserAuth, Beneficiary,FairPriceShop
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import qrcode
import io


# Home view
def home(request):
    return render(request, 'ration_app/home.html')

# Registration view
def register_view(request):
    if request.method == "POST":
        # ---- Extract form data ----
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address_line = request.POST.get('address')   # renamed field in model
        full_name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        income = request.POST.get('income')

        # ---- Basic validation ----
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        try:
            age = int(age)
            income = float(income)
        except ValueError:
            messages.error(request, "Invalid age or income format.")
            return redirect('register')

        # ---- Create User ----
        user = User.objects.create_user(username=username, password=password, email=email)

        # ---- Create UserAuth ----
        user_auth = UserAuth.objects.create(
            user=user,
            role='citizen',
            full_name=full_name,
            age=age,
            gender=gender,
            phone=phone,
            address_line=address_line,
            city=city,
            state=state,
            pincode=pincode,
            income=income
        )

        # create Beneficiary
        Beneficiary.objects.create(
            name=full_name,
            age=age,
            gender=gender,
            address=address_line,
            city=city,
            state=state,
            pincode=pincode,
            income=income
        )

        messages.success(request, "Registration successful! You can now login.")
        return redirect('login')

    return render(request, 'ration_app/user/user_registration.html')




# Login view
def user_login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'ration_app/user/user_login.html')





# Shop login view
def shop_login_view(request):
    if request.method == "POST":
        shop_name = request.POST.get("shop_name")
        license_number = request.POST.get("license_number")

        try:
            shop = FairPriceShop.objects.get(shop_name=shop_name, license_number=license_number)
            request.session['shop_id'] = shop.id
            request.session['shop_name'] = shop.shop_name
            messages.success(request, f"Welcome, {shop.shop_name}!")
            return redirect("shop_dashboard")
        except FairPriceShop.DoesNotExist:
            messages.error(request, "Invalid Shop Name or License Number.")

    return render(request, "ration_app/shopkeeper/shop_login.html")





#user_dashboard view
def user_dashboard(request):

    return render(request, 'ration_app/user/user_dashboard.html')



# Shop dashboard view
def shop_dashboard(request):
    shop = None

    # Try to load from session if you stored shop_id during login
    shop_id = request.session.get('shop_id')
    if shop_id:
        try:
            shop = FairPriceShop.objects.get(id=shop_id)
        except FairPriceShop.DoesNotExist:
            pass

    # Fallback: if logged in through Django user
    elif hasattr(request.user, 'shopkeeper'):
        shop = request.user.shopkeeper.first()

    if not shop:
        return redirect('shop_login')  # redirect if no shop session

    return render(request, 'ration_app/shopkeeper/shop_dashboard.html', {'shop': shop})




#logout view
def logout_view(request):
    logout(request)
    return redirect('login')





# QR Code generation view
def generate_ration_qr(request):
    try:
        userauth = getattr(request.user, "userauth", None)
        if not userauth:
            return HttpResponse("User data not found", status=404)

        rationcard = getattr(userauth, "rationcard", None)

        data = {
            "Full Name": getattr(userauth, "full_name", "Unknown"),
            "Ration Card": getattr(rationcard, "card_number", "Not Issued"),
            "Category": getattr(rationcard, "category", "N/A"),
            "Address": f"{getattr(userauth, 'address_line', '')}, {getattr(userauth, 'city', '')}, {getattr(userauth, 'state', '')}",
            "Phone": getattr(userauth, "phone", "N/A"),
        }

        # Convert dictionary to readable text
        qr_text = "\n".join(f"{k}: {v}" for k, v in data.items())

        # Generate QR
        qr = qrcode.make(qr_text)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)

        return HttpResponse(buffer.getvalue(), content_type="image/png")

    except Exception as e:
        print("❌ QR Generation Error:", e)
        return HttpResponse("Error generating QR", status=500)
