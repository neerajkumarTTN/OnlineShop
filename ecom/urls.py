from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("",views.StartingPageView.as_view(),name="starting-page"),

    path("register/",views.UserSignUpView.as_view(),name="register-page"),
    path('login/',views.UserLoginView.as_view(), name="login"),
    path("logout/",views.Logout.as_view(),name="logout"),

   
    path("add-to-cart",views.AddToCart.as_view(),name="add-cart-page"),
    path("cart/",views.CartItemView.as_view(),name="cart-page"),
    path("pluscart/",views.PlusCartItem.as_view()),
    path("minuscart/",views.MinusCartItem.as_view()),
    path("removecart/",views.DeleteCartItem.as_view()),


    path("checkout/",views.CheckoutView.as_view(),name="checkout-page"),
    path("placed_order/",views.PlacedOrderView.as_view(),name="placed-order"),
    
    path("search",views.SearchView.as_view(),name="search-result"),
    path("filter/<slug:data>",views.FilterView.as_view(),name="filterdata"),
    path("profile/",views.ProfileView.as_view(),name="user-profile"),
    path("item-detail/<slug:slug>",views.SignleItemView.as_view(),name="item-detail-page"),

    path("reset_password/",
        auth_views.PasswordResetView.as_view(),
        name="reset_password"),
    path("reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done"),
    path("reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm"),
    path("reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete"),
]



