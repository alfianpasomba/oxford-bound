from django.db import models
from django.utils import timezone

class Tense(models.Model):
    """
    Model ini menyimpan kamus tenses (contoh: Simple Present, Present Perfect).
    Akan digunakan untuk mengisi data di Tab 2, 3, dan 4 pada Daily Challenge.
    """
    name = models.CharField(max_length=50, help_text="Nama Tenses, misal: Present Perfect Tense")
    formula = models.TextField(help_text="Rumus tenses untuk ditampilkan di Tab 2")
    # Gunakan ImageField untuk menyimpan gambar grafik waktu (Tab 3)
    timeline_image = models.ImageField(upload_to='tenses_timelines/', null=True, blank=True)
    
    # Untuk Tab 4: Contoh kalimat Positive, Negative, Interrogative/Imperative
    positive_example = models.CharField(max_length=255)
    negative_example = models.CharField(max_length=255)
    other_example = models.CharField(max_length=255, help_text="Contoh kalimat interogatif atau imperatif")

    def __str__(self):
        return self.name


class Vocabulary(models.Model):
    """
    Model utama untuk mencatat kosa kata baru.
    """
    word = models.CharField(max_length=100, unique=True, help_text="Kosa kata dalam Bahasa Inggris")
    meaning = models.CharField(max_length=255, help_text="Arti dalam Bahasa Indonesia")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Field ini berguna untuk mengacak kata di Daily Challenge. 
    # Kata dengan tanggal 'last_practiced' paling lama bisa diprioritaskan muncul.
    last_practiced = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Vocabularies"

    def __str__(self):
        return self.word


class ExampleSentence(models.Model):
    """
    Model kalimat. Berelasi One-to-Many dengan Vocabulary.
    Semua kalimat (kalimat pertama, kalimat tambahan, kalimat dari challenge) disimpan di sini.
    """
    SOURCE_CHOICES = (
        ('first_heard', 'First Time Heard'),
        ('manual', 'Manual Addition'),
        ('challenge', 'Daily Challenge'),
    )

    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='examples')
    sentence = models.TextField(help_text="Isi kalimat contoh")
    
    # Menandai dari mana asal kalimat ini
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='manual')
    
    # Jika kalimat ini berasal dari Daily Challenge, kita catat tenses-nya.
    # Jika kalimat berasal dari first heard/manual, ini bisa dibiarkan kosong (null).
    tense = models.ForeignKey(Tense, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Mencatat tanggal pembuatan kalimat seperti yang Anda minta
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.vocabulary.word} - {self.sentence[:30]}..."
