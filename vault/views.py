from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from .models import Vocabulary, Tense, ExampleSentence

def dashboard(request):
    """
    Menampilkan halaman utama: Form input kosa kata & Daily Challenge.
    """
    # --- 1. Logika untuk "Coba Kata Lain" ---
    # Jika Anda menekan tombol "Try Another Word", kita akan mengecualikan kata saat ini
    exclude_word_id = request.GET.get('exclude_word')
    
    vocab_query = Vocabulary.objects.all()
    if exclude_word_id:
        vocab_query = vocab_query.exclude(id=exclude_word_id)
        
    # --- 2. Mengambil 1 Kata Random ---
    # Prioritaskan kata yang belum pernah dilatih (last_practiced = None) 
    # atau yang paling lama tidak dilatih, lalu diacak (?)
    random_word = vocab_query.order_by('last_practiced', '?').first()

    # --- 3. Mengambil 3 Tenses secara Acak ---
    # (Pastikan Anda sudah mengisi data tenses di Django Admin minimal 3 tenses)
    random_tenses = Tense.objects.order_by('?')[:3]

    context = {
        'random_word': random_word,
        'random_tenses': random_tenses,
    }
    return render(request, 'vault/vault.html', context)


def add_vocabulary(request):
    """
    Menangani form penambahan kosa kata baru.
    """
    if request.method == 'POST':
        word = request.POST.get('word', '').strip().lower() # Diseragamkan jadi huruf kecil
        meaning = request.POST.get('meaning', '').strip()
        first_sentence = request.POST.get('first_sentence', '').strip()

        if word and meaning:
            # get_or_create mencegah error jika Anda tidak sengaja menginput kata yang sama
            vocab, created = Vocabulary.objects.get_or_create(
                word=word,
                defaults={'meaning': meaning}
            )
            
            # Jika user mengisi kalimat pertama, simpan ke database
            if first_sentence:
                ExampleSentence.objects.create(
                    vocabulary=vocab,
                    sentence=first_sentence,
                    source='first_heard'
                )
            
            # Pesan sukses (bisa ditampilkan sebagai alert di HTML nanti)
            if created:
                messages.success(request, f"Splendid! '{word}' berhasil ditambahkan ke catatan Anda.")
            else:
                messages.warning(request, f"Kata '{word}' sudah ada, namun contoh kalimat baru tetap ditambahkan.")
                
        return redirect('dashboard')
    
    return redirect('dashboard')


def submit_challenge(request):
    """
    Menangani form Daily Challenge saat tombol Submit ditekan.
    """
    if request.method == 'POST':
        vocab_id = request.POST.get('vocab_id')
        vocab = get_object_or_404(Vocabulary, id=vocab_id)
        
        # Karena kita memiliki 3 form field tenses, form di HTML akan 
        # mengirim array/list dari `tense_id` dan `sentence`
        tense_ids = request.POST.getlist('tense_id')
        sentences = request.POST.getlist('sentence')
        
        # Pasangkan setiap tense_id dengan kalimat yang ditulis
        for t_id, sentence_text in zip(tense_ids, sentences):
            if sentence_text.strip(): # Hanya simpan jika user benar-benar mengetik kalimat
                tense_obj = get_object_or_404(Tense, id=t_id)
                ExampleSentence.objects.create(
                    vocabulary=vocab,
                    sentence=sentence_text.strip(),
                    source='challenge',
                    tense=tense_obj,
                    created_at=timezone.now().date()
                )
        
        # Tandai bahwa kata ini baru saja dilatih hari ini
        vocab.last_practiced = timezone.now().date()
        vocab.save()
        
        messages.success(request, "Brilliant! Anda telah menyelesaikan ujian hari ini.")
        return redirect('dashboard')
        
    return redirect('dashboard')