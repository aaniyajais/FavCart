from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from datetime import datetime
from django.db import connection
from django.contrib.auth.hashers import make_password, check_password


# Home page
def index(request):
    user = request.session.get('userid')
    ct = ""

    if user:
        ct = mcart.objects.filter(userid=user).count()

    x = category.objects.all().order_by('-id')[0:6]
    pdata = myproduct.objects.all().order_by('-id')[0:7]

    mydict = {
        "data": x,
        "prodata": pdata,
        "cart": ct
    }

    return render(request, 'user/index.html', context=mydict)


# About page
def about(request):
    user = request.session.get('userid')
    ct = ""

    if user:
        ct = mcart.objects.filter(userid=user).count()

    return render(request, 'user/aboutus.html', {"cart": ct})


# Product page
def product(request):
    user = request.session.get('userid')
    ct = ""

    if user:
        ct = mcart.objects.filter(userid=user).count()

    return render(request, 'user/product.html', {"cart": ct})


# Orders
def myorder(request):
    user = request.session.get('userid')
    oid = request.GET.get('oid')
    mydict = {}

    if user:

        # Cancel only the logged-in user's own order
        if oid is not None:
            morder.objects.filter(
                id=oid,
                userid=user
            ).delete()

            return HttpResponse(
                "<script>"
                "alert('your order has been cancelled..');"
                "location.href='/user/myorder/'"
                "</script>"
            )

        # Pending orders
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT p.*, o.*
            FROM user_myproduct p, user_morder o
            WHERE p.id = o.pid
              AND o.userid = %s
              AND o.remarks = %s
            """,
            [user, "pending"]
        )
        pdata = cursor.fetchall()

        # Delivered orders
        cursor.execute(
            """
            SELECT p.*, o.*
            FROM user_myproduct p, user_morder o
            WHERE p.id = o.pid
              AND o.userid = %s
              AND o.remarks = %s
            """,
            [user, "delivered"]
        )
        ddata = cursor.fetchall()

        mydict = {
            "pdata": pdata,
            "ddata": ddata
        }

    return render(request, 'user/myorder.html', mydict)


# Enquiry / Contact
def enquiry(request):
    status = False

    if request.method == "POST":
        a = request.POST.get("name")
        b = request.POST.get("email")
        c = request.POST.get("mob")
        d = request.POST.get("msg")

        contactus(
            Name=a,
            Mobile=c,
            Email=b,
            Message=d
        ).save()

        status = True

    msg = {"m": status}

    return render(request, 'user/enquiry.html', msg)


# Signup
def signup(request):
    if request.method == "POST":
        Name = request.POST.get("name")
        Email = request.POST.get("email")
        Mobile = request.POST.get("mob")
        Passwd = request.POST.get("passwd")
        Address = request.POST.get("address")
        Picture = request.FILES.get("pic")

        x = register.objects.filter(Email=Email).count()

        if x == 0:
            register(
                Name=Name,
                Email=Email,
                Mobile=Mobile,
                Ppic=Picture,
                Passwd=make_password(Passwd),
                Address=Address
            ).save()

            return HttpResponse(
                "<script>"
                "alert('you are registered successfully');"
                "location.href='/user/signup/'"
                "</script>"
            )

        else:
            return HttpResponse(
                "<script>"
                "alert('your email id is already registered');"
                "location.href='/user/signup/'"
                "</script>"
            )

    return render(request, 'user/signup.html')


# Profile
def myprofile(request):
    user = request.session.get('userid')

    if user:
        profile = register.objects.filter(Email=user).first()

        if request.method == "POST" and profile:
            Name = request.POST.get("name")
            Mobile = request.POST.get("mob")
            Passwd = request.POST.get("passwd")
            Address = request.POST.get("address")
            Picture = request.FILES.get("pic")

            profile.Name = Name
            profile.Mobile = Mobile
            profile.Address = Address

            # Only update password when the user entered a new one
            if Passwd:
                profile.Passwd = make_password(Passwd)

            # Only replace profile picture when a new picture is uploaded
            if Picture:
                profile.Ppic = Picture

            profile.save()

            return HttpResponse(
                "<script>"
                "alert('your profile is updated successfully..');"
                "location.href='/user/myprofile/'"
                "</script>"
            )

        x = register.objects.filter(Email=user)
    else:
        x = ""

    d = {"mdata": x}

    return render(request, 'user/myprofile.html', d)


# Sign in
def signin(request):
    if request.method == "POST":
        Email = request.POST.get('email')
        Password = request.POST.get('passwd')

        user = register.objects.filter(Email=Email).first()

        if user and check_password(Password, user.Passwd):
            request.session["userid"] = Email
            request.session["userpic"] = str(user.Ppic)

            return HttpResponse(
                "<script>"
                "alert('you are login...');"
                "location.href='/user/signin/'"
                "</script>"
            )

        return HttpResponse(
            "<script>"
            "alert('your user id or password is incorrect...');"
            "location.href='/user/signin/'"
            "</script>"
        )

    return render(request, 'user/signin.html')


# View product
def viewproduct(request):
    a = request.GET.get('abc')

    x = myproduct.objects.filter(id=a)

    return render(request, 'user/viewproduct.html', {"pdata": x})


# Men's products
def mens(request):
    cid = request.GET.get('msg')

    cat = category.objects.all().order_by('-id')

    d = myproduct.objects.filter(mcategory=8)

    if cid is not None:
        d = myproduct.objects.filter(
            mcategory=8,
            pcategory=cid
        )

    mydict = {
        "cats": cat,
        "data": d,
        "a": cid
    }

    return render(request, 'user/mens.html', mydict)


# Women's products
def womens(request):
    cid = request.GET.get('msg')

    cat = category.objects.all().order_by('-id')

    d = myproduct.objects.filter(mcategory=7)

    if cid is not None:
        d = myproduct.objects.filter(
            mcategory=7,
            pcategory=cid
        )

    mydict = {
        "cats": cat,
        "data": d,
        "a": cid
    }

    return render(request, 'user/womens.html', mydict)


# Kids' products
def kids(request):
    cid = request.GET.get('msg')

    cat = category.objects.all().order_by('-id')

    d = myproduct.objects.filter(mcategory=10)

    if cid is not None:
        d = myproduct.objects.filter(
            mcategory=10,
            pcategory=cid
        )

    mydict = {
        "cats": cat,
        "data": d,
        "a": cid
    }

    return render(request, 'user/kids.html', mydict)


# Sign out
def signout(request):
    if request.session.get('userid'):
        del request.session["userid"]

    return HttpResponse(
        "<script>"
        "alert('you are logged out...');"
        "location.href='/user/signin/'"
        "</script>"
    )


# Place order from product page
def myordr(request):
    user = request.session.get('userid')
    pid = request.GET.get('msg')

    if user:
        if pid is not None:
            morder(
                userid=user,
                pid=pid,
                remarks="pending",
                odate=datetime.now().date(),
                status=True
            ).save()

            return HttpResponse(
                "<script>"
                "alert('your order id confirmd');"
                "location.href='/user/viewproduct/'"
                "</script>"
            )

    else:
        return HttpResponse(
            "<script>"
            "alert('you have to log in first....');"
            "location.href='/user/signin/'"
            "</script>"
        )

    return render(request, 'user/myordr.html')


# Add item to cart
def mycart(request):
    user = request.session.get('userid')
    p = request.GET.get('pid')

    if user:
        if p is not None:
            mcart(
                userid=user,
                pid=p,
                cdate=datetime.now().date(),
                status=True
            ).save()

            return HttpResponse(
                "<script>"
                "alert('your item is added to cart....');"
                "location.href='/user/index/'"
                "</script>"
            )

    else:
        return HttpResponse(
            "<script>"
            "alert('You have to login first.....');"
            "location.href='/user/signin/'"
            "</script>"
        )

    return render(request, 'user/mcart.html')


# Show cart
def showcart(request):
    user = request.session.get('userid')

    md = {}

    a = request.GET.get('msg')
    cid = request.GET.get('cid')
    pid = request.GET.get('pid')

    if user:

        # Remove cart item
        if a is not None:
            mcart.objects.filter(
                id=a,
                userid=user
            ).delete()

            return HttpResponse(
                "<script>"
                "alert('Your item are deleted....');"
                "location.href='/user/index/'"
                "</script>"
            )

        # Place order from cart
        elif pid is not None:
            mcart.objects.filter(
                id=cid,
                userid=user
            ).delete()

            morder(
                userid=user,
                pid=pid,
                remarks="Pending",
                status=True,
                odate=datetime.now().date()
            ).save()

            return HttpResponse(
                "<script>"
                "alert('Your order has been placed successfully...');"
                "location.href='/user/myorder/'"
                "</script>"
            )

        # Cart items
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT p.*, c.*
            FROM user_myproduct p, user_mcart c
            WHERE p.id = c.pid
              AND c.userid = %s
            """,
            [user]
        )

        cdata = cursor.fetchall()

        md = {
            "cdata": cdata
        }

    return render(request, 'user/showcart.html', md)


# Products by category
def cpdetail(request):
    c = request.GET.get('cid')

    p = myproduct.objects.filter(pcategory=c)

    return render(request, 'user/cpdetail.html', {"pdata": p})


# Terms page
def terms(request):
    user = request.session.get('userid')
    ct = ""

    if user:
        ct = mcart.objects.filter(userid=user).count()

    return render(request, 'user/terms.html', {"cart": ct})