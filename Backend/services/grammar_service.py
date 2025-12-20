# services/grammar_service.py
import re
from functools import lru_cache

# Optional: jika ada modul kbbi, gunakan. Jika tidak — lewati cek KBBI.
try:
    from kbbi import KBBI
    _HAS_KBBI = True
except Exception:
    _HAS_KBBI = False


@lru_cache(maxsize=10000)
def cek_kbbi(kata: str) -> bool:
    """
    Cek KBBI jika tersedia. Untuk kata pendek (<=2) return True agar tidak memblokir.
    """
    kata = kata.strip()
    if not kata or len(kata) <= 2:
        return True
    if not _HAS_KBBI:
        # Jika KBBI tidak tersedia, kembalikan False untuk kata yang tampak digabung 'diX'?
        return False
    try:
        KBBI(kata)
        return True
    except Exception:
        return False


# Simplified dictionaries (bisa kamu perluas kembali)
DI_LOKASI = {
    "rumah", "kantor", "sekolah", "kampus", "pasar", "kota", "desa", "kabupaten",
    "provinsi", "negara", "daerah", "jalan", "kamar", "dapur", "teras", "taman",
    "toilet", "wc", "garasi", "hotel", "restoran", "kafe", "stasiun",
    "bandara", "terminal", "perpustakaan", "lapangan", "rumah sakit", "bank",
}

KATA_KERJA_UMUM = {
    "ambil", "taruh", "angkat", "makan", "minum", "bawa", "buat", "beri", "jual", "beli",
    "tulis", "hapus", "cetak", "masak", "pakai", "bakar", "dorong", "tarik", "tutup",
    "buka", "cuci", "tolong", "lari", "jalan", "duduk", "berdiri", "naik", "turun",
    "klik", "ketik", "upload", "download", "kirim", "simpan", "cari", "parkir",
}


def _find_sentence_starts(text: str):
    """
    Menghasilkan match untuk kata pertama tiap kalimat (pos dan kata).
    Kalimat dianggap dimulai di awal teks atau setelah .!? diikuti spasi.
    """
    pattern = re.compile(r'(^|[\.!?]\s+)([^\s])', flags=re.MULTILINE | re.UNICODE)
    for m in pattern.finditer(text):
        yield m.start(2), m.group(2)


def check_grammar(text: str):
    """
    Mengembalikan dict:
    {
      "corrected_text": "...",
      "errors": [
        {"start": int, "end": int, "original": "...", "suggestion":"...", "message":"..."},
        ...
      ]
    }
    Deteksi:
      - Huruf awal kalimat harus kapital
      - 'di' yang salah pisah/gabung (sederhana)
      - spasi ganda
      - spasi sebelum tanda baca
      - kata + 'nya' yang seharusnya digabung (cek KBBI jika tersedia)
    """
    if not text:
        return {"corrected_text": "", "errors": []}

    errors = []

    # 1) Huruf awal kalimat kecil -> sarankan kapitalisasi kata awal
    for pos, char in _find_sentence_starts(text):
        if char.isalpha() and char.islower():
            # ambil kata lengkap dari posisi pos
            m_word = re.match(r'[^\s\.,;:!?()"\']+', text[pos:])
            if m_word:
                word = m_word.group(0)
                start = pos
                end = pos + len(word)
                suggestion = word[0].upper() + word[1:] if len(word) > 0 else word.upper()
                errors.append({
                    "start": start, "end": end,
                    "original": text[start:end],
                    "suggestion": suggestion,
                    "message": "Huruf pertama kalimat harus kapital"
                })

    # 2) Spasi sebelum tanda baca -> hapus spasi
    for m in re.finditer(r'\s+([,.:;!?])', text):
        start, end = m.start(0), m.end(0)
        # suggestion: punctuation saja (tanpa spasi)
        suggestion = m.group(1)
        errors.append({
            "start": start, "end": end,
            "original": text[start:end],
            "suggestion": suggestion,
            "message": "Hapus spasi sebelum tanda baca"
        })

    # 3) Spasi ganda -> ganti jadi satu spasi
    for m in re.finditer(r' {2,}', text):
        start, end = m.start(), m.end()
        suggestion = " "
        errors.append({
            "start": start, "end": end,
            "original": text[start:end],
            "suggestion": suggestion,
            "message": "Spasi ganda — gunakan satu spasi"
        })

    # 4) 'di' salah pisah / harus digabung
    for m in re.finditer(r'\bdi\s+([^\s,\.!?;:()"\']+)', text, flags=re.IGNORECASE):
        kata = m.group(1)
        start, end = m.start(0), m.end(0)
        kata_lower = kata.lower()
        
        # jika kata kerja umum -> gabung
        if kata_lower in KATA_KERJA_UMUM:
            suggestion = "di" + kata
            errors.append({
                "start": start, "end": end,
                "original": text[start:end],
                "suggestion": suggestion,
                "message": f"Gabungkan 'di' dengan kata kerja (bentuk baku: 'di{kata_lower}')"
            })
        else:
            # jika KBBI ada dan 'di'+kata adalah entry baku, sarankan gabung
            if cek_kbbi("di" + kata_lower):
                suggestion = "di" + kata
                errors.append({
                    "start": start, "end": end,
                    "original": text[start:end],
                    "suggestion": suggestion,
                    "message": "Kemungkinan kata baku 'di'+kata seharusnya digabung"
                })

    # 5) 'masak nya' -> 'masaknya'
    for m in re.finditer(r'\b([^\s,\.!?;:()"\']+)\s+nya\b', text, flags=re.IGNORECASE):
        dasar = m.group(1)
        gab = (dasar + "nya").lower()
        if cek_kbbi(gab):
            start, end = m.start(0), m.end(0)
            suggestion = dasar + "nya"
            errors.append({
                "start": start, "end": end,
                "original": text[start:end],
                "suggestion": suggestion,
                "message": f"Gabungkan kata dan 'nya' menjadi '{suggestion}'"
            })

    # Deduplicate errors
    seen = set()
    unique_errors = []
    for e in errors:
        key = (e["start"], e["end"], e["suggestion"])
        if key not in seen:
            seen.add(key)
            unique_errors.append(e)

    # Sort by start position
    unique_errors.sort(key=lambda x: x["start"])

    # Build corrected_text
    corrected = text
    edits = [(e["start"], e["end"], e["suggestion"]) for e in unique_errors]
    edits.sort(key=lambda t: t[0], reverse=True)

    for s, e, sug in edits:
        corrected = corrected[:s] + sug + corrected[e:]

    return {
        "corrected_text": corrected,
        "errors": unique_errors
    }