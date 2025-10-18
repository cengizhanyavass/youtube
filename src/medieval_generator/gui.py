"""Desktop GUI wrapper for the medieval content generator."""

from __future__ import annotations

import json
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Any, Dict

from .cli import generate_payload


class GeneratorApp(tk.Tk):
    """Simple Tkinter application for generating content with one click."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Medieval Content Generator")
        self.geometry("960x720")

        self._last_payload: Dict[str, Any] | None = None
        self._worker: threading.Thread | None = None

        self._theme_var = tk.StringVar(value="Medieval Winter Watch")
        self._title_var = tk.StringVar(value="Holding the Frost-Bitten Night")
        self._ideas_var = tk.StringVar(value="20")
        self._script_words_var = tk.StringVar(value="32000")
        self._image_prompts_var = tk.StringVar(value="24")
        self._seed_var = tk.StringVar(value="")
        self._preview_var = tk.BooleanVar(value=False)
        self._status_var = tk.StringVar(value="Hazır")

        self._build_layout()

    # ------------------------------------------------------------------
    # UI construction helpers
    # ------------------------------------------------------------------
    def _build_layout(self) -> None:
        container = tk.Frame(self, padx=16, pady=16)
        container.pack(fill=tk.BOTH, expand=True)

        form_frame = tk.LabelFrame(container, text="İçerik Ayarları", padx=12, pady=8)
        form_frame.pack(fill=tk.X, anchor=tk.N)

        self._add_labeled_entry(form_frame, "Tema", self._theme_var, row=0)
        self._add_labeled_entry(form_frame, "Başlık", self._title_var, row=1)
        self._add_labeled_entry(form_frame, "Fikir Sayısı", self._ideas_var, row=2)
        self._add_labeled_entry(
            form_frame, "Senaryo Kelime Sayısı", self._script_words_var, row=3
        )
        self._add_labeled_entry(
            form_frame, "Görsel Prompt Sayısı", self._image_prompts_var, row=4
        )
        self._add_labeled_entry(form_frame, "Rastgele Tohum (isteğe bağlı)", self._seed_var, row=5)

        preview_check = tk.Checkbutton(
            form_frame,
            text="Önizleme modunu etkinleştir (kelime sayısının %5'i)",
            variable=self._preview_var,
        )
        preview_check.grid(row=6, column=0, columnspan=2, sticky="w", pady=(8, 0))

        button_frame = tk.Frame(container)
        button_frame.pack(fill=tk.X, pady=(12, 0))

        self._generate_button = tk.Button(
            button_frame,
            text="İçerik Oluştur",
            command=self._on_generate_clicked,
            height=2,
        )
        self._generate_button.pack(side=tk.LEFT, padx=(0, 8))

        save_button = tk.Button(
            button_frame,
            text="Sonucu Kaydet",
            command=self._on_save_clicked,
            height=2,
        )
        save_button.pack(side=tk.LEFT)

        status_label = tk.Label(button_frame, textvariable=self._status_var, anchor="w")
        status_label.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        output_frame = tk.LabelFrame(container, text="JSON Çıktısı", padx=8, pady=8)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(12, 0))

        self._output = tk.Text(output_frame, wrap=tk.NONE)
        self._output.pack(fill=tk.BOTH, expand=True)

        scrollbar_y = tk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self._output.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self._output.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = tk.Scrollbar(output_frame, orient=tk.HORIZONTAL, command=self._output.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self._output.configure(xscrollcommand=scrollbar_x.set)

    def _add_labeled_entry(
        self, parent: tk.Misc, label: str, variable: tk.StringVar, *, row: int
    ) -> None:
        lbl = tk.Label(parent, text=label)
        lbl.grid(row=row, column=0, sticky="w", padx=(0, 12), pady=4)
        entry = tk.Entry(parent, textvariable=variable, width=36)
        entry.grid(row=row, column=1, sticky="we", pady=4)
        parent.grid_columnconfigure(1, weight=1)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def _on_generate_clicked(self) -> None:
        if self._worker and self._worker.is_alive():
            return

        try:
            ideas_count = self._parse_positive_int(self._ideas_var.get(), "Fikir Sayısı")
            script_words = self._parse_positive_int(
                self._script_words_var.get(), "Senaryo Kelime Sayısı"
            )
            image_prompts = self._parse_positive_int(
                self._image_prompts_var.get(), "Görsel Prompt Sayısı"
            )
            seed = self._parse_optional_int(self._seed_var.get())
        except ValueError as exc:
            messagebox.showerror("Geçersiz Girdi", str(exc), parent=self)
            return

        params = dict(
            theme=self._theme_var.get().strip(),
            title=self._title_var.get().strip(),
            ideas_count=ideas_count,
            script_words=script_words,
            image_prompts=image_prompts,
            seed=seed,
            preview=self._preview_var.get(),
        )

        if not params["theme"] or not params["title"]:
            messagebox.showerror(
                "Eksik Bilgi",
                "Lütfen tema ve başlık alanlarını doldurun.",
                parent=self,
            )
            return

        self._status_var.set("İşleniyor...")
        self._generate_button.config(state=tk.DISABLED)
        self._output.delete("1.0", tk.END)

        self._worker = threading.Thread(
            target=self._run_generation, args=(params,), daemon=True
        )
        self._worker.start()

    def _run_generation(self, params: Dict[str, Any]) -> None:
        try:
            payload = generate_payload(**params)
        except Exception as exc:  # pragma: no cover - GUI feedback
            self.after(0, lambda: self._on_generation_error(exc))
        else:
            self.after(0, lambda: self._on_generation_success(payload))

    def _on_generation_success(self, payload: Dict[str, Any]) -> None:
        self._last_payload = payload
        pretty = json.dumps(payload, ensure_ascii=False, indent=2)
        self._output.delete("1.0", tk.END)
        self._output.insert(tk.END, pretty)
        self._status_var.set("Tamamlandı")
        self._generate_button.config(state=tk.NORMAL)

    def _on_generation_error(self, error: Exception) -> None:
        self._status_var.set("Hata oluştu")
        self._generate_button.config(state=tk.NORMAL)
        messagebox.showerror("Üretim Hatası", str(error), parent=self)

    def _on_save_clicked(self) -> None:
        if not self._last_payload:
            messagebox.showinfo(
                "Kaydedilecek İçerik Yok",
                "Önce bir içerik oluşturmalısınız.",
                parent=self,
            )
            return

        file_path = filedialog.asksaveasfilename(
            title="JSON çıktısını kaydet",
            defaultextension=".json",
            filetypes=(("JSON dosyası", "*.json"), ("Tüm dosyalar", "*.*")),
        )
        if not file_path:
            return

        with open(file_path, "w", encoding="utf-8") as fh:
            json.dump(self._last_payload, fh, ensure_ascii=False, indent=2)
        self._status_var.set(f"Kaydedildi: {file_path}")

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _parse_positive_int(value: str, field: str) -> int:
        try:
            parsed = int(value)
        except ValueError as exc:
            raise ValueError(f"{field} sayısal olmalı.") from exc
        if parsed <= 0:
            raise ValueError(f"{field} pozitif olmalı.")
        return parsed

    @staticmethod
    def _parse_optional_int(value: str) -> int | None:
        value = value.strip()
        if not value:
            return None
        try:
            return int(value)
        except ValueError as exc:  # pragma: no cover - GUI feedback
            raise ValueError("Tohum değeri sayısal olmalı.") from exc


def run_app() -> None:
    """Launch the Tkinter application."""

    app = GeneratorApp()
    app.mainloop()


if __name__ == "__main__":  # pragma: no cover - manual invocation
    run_app()
