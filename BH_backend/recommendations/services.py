from collections import defaultdict

from django.db import transaction

from scrapy_app.models import Products
from users.models import UserInteractions, UserPreferences

from .models import UserRecommendation


def _split_csv_values(raw_value):
    if not raw_value:
        return set()
    return {part.strip().lower() for part in raw_value.split(",") if part.strip()}


def _extract_numeric_rating(rating_text):
    if not rating_text:
        return 0
    digit_chars = [char for char in str(rating_text) if char.isdigit()]
    if not digit_chars:
        return 0
    return int(digit_chars[0])


def generate_rule_based_recommendations(user, limit=10):
    preferences = UserPreferences.objects.filter(user=user).first()
    preferred_brands = _split_csv_values(
        preferences.preferred_brands if preferences else ""
    )
    preferred_types = _split_csv_values(
        preferences.preferred_product_types if preferences else ""
    )

    interactions = UserInteractions.objects.filter(user=user).select_related("product")
    favorite_product_ids = set(
        interactions.filter(interaction_type="favorite").values_list("product_id", flat=True)
    )
    interacted_type_names = {
        interaction.product.type.strip().lower()
        for interaction in interactions
        if interaction.product and interaction.product.type
    }

    scored_products = []
    for product in Products.objects.select_related("brand").all():
        if not product.id:
            continue
        if product.id in favorite_product_ids:
            continue

        score = 0
        reasons = []

        brand_name = (
            product.brand.brand.strip().lower()
            if product.brand and product.brand.brand
            else ""
        )
        product_type = product.type.strip().lower() if product.type else ""
        rating_value = _extract_numeric_rating(product.rating)

        if brand_name and brand_name in preferred_brands:
            score += 3
            reasons.append("preferred brand")

        if product_type and product_type in preferred_types:
            score += 3
            reasons.append("preferred product type")

        if product_type and product_type in interacted_type_names:
            score += 2
            reasons.append("similar to your previous interactions")

        if rating_value >= 4:
            score += 1
            reasons.append("high product rating")

        if score > 0:
            scored_products.append((score, product, reasons))

    scored_products.sort(key=lambda item: (-item[0], item[1].id))
    selected = scored_products[:limit]

    with transaction.atomic():
        UserRecommendation.objects.filter(user=user).delete()
        created = []
        for score, product, reasons in selected:
            reason_text = ", ".join(dict.fromkeys(reasons))
            recommendation = UserRecommendation.objects.create(
                user=user,
                product=product,
                reason=f"Rule score {score}: {reason_text}",
            )
            created.append(recommendation)

    return created
