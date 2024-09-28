import stripe
from django.conf import settings


def create_session_stripe(price_id):
    stripe.api_key = settings.STRIPE_API_KEY
    response = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return response
