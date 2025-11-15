from django.db import models
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.base import ContentFile

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('PRANZO', 'Pranzo'),
        ('CARBURANTE', 'Carburante'),
        ('TRASPORTO', 'TRASPORTO'),
        ('VARIE', 'Varie'),
    ]

    category = models.CharField("Tipologia", max_length=50, choices=CATEGORY_CHOICES)
    city = models.CharField("Comune", max_length=100)
    province = models.CharField("Provincia", max_length=2)
    amount = models.DecimalField("Totale spesa", max_digits=10, decimal_places=2)
    date = models.DateField("Data spesa", auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.category} - {self.amount}€"


class ReceiptImage(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='receipts')
    original_image = models.ImageField("Immagine originale", upload_to='receipts/original/')
    cleaned_image = models.ImageField("Immagine pulita", upload_to='receipts/cleaned/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scontrino {self.id} per spesa {self.expense_id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # salva prima l'originale

        if self.original_image and not self.cleaned_image:
            try:
                img = Image.open(self.original_image.path)

                # Converti in bianco e nero
                img = img.convert("L")

                # Migliora contrasto automaticamente
                img = ImageOps.autocontrast(img)

                # Ridimensiona per stare bene su A4 (larghezza max ~1000 px)
                max_width = 1000
                if img.width > max_width:
                    ratio = max_width / float(img.width)
                    new_height = int(float(img.height) * ratio)
                    img = img.resize((max_width, new_height), Image.LANCZOS)

                # Salva in memoria
                buffer = BytesIO()
                img.save(buffer, format="JPEG", quality=85)
                file_name = f"cleaned_{self.pk}.jpg"
                self.cleaned_image.save(file_name, ContentFile(buffer.getvalue()), save=False)

                super().save(update_fields=['cleaned_image'])
            except Exception:
                # in caso di errore, non bloccare il salvataggio
                pass
