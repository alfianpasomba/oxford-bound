from django.contrib import admin
from .models import Tense, Vocabulary, ExampleSentence

# ==========================================
# 1. Tense Admin
# ==========================================
@admin.register(Tense)
class TenseAdmin(admin.ModelAdmin):
    # Kolom yang akan ditampilkan di halaman list (daftar) Tense
    list_display = ('name', 'formula_preview')
    search_fields = ('name',)

    # Memotong text rumus jika terlalu panjang di tampilan tabel
    def formula_preview(self, obj):
        return obj.formula[:50] + '...' if len(obj.formula) > 50 else obj.formula
    formula_preview.short_description = 'Formula'


# ==========================================
# 2. Example Sentence Inline
# ==========================================
# TabularInline memungkinkan kita menampilkan form ExampleSentence 
# di dalam form halaman detail Vocabulary.
class ExampleSentenceInline(admin.TabularInline):
    model = ExampleSentence
    extra = 1  # Jumlah form kosong tambahan yang ditampilkan
    fields = ('sentence', 'source', 'tense', 'created_at')


# ==========================================
# 3. Vocabulary Admin
# ==========================================
@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    # Kolom yang tampil di daftar kosa kata
    list_display = ('word', 'meaning', 'last_practiced', 'created_at')
    
    # Menambahkan fitur pencarian berdasarkan kata dan arti
    search_fields = ('word', 'meaning')
    
    # Menambahkan filter di sidebar kanan untuk menyortir data
    list_filter = ('last_practiced', 'created_at')
    
    # Memasukkan inline agar contoh kalimat tampil di dalam halaman edit Vocabulary
    inlines = [ExampleSentenceInline]


# ==========================================
# 4. Example Sentence Admin (Standalone)
# ==========================================
@admin.register(ExampleSentence)
class ExampleSentenceAdmin(admin.ModelAdmin):
    # Menampilkan tabel daftar semua kalimat dari semua kata
    list_display = ('vocabulary', 'sentence_preview', 'source', 'tense', 'created_at')
    
    # Filter sidebar yang sangat berguna untuk melihat kalimat berdasarkan Tenses atau Sumber
    list_filter = ('source', 'tense', 'created_at')
    
    # Pencarian berelasi: bisa mencari teks kalimatnya, atau kata dari model Vocabulary
    search_fields = ('sentence', 'vocabulary__word')

    def sentence_preview(self, obj):
        return obj.sentence[:50] + '...' if len(obj.sentence) > 50 else obj.sentence
    sentence_preview.short_description = 'Sentence'