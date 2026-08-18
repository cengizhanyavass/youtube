# Habitar Largo — dar niş / geniş hacim büyüme planı

**Kanal:** İspanyolca, 60+ yaş için güvenli ve erişilebilir konut. Animasyon + maskot,
12–17 dk long-form. 4 video, ~4 gün, ~2 izlenme.

**Not:** Bu plan görsel kanıt (4 video + thumbnail) ve niş bilgisi üzerine kuruldu.
İzlenme/abone rakamları içeren her iddia `tools/viral_scout.py` ile doğrulanmalı —
komutlar aşağıda. Rakam uydurulmadı, uydurulmayacak.

---

## 1. Teşhis: sorun retention değil, kimlik ve hacim

4 günlük kanalda 2 izlenme **normaldir**. YouTube yeni kanalı 20–50 kişilik minik
test grubuna gösterir; o grup tıklamazsa video durur. Yani ilk 20 videoda tek
önemli metrik CTR + ilk 30 saniye. Şu an düzeltilecek 4 somut şey var:

| Sorun | Kanıt | Düzeltme |
|---|---|---|
| Başlıklar mobilde kesiliyor | "Cómo preparar una casa segura después de los 60 de principio a fin" = 65 karakter | 45–52 karakterde bitir. "de principio a fin" gibi boş kuyrukları at |
| Süre yeni kanal için uzun | 16:59 / 13:17 | İlk 15 videoda **8–11 dk**. Yüzde olarak retention yükselir, algoritma daha çok dağıtır |
| Thumbnail metni tutarsız | "10 MIDE ESTO ANTES" okuma sırası karışık | Kural: **en fazla 3 kelime**, tek satır ya da iki satır. "MIDE ESTO ANTES" yeter, 10'u başlığa bırak |
| Konu dağınık başladı | 4 video 4 farklı alt konu | İlk 15 videoyu **tek kümede** topla (banyo + düşme). Algoritmanın kanalı tanıması için tekrar şart |

En güçlü varlığın: **"TU BAÑO TE FRENA"** thumbnail'i. Doğru kümeyi de o işaret ediyor.

---

## 2. Niş stratejisi: dar gir, hacmi kümeyle büyüt

Senin istediğin şey ("dar nişten katılıp büyümek") bu nişte tam olarak çalışır,
çünkü niş dar ama **kitle devasa**: İspanyolca konuşan 60+ nüfus + onların
40–55 yaşındaki çocukları. Çocuklar çoğu zaman asıl tıklayan taraftır — bu yüzden
listede onlara yönelik başlıklar da var.

**Çekirdek (ilk 15 video):** `casa segura + baño + caídas`
**1. halka (16–30):** `casa o piso, mudanza, vender`
**2. halka (31+):** `dinero: reformas, ayudas, coste`
**3. halka:** `vivir solo, autonomía diaria`

Neden bu sıra: banyo/düşme konusu **korku + acil ihtiyaç** taşır, en yüksek CTR
oradadır. Kanal orada kimlik kazanınca YouTube seni aynı izleyiciye para ve
taşınma videolarında da önerir. Ters sırayla giden kanallar takılıp kalıyor.

---

## 3. Başka dillerden taşınacak formatlar

Bu formatlar İngilizce/Almanca'da olgun, İspanyolca'da büyük ölçüde **kurumsal ve
sıkıcı** (sigorta şirketi, ortopedi mağazası, belediye videoları). Animasyonlu
anlatım boşlukta — senin avantajın bu.

| Kaynak dildeki format | İspanyolca uyarlaman | Neden taşınır |
|---|---|---|
| "Aging in place home modifications" (EN) | `Adaptar la casa para la vejez` serisi | Arama hacmi sabit, mevsimsel değil |
| "Things to get rid of after 60" (EN) | `10 cosas que debes tirar después de los 60` | Liste + yaş kimliği; en kolay viral kalıp |
| "Bathroom falls" (EN) | `El baño y las caídas` | Korku + çözüm, en yüksek CTR |
| "Downsizing after retirement" (EN) | `¿Vender la casa a los 70?` | Karar videosu, izlenme süresi uzun |
| "Barrierefrei umbauen" (DE) | `Reformar sin obras` | Almanca'da teknik, İspanyolca'da hikâyeleştirilmemiş |
| "Sturzprophylaxe" (DE) | `9 puntos donde ocurren las caídas` | Klinik bilgi + görsel anlatım = animasyona birebir |
| "Como falar com os pais" (PT) | `Hablar con tus padres sin discutir` | Çocuk kitlesini kanala sokar |

**Doğrulama komutu** (gerçek izlenme/abone verisiyle):
```bash
.venv/bin/python tools/viral_scout.py --queries-file scripts/queries.json \
  --max-subs 80000 --min-views 80000 --top 25
```
Çıkan tabloda `oran` 20x+ olan satırlar = konunun kanalı taşıdığı videolar.
Onları birebir çevirme, **kalıbını** al.

---

## 4. Viral video listesi (30 başlık)

Her satır: başlık (ES) · thumbnail metni · ilk 10 saniyenin kancası.
Sıra önemli — yukarıdan aşağı çek.

### Küme A — Baño (video 1–8, en yüksek öncelik)

1. **La ducha que evita la mayoría de las caídas en casa** · `ESTA DUCHA NO` · "Si tu ducha tiene este borde, tienes un problema y no lo sabes."
2. **Quita la bañera después de los 65: esto va en su lugar** · `QUITA LA BAÑERA` · "Entrar en la bañera exige levantar la pierna 40 cm. A los 70, eso es una apuesta."
3. **Las barras de apoyo mal puestas no sujetan nada** · `MAL PUESTA` · "Esta barra está puesta al revés. La mitad de las casas la tiene así."
4. **El suelo del baño que resbala aunque parezca seguro** · `RESBALA` · "El suelo mojado no es el peligro. El peligro es este otro."
5. **Cuánto cuesta adaptar un baño de verdad** · `PRECIO REAL` · "Te van a dar tres presupuestos. Solo uno tiene sentido."
6. **Ir al baño de noche: el trayecto más peligroso de la casa** · `A LAS 3 AM` · "A las tres de la mañana tu casa es otra casa."
7. **7 errores del baño que te quitan autonomía** · `7 ERRORES` · *(yeniden çek: 9 dk, başlık kısaltılmış)*
8. **Adaptar el baño sin obras: 6 cambios de un día** · `SIN OBRAS` · "No hace falta romper nada. Ni pedir permiso."

### Küme B — Caídas y rutina diaria (9–15)

9. **9 puntos de la casa donde ocurren las caídas** · `9 PUNTOS` · "El 80% de las caídas pasan en cuatro metros cuadrados."
10. **La alfombra que le costó la cadera a una vecina** · `LA ALFOMBRA` · "Era una alfombra bonita. Llevaba 20 años ahí."
11. **Cómo levantarte del suelo si te caes y estás solo** · `SI TE CAES` · "Lo primero no es levantarse. Es esto."
12. **El pasillo mal iluminado: el arreglo más barato** · `12 EUROS` · "Doce euros. Ese es el coste de arreglar el punto más peligroso."
13. **La cocina te quita fuerza cada día y no lo notas** · `TU COCINA` · "Si abres este armario de puntillas, ya estás perdiendo autonomía."
14. **Dormir arriba después de los 70: ¿sí o no?** · `¿SUBIR O NO?` · "Catorce escalones, cuatro veces al día, cinco mil veces al año."
15. **Escaleras: adaptarlas o mudarse** · `O TE MUDAS` · "Hay un número que decide esto por ti."

### Küme C — Casa o piso, mudanza (16–22)

16. **¿Vender la casa a los 70? Cuándo sí y cuándo es un error** · `¿VENDER YA?` · "Vender es fácil. Volver atrás, no."
17. **Mudarte cerca de tus hijos: lo que nadie te cuenta** · `CERCA DE ELLOS` · "Suena bien. Hasta el segundo año."
18. **Pueblo o ciudad después de jubilarte** · `¿PUEBLO O CIUDAD?` · "La respuesta cambia el día que dejas de conducir."
19. **El ascensor no lo es todo: 6 cosas antes de comprar piso** · `NO SOLO ASCENSOR` · "Hay ascensor. Y aun así no puedes entrar."
20. **Casa de una planta o apartamento después de los 60** · `¿CASA O PISO?` · *(yeniden çek: 10 dk)*
21. **Antes de comprar una casa para jubilarte, mide esto** · `MIDE ESTO ANTES` · *(thumbnail düzelt, 10'u kaldır)*
22. **La casa perfecta a los 60 que no sirve a los 80** · `A LOS 80 NO` · "La compraron pensando en los nietos. No en las rodillas."

### Küme D — Dinero (23–26)

23. **Adaptar la casa entera con poco dinero: el orden correcto** · `EN ESTE ORDEN` · "Si tienes 2.000 euros, hay un orden que multiplica lo que compras."
24. **Ayudas para adaptar la vivienda: cómo se piden paso a paso** · `PASO A PASO` · "El trámite tiene tres puertas. La mayoría llama a la equivocada." *(ülkeye göre güncel mevzuatı kendin doğrula)*
25. **5 reformas que dan seguridad y suben el valor de la casa** · `SUBE EL VALOR` · "Seguridad y dinero no siempre van juntos. Aquí sí."
26. **El error de gastar en lo bonito antes que en lo seguro** · `BONITO ≠ SEGURO` · "Cambiaron la cocina entera. El escalón sigue ahí."

### Küme E — Vivir solo / autonomía (27–28)

27. **Vivir solo después de los 75: 8 cosas que debes tener** · `VIVIR SOLO` · "No es cuestión de valentía. Es cuestión de ocho objetos."
28. **Cómo pedir ayuda si te caes y no llegas al teléfono** · `NO LLEGO` · "El teléfono está en la mesa. Tú estás en el suelo."

### Küme F — Hijos (29–30, kanala yeni kitle sokar)

29. **Señales de que la casa de tus padres ya no es segura** · `MIRA ESTO` · "La próxima vez que entres en casa de tus padres, mira el suelo primero."
30. **Hablar con tus padres de adaptar su casa sin discutir** · `SIN DISCUTIR` · "No empieces por la casa. Empieza por esta frase."

---

## 4b. Üç seri = büyüme motoru

Ürettiğin üç seri farklı işler yapıyor; bunu bilerek dengelemen gerekiyor:

| Seri | Ne getirir | Trafik kaynağı | Oran |
|---|---|---|---|
| **La Casa Después de los 60** | Yüksek niyetli izleyici, arama trafiği, otorite | Búsqueda | %40 |
| **Secretos de la Casa de Antes** | Hacim, nostalji, yüksek CTR, yorum | Browse / Sugeridos | %40 |
| **Lo que las Casas Modernas Olvidaron** | Tartışma, paylaşım, yeni kitle | Sugeridos | %20 |

"Dar nişten girip büyümek" tam olarak budur: **Después de los 60** seni bir konuda
otorite yapar (dar), **Casa de Antes** hacmi getirir (geniş). Nostalji 60+ kitlede
en güçlü tıklama sebebidir ve senin animasyon tarzın buna İspanyolca'da neredeyse
rakipsiz uyuyor — arşiv görüntüsü bulmak zor, çizim ise sınırsız.

**Önemli kural:** her nostalji videosunun sonunda bir "Después de los 60" videosuna
köprü kur. Nostalji izleyiciyi getirir, dar seri onu abone yapar.

### Küme G — Secretos de la Casa de Antes (nostalji, hacim motoru)

31. **Por qué las casas de antes no tenían pasillos largos** · `SIN PASILLOS` · "Los albañiles de 1950 sabían algo que hoy se nos olvidó."
32. **El truco de la abuela para que la casa fuera fresca sin aire acondicionado** · `SIN AIRE` · "Treinta y ocho grados fuera. Dentro se dormía con manta."
33. **La despensa: la habitación que desapareció de las casas** · `LA DESPENSA` · "Ocupaba dos metros. Ahorraba un sueldo al año."
34. **Por qué las ventanas de antes duraban 60 años** · `60 AÑOS` · "La misma ventana. Tres generaciones."
35. **La cocina de carbón y lo que enseñó a toda una generación** · `LA COCINA DE ANTES` · "Encender el fuego era el primer trabajo del día."
36. **Las casas de pueblo tenían este muro por una razón** · `ESTE MURO` · "Medio metro de grosor. Nadie construía así por gusto."
37. **7 cosas que había en todas las casas y hoy no hay en ninguna** · `7 COSAS` · "Estaban en todas. Ahora en ninguna."
38. **El patio interior: el invento que refrescaba la casa entera** · `EL PATIO` · "Un agujero en el techo enfriaba ocho habitaciones."
39. **Por qué antes se dormía mejor sin calefacción** · `SIN CALEFACCIÓN` · "Cero grados en la habitación. Y se dormía del tirón."
40. **La casa de tus abuelos estaba mejor pensada que la tuya** · `MEJOR PENSADA` · "Sin arquitecto, sin planos, sin dinero. Y funcionaba."

### Küme H — Lo que las Casas Modernas Olvidaron (tartışma motoru)

41. **Las casas modernas son bonitas y se viven mal** · `BONITA, INCÓMODA` · "Sale en la foto perfecta. Vívela un invierno."
42. **Por qué los pisos nuevos tienen menos ventanas que los de 1970** · `MENOS LUZ` · "Mismo metraje. La mitad de la luz."
43. **La cocina abierta: la moda que nadie te contó bien** · `COCINA ABIERTA` · "Queda enorme en el catálogo. Y huele a todo."
44. **Techos de 2,50: lo que perdimos al bajarlos** · `2,50 METROS` · "Sesenta centímetros menos. Y se nota cada día."
45. **Los materiales de hoy duran 15 años, los de antes 80** · `15 VS 80` · "Mismo precio real. Un quinto de vida."
46. **La casa moderna no está pensada para envejecer en ella** · `NO ENVEJECE` · "Está diseñada para tener 35 años. Siempre."
47. **Muebles que se tiran en 5 años: cómo elegían nuestros padres** · `5 AÑOS` · "Aquel armario sigue en pie. El tuyo ya cojea."
48. **Por qué ya no se hacen recibidores (y por qué importaba)** · `SIN RECIBIDOR` · "Entrabas y ya estabas en el salón. Eso cambia la casa."
49. **Aislamiento: el engaño de las casas nuevas** · `MAL AISLADA` · "Certificado energético A. Y pagas más de calefacción."
50. **Si tuvieras que construir hoy, copia estas 8 cosas de antes** · `COPIA ESTO` · "Ocho ideas viejas que hoy valdrían una fortuna."

---

## 5. Paketleme kuralları (her videoda uygula)

- **Başlık:** 45–52 karakter. "después de los 60" ifadesini videoların ~%60'ında kullan, hepsinde değil — küme kimliği için yeterli, tekrar bıkkınlık yapmasın.
- **Thumbnail:** en fazla 3 kelime · maskot + tek kırmızı işaret · metin sol, görsel sağ (şu anki düzenin doğru, koru).
- **İlk 10 saniye:** doğrudan tehlikeyi göster. Selamlama, kanal tanıtımı, "hoş geldiniz" yok. 60+ kitlede giriş müziği izleyici kaybettirir.
- **Süre:** 8–11 dk, kanal 1.000 aboneye ulaşana kadar.
- **Bitiş:** her video aynı kümedeki bir sonrakine köprü kursun ("si tu baño tiene esto, mira este otro"). Suggested trafiği ancak zincirle gelir.
- **Playlist:** küme başına tek oynatma listesi, sırayla. A kümesi: "Baño seguro después de los 60".
- **Açıklama:** ilk satırda videonun tek cümlelik vaadi + kümenin anahtar kelimesi.

## 6. İlk 30 gün

Haftada 3 video, 2 dar + 1 nostalji dengesiyle:

| Hafta | Después de los 60 | Casa de Antes / Modernas |
|---|---|---|
| 1 | 1, 2 | 31 |
| 2 | 3, 6 | 41 |
| 3 | 9, 10 | 32 |
| 4 | 11, 16 | 37 |

Ek işler: hafta 1'de mevcut 4 videonun başlık + thumbnail'ini düzelt (yeniden
yüklemeden). Hafta 2'de küme playlist'lerini kur ve köprüleri ekle. Hafta 3'te
`viral_scout` çıktısındaki en yüksek oranlı 3 formatı listeye ekle. Hafta 4'te en
iyi CTR'yi alan videonun kalıbından 2 varyant daha çek — tutan kalıp tekrarlanır.

Ölçüm: her Pazar `.venv/bin/python tools/channel_analyze.py <kanal_url>` çalıştır,
`out/rapor.txt`'i bana yapıştır — hangi kalıbın tuttuğunu veriden görürüz.
