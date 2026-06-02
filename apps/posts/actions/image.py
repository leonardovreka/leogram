import boto3
import uuid
from io import BytesIO
from PIL import Image
from django.conf import settings
from botocore.client import Config


def validate_and_upload_image(image_file) -> str:

    allowed_types = ['image/jpeg', 'image/png', 'image/webp']
    if image_file.content_type not in allowed_types:
        raise ValueError('Invalid image type. Only JPEG, PNG and WebP are allowed')

    if image_file.size > 5 * 1024 * 1024:
        raise ValueError('Image size must be under 5MB')

    try:
        img = Image.open(image_file)
        img.verify()
    except Exception:
        raise ValueError('Invalid image file')

    image_file.seek(0)
    img = Image.open(image_file)

    if img.width > 1080:
        ratio = 1080 / img.width
        new_height = int(img.height * ratio)
        img = img.resize((1080, new_height), Image.LANCZOS)

    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=85, optimize=True)
    buffer.seek(0)

    s3 = boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4'),
    )

    filename = f"posts/{uuid.uuid4()}.jpg"

    s3.upload_fileobj(
        buffer,
        settings.AWS_STORAGE_BUCKET_NAME,
        filename,
        ExtraArgs={'ContentType': 'image/jpeg'}
    )

    image_url = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{filename}"
    return image_url