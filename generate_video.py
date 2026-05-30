#!/usr/bin/env python3
"""
YouTube Video Üretici
MoneyPrinterTurbo üzerine kurulu kolay video üretim aracı.

Kullanım:
  python generate_video.py --konu "Yapay Zekanın Geleceği" --stil shorts
  python generate_video.py --konu "Para Kazanma Yolları" --stil belgesel --dil tr
  python generate_video.py --liste konular.txt
"""

import argparse
import json
import os
import sys
import time
import requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:8080"


# ---------- Ön tanımlı video stilleri ----------
STILLER = {
    "shorts": {
        "video_aspect": "9:16",
        "video_clip_duration": 4,
        "voice_rate": 1.1,
        "bgm_type": "random",
        "bgm_volume": 0.15,
        "subtitle_enabled": True,
        "subtitle_position": "bottom",
        "font_size": 70,
        "text_color": "#FFFFFF",
        "stroke_color": "#000000",
        "stroke_width": 2.0,
        "video_count": 1,
        "aciklama": "YouTube Shorts / TikTok dikey video (9:16)",
    },
    "uzun": {
        "video_aspect": "16:9",
        "video_clip_duration": 6,
        "voice_rate": 1.0,
        "bgm_type": "random",
        "bgm_volume": 0.1,
        "subtitle_enabled": True,
        "subtitle_position": "bottom",
        "font_size": 55,
        "text_color": "#FFFFFF",
        "stroke_color": "#000000",
        "stroke_width": 1.5,
        "video_count": 1,
        "aciklama": "YouTube uzun format yatay video (16:9)",
    },
    "belgesel": {
        "video_aspect": "16:9",
        "video_clip_duration": 8,
        "voice_rate": 0.95,
        "bgm_type": "random",
        "bgm_volume": 0.08,
        "subtitle_enabled": True,
        "subtitle_position": "bottom",
        "font_size": 50,
        "text_color": "#F0E68C",
        "stroke_color": "#000000",
        "stroke_width": 1.5,
        "video_count": 1,
        "aciklama": "Belgesel tarzı yavaş tempolu video",
    },
    "motivasyon": {
        "video_aspect": "9:16",
        "video_clip_duration": 3,
        "voice_rate": 1.15,
        "bgm_type": "random",
        "bgm_volume": 0.25,
        "subtitle_enabled": True,
        "subtitle_position": "center",
        "font_size": 75,
        "text_color": "#FFD700",
        "stroke_color": "#000000",
        "stroke_width": 2.5,
        "video_count": 1,
        "aciklama": "Motivasyon / ilham verici hızlı tempolu short",
    },
    "haber": {
        "video_aspect": "16:9",
        "video_clip_duration": 5,
        "voice_rate": 1.05,
        "bgm_type": "random",
        "bgm_volume": 0.05,
        "subtitle_enabled": True,
        "subtitle_position": "bottom",
        "font_size": 52,
        "text_color": "#FFFFFF",
        "stroke_color": "#1a1a2e",
        "stroke_width": 1.5,
        "video_count": 1,
        "aciklama": "Haber / bilgi verici profesyonel format",
    },
}


def sunucu_calis_mi() -> bool:
    try:
        r = requests.get(f"{BASE_URL}/ping", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def video_olustur(konu: str, stil: str, dil: str, ses: str, kaynak: str, adet: int) -> dict:
    stil_ayarlar = STILLER.get(stil, STILLER["shorts"]).copy()
    stil_ayarlar.pop("aciklama", None)
    stil_ayarlar["video_count"] = adet

    payload = {
        "video_subject": konu,
        "video_language": dil,
        "video_source": kaynak,
        **stil_ayarlar,
    }

    if ses:
        payload["voice_name"] = ses

    print(f"\n[*] Konu   : {konu}")
    print(f"[*] Stil   : {stil} — {STILLER.get(stil, {}).get('aciklama', '')}")
    print(f"[*] Dil    : {dil or 'otomatik'}")
    print(f"[*] Kaynak : {kaynak}")
    print(f"[*] Adet   : {adet}")
    print("[*] Görev gönderiliyor...\n")

    r = requests.post(f"{BASE_URL}/api/v1/videos", json=payload, timeout=30)
    if r.status_code != 200:
        print(f"[!] Hata: {r.status_code} — {r.text}")
        sys.exit(1)

    data = r.json()
    task_id = data.get("data", {}).get("task_id")
    if not task_id:
        print(f"[!] task_id alınamadı: {data}")
        sys.exit(1)

    print(f"[✓] Görev başlatıldı: {task_id}")
    return task_id


def gorevi_bekle(task_id: str, timeout: int = 600):
    print("[*] Video oluşturuluyor ", end="", flush=True)
    bekleme = 0
    while bekleme < timeout:
        r = requests.get(f"{BASE_URL}/api/v1/tasks/{task_id}", timeout=10)
        if r.status_code == 200:
            durum = r.json().get("data", {})
            state = durum.get("state", 0)
            if state == 1:  # tamamlandı
                print(" ✓")
                videos = durum.get("videos", [])
                return videos
            elif state == -1:  # hata
                print(" ✗")
                print(f"[!] Video üretimi başarısız: {durum.get('error', 'bilinmeyen hata')}")
                sys.exit(1)
        print(".", end="", flush=True)
        time.sleep(5)
        bekleme += 5
    print(" ZAMAN AŞIMI")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="YouTube Video Üretici",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="\nKullanılabilir stiller:\n" + "\n".join(
            f"  {k:12s} — {v['aciklama']}" for k, v in STILLER.items()
        ),
    )
    parser.add_argument("--konu", "-k", help="Video konusu / başlığı")
    parser.add_argument("--stil", "-s", default="shorts", choices=list(STILLER.keys()),
                        help="Video stili (varsayılan: shorts)")
    parser.add_argument("--dil", "-d", default="tr", help="Video dili, örn: tr, en (varsayılan: tr)")
    parser.add_argument("--ses", help="Ses adı (boş bırakılırsa otomatik seçilir)")
    parser.add_argument("--kaynak", default="pexels", choices=["pexels", "pixabay"],
                        help="Video malzeme kaynağı (varsayılan: pexels)")
    parser.add_argument("--adet", type=int, default=1, help="Üretilecek video sayısı (varsayılan: 1)")
    parser.add_argument("--liste", "-l", help="Konu listesi dosyası (her satır bir konu)")
    parser.add_argument("--stiller", action="store_true", help="Mevcut stilleri listele")
    parser.add_argument("--url", default="http://127.0.0.1:8080", help="API adresi")

    args = parser.parse_args()
    global BASE_URL
    BASE_URL = args.url.rstrip("/")

    if args.stiller:
        print("\nKullanılabilir video stilleri:\n")
        for isim, ayarlar in STILLER.items():
            print(f"  {isim:12s} — {ayarlar['aciklama']}")
            print(f"              {ayarlar['video_aspect']} | klip: {ayarlar['video_clip_duration']}s | bgm: {ayarlar['bgm_volume']}")
        print()
        sys.exit(0)

    if not sunucu_calis_mi():
        print(f"[!] API sunucusuna ({BASE_URL}) ulaşılamıyor.")
        print("[!] Sunucuyu başlatmak için:")
        print(f"      cd MoneyPrinterTurbo && python main.py")
        sys.exit(1)

    konular = []
    if args.liste:
        with open(args.liste, encoding="utf-8") as f:
            konular = [line.strip() for line in f if line.strip()]
    elif args.konu:
        konular = [args.konu]
    else:
        parser.print_help()
        sys.exit(1)

    for konu in konular:
        task_id = video_olustur(konu, args.stil, args.dil, args.ses or "", args.kaynak, args.adet)
        videolar = gorevi_bekle(task_id)
        print(f"\n[✓] Hazır! Video dosyaları:")
        for v in videolar:
            print(f"    {v}")
        print()


if __name__ == "__main__":
    main()
