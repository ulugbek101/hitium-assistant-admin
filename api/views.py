from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import get_user_model

from rest_framework.views import csrf_exempt

User = get_user_model()

from django.db import transaction
from .models import User, Specialization


@transaction.atomic
def register_user_in_db(data, files):
    phone_number = data.get("phone_number")
    telegram_id = data.get("telegram_id")

    # 1. Resolve specialization
    specialization = None
    specialization_name = data.get("specialization")

    if specialization_name:
        specialization, _ = Specialization.objects.get_or_create(
            name=specialization_name
        )

    # 2. Find user by unique fields
    user = (
        User.objects
        .filter(phone_number=phone_number)
        .first()
        or
        User.objects.filter(telegram_id=telegram_id).first()
    )

    # 3. Create user if not exists
    if not user:
        user = User.objects.create(
            telegram_id=telegram_id,
            phone_number=phone_number,
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            middle_name=data.get("middle_name"),
            born_year=datetime.strptime(data.get("born_year"), "%Y-%m-%d").date(),
            type_of_document=data.get("type_of_document"),
            card_number=data.get("card_number"),
            card_holder_name=data.get("card_holder_name"),
            tranzit_number=data.get("tranzit_number"),
            bank_name=data.get("bank_name"),
            specialization=specialization,
            passport_photo=files.get("passport_photo"),
            id_card_photo1=files.get("id_card_photo1"),
            id_card_photo2=files.get("id_card_photo2"),
        )
        return user, True

    # 4. Update existing user (only provided fields)
    user.telegram_id = telegram_id or user.telegram_id
    user.first_name = data.get("first_name") or user.first_name
    user.last_name = data.get("last_name") or user.last_name
    user.middle_name = data.get("middle_name") or user.middle_name
    user.type_of_document = data.get("type_of_document") or user.type_of_document
    user.card_number = data.get("card_number") or user.card_number
    user.card_holder_name = data.get("card_holder_name") or user.card_holder_name
    user.tranzit_number = data.get("tranzit_number") or user.tranzit_number
    user.bank_name = data.get("bank_name") or user.bank_name
    user.born_year = datetime.strptime(data.get("born_year"), "%Y-%m-%d").date() or user.born_year
    user.specialization = specialization or user.specialization

    # 5. Update files only if sent
    if files.get("passport_photo"):
        user.passport_photo = files["passport_photo"]

    if files.get("id_card_photo1"):
        user.id_card_photo1 = files["id_card_photo1"]

    if files.get("id_card_photo2"):
        user.id_card_photo2 = files["id_card_photo2"]

    user.save()

    return user, False


@csrf_exempt
def register_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    # Text data
    user_data = request.POST.dict()

    # Files
    user_files = request.FILES

    register_user_in_db(user_data, user_files)

    return JsonResponse({"status": "ok"})
