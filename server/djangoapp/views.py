"""this is the views.py file for the djangoapp app"""""
import logging
import json
import random
import pdb
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from . import restapis
from .models import CarModel, CarMake

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    """about page"""
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    """contact page"""
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    """the login page"""
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context["message"] = "Invalid username or password."
    else:
        return render(request, "djangoapp/index.html", context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    """the logout page"""
    logout(request)
    return redirect("djangoapp:index")


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    """the registration page"""
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/registration.html", context)
    elif request.method == "POST":
        # Check if user exists
        username = request.POST["username"]
        password = request.POST["psw"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except ValueError:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context["message"] = "User already exists."
            return render(
                request, "djangoapp/registration.html", context
            )


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    """this get_dealerships method"""
    context = {}
    if request.method == "GET":
        url = "http://127.0.0.1:3000/dealerships/get"
        # Get dealers from the URL
        dealerships = restapis.get_dealers_from_cf(url, api_key='aa1cPksgn9BNNMDnmfXSNi3Zw1uVVGBW96LwiOhIhS9p')
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Add dealer_names to the context dictionary
        context['dealerships'] = dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    """this get_dealer_details method"""
    context = {}
    if request.method == "GET":
        url = f"http://127.0.0.1:5000/api/get_reviews?id={dealer_id}"
        # Get dealers from the URL using the id
        api_key = 'aa1cPksgn9BNNMDnmfXSNi3Zw1uVVGBW96LwiOhIhS9p'
        reviews = restapis.get_dealer_by_id_from_cf(url, dealerId=dealer_id, api_key=api_key)
        # Add dealer's reviews to the context dictionary 
        context['reviews'] = reviews
        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    """this add_review method"""
    url = "http://127.0.0.1:3000/dealerships/get"
    context = {}
    review = {}
    json_payload = {}
    user = request.user
    carmodel = CarModel.objects.filter(dealer_id=dealer_id).values()
    carmake = CarMake.objects.all().order_by('id').values()
    dealer_name = restapis.get_dealers_from_cf(url, api_key='aa1cPksgn9BNNMDnmfXSNi3Zw1uVVGBW96LwiOhIhS9p')

    if user.is_authenticated:       
        if request.method == "GET":
            context = {
                "dealer_id": dealer_id,
                "carmodel" : carmodel,
                "carmake" : carmake,
                "dealer_name" : dealer_name,
            }
            return render(request, "djangoapp/add_review.html", context)

        elif request.method == "POST":
            url = "http://127.0.0.1:5000/api/post_review"
            review["time"] = datetime.utcnow().isoformat()
            review["id"] = random.randint(1, 1000)
            review["name"] = user.username
            review["dealership"] = dealer_id
            review["review"] = request.POST["content"]
            # review["purchase"] = bool(request.POST.get("purchasecheck"))
            raw_purchase = request.POST.get("purchasecheck")
            if raw_purchase:
                review["purchase"] = raw_purchase.capitalize() == "True"
            else:
                review["purchase"] = False
            review["purchase_date"] = request.POST["purchasedate"]
            review["car_make"] = request.POST.get("carmake")
            review["car_model"] = request.POST.get("carmodel")
            review["car_year"] = int(request.POST.get("caryear"))
            json_payload["review"] = review
            correct_json = json_payload["review"]
            json_string = json.dumps(correct_json)
            pdb.set_trace()
            print(json_string)
            restapis.post_request(url, json_string, dealerId=dealer_id)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    else:
        message = "Sign up to post a review"
        return HttpResponse(message)
 