from django.shortcuts import render, redirect
from django.db import models
from django.db.models import Q
from .models import Pier, Boat, Bookings, CustomUser
from .forms import PierForm, BoatForm, RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from .utils import check_email, email_confirmation
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import Workbook


# Create your views here.
def home(request):
    return render(request, "home.html")


""" Pier and Boat managing views"""


@login_required
def create_pier(request):
    if request.method == "GET":
        return render(request, "pier_create.html", {"form": PierForm()})

    if request.method == "POST":
        form = PierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("piers")
        else:
            error = "Formularz zawiera błędy."
            return render(request, "pier_create.html", {"error": error})


@login_required
def pier_edit(request, pier_id):
    pier = Pier.objects.get(id=pier_id)
    if request.method == "GET":
        form = PierForm(instance=pier)
        return render(request, "pier_create.html", {"form": form})

    if request.method == "POST":
        form = PierForm(request.POST, instance=pier)
        if form.is_valid():
            form.save()
            return redirect("piers")
        else:
            error = "Formularz zawiera błędy."
            return render(request, "pier_create.html", {"error": error, "form": form})


@login_required
def pier_delete(request, pier_id):
    pier = Pier.objects.get(id=pier_id)
    pier.delete()
    return redirect('piers')


@login_required
def pier_list(request):
    piers = Pier.objects.all()
    return render(request, "piers.html", {"piers": piers})


@login_required
def create_boat(request):
    if request.method == "GET":
        return render(request, "boat_create.html", {"form": BoatForm()})

    if request.method == "POST":
        form = BoatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("boats")
        else:
            error = "Formularz zawiera błędy."
            print(form.errors)
            return render(request, "boat_create.html", {"error": error})


@login_required
def boat_edit(request, boat_id):
    boat = Boat.objects.get(id=boat_id)
    if request.method == "GET":
        form = BoatForm(instance=boat)
        return render(request, "boat_create.html", {"form": form})

    if request.method == "POST":
        form = BoatForm(request.POST, request.FILES, instance=boat)
        if form.is_valid():
            form.save()
            return redirect("boats")
        else:
            error = "Formularz zawiera błędy."
            print(form.errors)
            return render(request, "boat_create.html", {"form": form, "error": error})


@login_required
def boat_delete(request, boat_id):
    boat = Boat.objects.get(id=boat_id)
    boat.delete()
    return redirect("boats")


def boat_list(request):
    boats_list = Boat.objects.all()
    return render(request, "boats.html", {"boats_list": boats_list})


def boat_detail(request, boat_id):
    boat = Boat.objects.get(id=boat_id)
    return render(request, "boat_detail.html", {"boat_detail": boat})


""" User authorization views """


def register(request):
    if request.method == "GET":
        return render(request, "register.html", {"user_form": RegisterForm()})

    if request.method == "POST":
        form = RegisterForm(request.POST)

        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            username_taken = CustomUser.objects.filter(username=username).exists()
            email_taken = CustomUser.objects.filter(email=email).exists()

            if username_taken:
                error = "Wybrana nazwa użytkownika jest zajęta."
            if email_taken:
                error = "Użytkownik o podanym emailu jest już w bazie."

            if not username_taken and not email_taken:
                email_valid = check_email(email)
                if email_valid:
                    try:
                        validate_password(password1)
                    except ValidationError as e:
                        return render(request, "register.html",
                                      {'password_errors': e.messages, 'user_form': RegisterForm()})
                    else:
                        if form.is_valid():
                            user = form.save(commit=False)
                            user.first_name = form.cleaned_data['first_name']
                            user.last_name = form.cleaned_data['last_name']
                            user.save()

                            user = authenticate(username=username, password=password1)
                            login(request, user)
                        return redirect("home")
                else:
                    error = "Nieprawidłowy email. Spróbuj ponownie."
        else:
            error = "Hasła nie pasują do siebie. Wprowadź pownownie."

        return render(request, "register.html", {"user_form": RegisterForm(), "error": error})


def login_user(request):
    if request.method == "GET":
        return render(request, "login_page.html", {"form": LoginForm()})

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            user_exists = CustomUser.objects.filter(username=username).exists()
            if user_exists:
                error = "Błędne hasło."
            else:
                error = f"Użytkownik {username} nie istnieje."
            return render(request, "login_page.html", {"form": LoginForm(), "error": error})


@login_required()
def logout_user(request):
    logout(request)
    return render(request, "home.html")


@login_required()
def customer_detail(request, user_id):
    # booking = Bookings.objects.get(id=user_id)
    customer = CustomUser.objects.get(id=user_id)
    return render(request, "customer_detail.html", {"customer": customer})


@login_required()
def customer_list(request):
    customers = CustomUser.objects.all()
    return render(request, "customer_list.html", {"customers": customers})


""" Booking views """


@login_required
def rent(request, boat_id):
    boat = Boat.objects.get(id=boat_id)
    return render(request, "booking_details.html", {"boat": boat})


@login_required
def booking_details(request, boat_id):
    username = request.user
    user = CustomUser.objects.get(username=username)
    boat = Boat.objects.get(id=boat_id)
    start_date_str = request.POST['start_date']
    end_date_str = request.POST['end_date']

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    total_price = int((end_date - start_date).days) * boat.daily_price
    # booking_availability = Bookings.objects.filter(boat_id=boat_id)

    if start_date < date.today() or end_date <= start_date:
        message = "Proszę podać poprawne daty."
        return render(request, "booking_confirmation.html", {"message": message})

    availability_query = Q(start_date__in=[start_date, end_date]) | Q(end_date__in=[start_date, end_date])
    available_dates = Bookings.objects.filter(Q(boat_id=boat_id) & Q(availability_query))

    if available_dates.exists():
        boat_avail = available_dates.first()
        message = f"Łódź jest niedostępna w okresie {boat_avail.start_date} - {boat_avail.end_date}."
        return render(request, 'booking_confirmation.html', {"message": message})

    try:
        booking = Bookings(
            boat_id=boat,
            customer_id=user,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price)
        booking.save()
        user.wallet += total_price
        user.save()

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return render(request, 'booking_confirmation.html', {'error_message': 'Wystąpił błąd podczas rezerwacji.'})

    # Email notification for menager
    template_text = (f"Otrzymano nową prośbę o rezerwację łodzi {booking.boat_id.name} "
                     f"w terminie {booking.start_date} - {booking.end_date}")

    email_confirmation("fpiecyk.dev@gmail.com", template_text)

    # Email notification for customer
    template_text = (f"Wysłano  prośbę o rezerwację łodzi {booking.boat_id.name} "
                     f"w terminie {booking.start_date} - {booking.end_date}.\n"
                     f"Rezerwacja zostanie potwierdzona w osobnym mailu.")

    email_confirmation(booking.customer_id.email, template_text)

    return render(request, 'booking_confirmation.html', {'booking': booking})


@login_required
def bookings_list(request):
    if request.method == "GET":
        username = request.user
        user = CustomUser.objects.get(username=username)
        if not user.is_staff:
            bookings = Bookings.objects.filter(customer_id=user).order_by("-end_date")
        else:
            bookings = Bookings.objects.all().order_by("-end_date")

        bookings_sum = bookings.aggregate(total_price_sum=models.Sum('total_price'))['total_price_sum']

        customer_ids = Bookings.objects.values_list('customer_id', flat=True).distinct()
        customers = CustomUser.objects.filter(id__in=customer_ids)

        boats_ids = Bookings.objects.values_list('boat_id', flat=True).distinct()
        boats = Boat.objects.filter(id__in=boats_ids)
        context = {"bookings_list": bookings, "customers": customers, "boats": boats, "bookings_sum": bookings_sum}
        return render(request, "bookings_list.html", context)

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        boat_id = request.POST.get("boat_id")

        if user_id and boat_id:
            bookings = Bookings.objects.filter(customer_id=user_id, boat_id=boat_id).order_by("end_date")
            bookings_sum = bookings.aggregate(total_price_sum=models.Sum('total_price'))['total_price_sum']
            return render(request, "bookings_list.html", {"bookings_list": bookings, "bookings_sum": bookings_sum})

        elif user_id:
            bookings = Bookings.objects.filter(customer_id=user_id).order_by("end_date")
            bookings_sum = bookings.aggregate(total_price_sum=models.Sum('total_price'))['total_price_sum']
            return render(request, "bookings_list.html", {"bookings_list": bookings, "bookings_sum": bookings_sum})

        elif boat_id:
            bookings = Bookings.objects.filter(boat_id=boat_id).order_by("end_date")
            bookings_sum = bookings.aggregate(total_price_sum=models.Sum('total_price'))['total_price_sum']
            return render(request, "bookings_list.html", {"bookings_list": bookings, "bookings_sum": bookings_sum})

        else:
            return redirect("bookings_list")


@login_required
def customer_booking_list(request):
    username = request.user
    user = CustomUser.objects.get(username=username)
    bookings = Bookings.objects.filter(customer_id=user).order_by("-end_date")
    bookings_sum = bookings.aggregate(total_price_sum=models.Sum('total_price'))['total_price_sum']
    context = {"bookings_list": bookings, "bookings_sum": bookings_sum}
    return render(request, "bookings_list.html", context)


@login_required
def booking_edit(request, booking_id):
    booking = Bookings.objects.get(id=booking_id)
    original_total_price = booking.total_price
    boat = booking.boat_id

    if request.method == "GET":
        return render(request, "booking_edit.html", {"booking": booking})

    if request.method == "POST":
        start_date_str = request.POST['start_date']
        end_date_str = request.POST['end_date']

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        if start_date < date.today() or end_date <= start_date:
            message = "Proszę podać poprawne daty."
            return render(request, "booking_confirmation.html", {"message": message})

        availability_query = Q(start_date__in=[start_date, end_date]) | Q(end_date__in=[start_date, end_date])
        available_dates = Bookings.objects.filter(Q(boat_id=boat) & Q(availability_query)).exclude(id=booking_id)

        if available_dates.exists():
            boat_avail = available_dates.first()
            message = f"Łódź jest niedostępna w okresie {boat_avail.start_date} - {boat_avail.end_date}."
            return render(request, 'booking_confirmation.html', {"message": message})

        # with transaction.atomic():
        booking.start_date = start_date
        booking.end_date = end_date
        booking.total_price = int((end_date - start_date).days) * boat.daily_price
        booking.save()

        new_total_price = int((end_date - start_date).days) * boat.daily_price
        user = booking.customer_id
        wallet_difference = new_total_price - original_total_price
        user.wallet += wallet_difference
        user.save()

        return redirect('bookings_list')


@login_required
def booking_cancel(request, booking_id):
    booking = Bookings.objects.get(id=booking_id)

    if booking.booking_confirm:
        message = "Nie można usunąć zatwierdzonej rezerwacji."
        return render(request, "bookings_list.html", {"message": message})

    if booking.end_date < date.today():
        message = "Wynajem został zrealizowany. Nie można usunąć rezerwacji z historii."
        return render(request, "bookings_list.html", {"message": message})

    price = booking.total_price
    user = booking.customer_id
    user.wallet -= price
    user.save()
    booking.delete()
    return redirect("bookings_list")


@login_required
def booking_status(request, booking_id):
    booking = Bookings.objects.get(id=booking_id)

    if booking.booking_confirm:
        booking.booking_confirm = False
        template_text = (f"Przepraszamy, ale z powodów niezależnych musięliśmy odwołać twoją rezerwację.\n"
                         f"Prosimy o kontakt z naszym biurem bądź wyszukanie innej łodzi z oferty.")
    else:
        booking.booking_confirm = True
        template_text = (f"Twoja rezerwacja na łódź {booking.boat_id.name} w okresie "
                         f"od {booking.start_date} do {booking.end_date} została potwierdzona.\n"
                         f"Odbiór łodzi w przystani {booking.boat_id.pier_id.name} "
                         f"pod adresem {booking.boat_id.pier_id.address}")
    booking.save()

    # Email confirmation about booking status
    email_confirmation(booking.customer_id.email, template_text)

    return redirect("bookings_list")


@login_required
def export_bookings(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Rezerwacje.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Rezerwacje"

    # Add headers
    headers = ["Łódź", "Data początkowa", "Data końcowa", "Klient", "Kwota", ]
    ws.append(headers)

    # Add data from the model
    bookings = Bookings.objects.all()
    for booking in bookings:
        ws.append([booking.boat_id.name, booking.start_date, booking.end_date,
                   booking.customer_id.first_name + " " + booking.customer_id.last_name, booking.total_price])

    # Save the workbook to the HttpResponse
    wb.save(response)
    return response
