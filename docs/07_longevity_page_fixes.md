# Правки к longevity dashboard — rev 1

Файлы для изменений: `data/derived/reports/longevity_v1.html` и `scripts/reports/build_longevity_v1.py`.
HTML-шаблон дублирован в обоих файлах — все правки применять к обоим одновременно (в `build_longevity_v1.py` шаблон находится внутри функции `_html()`).

---

## 1. Бейджи приоритета в "Приоритетных действиях" — английские слова

**Где:** функция `actionsHtml`, строка с `badge`.

**Было:**
```js
<span class="badge ${statusClass(x.priority)}">${e(x.priority)}</span>
```

**Стало:**
```js
<span class="badge ${statusClass(x.priority)}">${e(statusLabel(x.priority))}</span>
```

`statusLabel()` уже определена выше в скрипте и возвращает "требует внимания" / "пробелы данных" / "нет данных".

---

## 2. Заголовок секции — неверный

**Где:** функция `render()`, секция всадников.

**Было:**
```js
<h2>Четыре зоны риска</h2>
```

**Стало:**
```js
<h2>Четыре всадника</h2>
```

---

## 3. KPI-блок в "Горизонт жизни" — неверный набор

**Где:** функция `render()`, блок `.kpis`.

По ТЗ 4 KPI должны быть: **лет данных / маркеров отслеживается / зон под контролем / действий требуют внимания**.
Возраст — не KPI, его нужно показать как аннотацию рядом с progress bar.
`h.zones_under_control` уже есть в API payload, просто не рендерится.

**Было:**
```js
<div class="kpis">
  <div class="kpi"><div class="label">возраст</div><div class="value">${e(h.current_age ?? 'н/д')}</div></div>
  <div class="kpi"><div class="label">лет данных</div><div class="value">${e(h.data_years ?? 0)}</div></div>
  <div class="kpi"><div class="label">маркеров</div><div class="value">${e(h.tracked_markers ?? 0)}</div></div>
  <div class="kpi"><div class="label">требуют внимания</div><div class="value">${e(h.actions_need_attention ?? 0)}</div></div>
</div>
```

**Стало:**
```js
<div style="font-size:13px;color:var(--muted);margin-bottom:4px">${e(h.current_age ?? '?')} лет → цель 100</div>
<div class="progress-track"><div class="progress-fill" style="width:${pct}%"></div></div>
<div class="kpis">
  <div class="kpi"><div class="label">лет данных</div><div class="value">${e(h.data_years ?? 0)}</div></div>
  <div class="kpi"><div class="label">маркеров</div><div class="value">${e(h.tracked_markers ?? 0)}</div></div>
  <div class="kpi"><div class="label">зон под контролем</div><div class="value">${e(h.zones_under_control ?? 0)}</div></div>
  <div class="kpi"><div class="label">требуют внимания</div><div class="value">${e(h.actions_need_attention ?? 0)}</div></div>
</div>
```

Также убрать из `render()` старую строку с progress bar (она была над kpis) — теперь она встроена внутрь нового блока выше.

---

## 4. Бейджи в "Что нужно добавить" — все серые, без приоритета

**Где:** функция `gapsHtml`.

Screening gaps имеют приоритет `red`/`amber`, остальные — `gray`. Сейчас все теги одного стиля.

**Было:**
```js
<span class="tag">${e(g.title)}</span>
```

**Стало:**
```js
<span class="badge ${statusClass(g.priority)}">${e(g.title)}</span>
```

CSS-класс `.tag` можно оставить или удалить — `badge` уже имеет нужные стили для цветовых состояний.

---

## 5. Секция "Протоколы" — убрать из видимого layout

По ТЗ страница не содержит секцию "Протоколы" как отдельный блок — это тип данных для ввода.

**Где:** функция `render()`.

**Было:**
```js
${protocolsHtml(payload.protocols || [])}
```

**Стало:** удалить эту строку из `render()`. Функцию `protocolsHtml` можно оставить в коде на будущее, просто не вызывать.

---

## 6. Иконки на карточках всадников

**Где:** функция `zoneHtml`.

Добавить в начало функции маппинг иконок:
```js
function zoneHtml(zone){
  const icons = {cardiovascular:'♥',metabolic:'⚡',cancer:'🔬',neuro:'🧠'};
  const icon = icons[zone.id] || '';
  return `<div class="zone">
    <div class="zone-head">
      <h3>${icon} ${e(zone.title)}</h3>
      <span class="badge ${statusClass(zone.status)}">${e(zone.status_label || statusLabel(zone.status))}</span>
    </div>
    <div class="metrics">${(zone.metrics||[]).map(metricHtml).join('')}</div>
  </div>`;
}
```

---

## 7. Физические показатели — одна колонка вместо двух

**Где:** CSS + функция `metricSection` (или создать отдельную функцию для физических показателей).

Добавить CSS:
```css
.metrics-2col{grid-template-columns:1fr 1fr}
@media(max-width:900px){.metrics-2col{grid-template-columns:1fr}}
```

В `render()` заменить:
```js
${metricSection('Физические показатели', payload.physical_baselines || [])}
```

на inline-вариант с двумя колонками:
```js
<div class="section half">
  <h2>Физические показатели</h2>
  <div class="metrics metrics-2col">${(payload.physical_baselines||[]).map(metricHtml).join('') || '<div class="muted">нет данных</div>'}</div>
</div>
```

---

## 8. Тренд моноцитов (изменение в `longevity_overview.py`)

По ТЗ: "Моноциты (с трендом)". Сейчас показывается только последнее значение.

**Изменение в `longevity_overview.py`**, функция `build_longevity_overview`:

После сборки `inflammation` добавить в маркер `monocytes` поле `trend` — список последних 5 измерений по убыванию даты:

```python
# после сборки inflammation
_monocyte_rows = sorted(
    _find_lab_rows(labs, ["моноцит", "mon%"]),
    key=lambda x: (_parse_date(x.get("event_date")) or date.min),
    reverse=True,
)
for m in inflammation:
    if m.get("id") == "monocytes":
        m["trend"] = [
            {
                "date": _iso(r.get("event_date")),
                "value": r.get("value_text"),
                "abnormal": bool(r.get("abnormal_flag")),
            }
            for r in _monocyte_rows[:5]
        ]
```

**В HTML**, в функции `metricHtml` добавить специальный рендер для тренда, если поле `trend` присутствует:

```js
function metricHtml(m){
  const cls = statusClass(m.status);
  const date = m.event_date ? `${shortDate(m.event_date)} (${daysText(m.days_since)})` : 'даты нет';
  const trendHtml = (m.trend && m.trend.length > 1)
    ? `<div class="meta">${m.trend.slice().reverse().map(t=>`<span style="color:${t.abnormal?'var(--red)':'inherit'}">${e(t.value||'?')}</span>`).join(' → ')}</div>`
    : '';
  return `<div class="metric">
    <div>
      <div class="name">${e(m.label)}</div>
      <div class="value">${e(metricValue(m))}</div>
      <div class="meta">${e(date)}${m.reference ? ` | ref: ${e(m.reference)}` : ''}</div>
      ${trendHtml}
    </div>
    <span class="badge ${cls}">${e(statusLabel(m.status))}</span>
  </div>`;
}
```

---

## Приоритеты

| # | Пункт | Приоритет |
|---|-------|-----------|
| 1 | Бейджи на русском в "Приоритетных действиях" | обязательно |
| 2 | Заголовок "Четыре всадника" | обязательно |
| 3 | KPI-блок: убрать возраст, добавить "зон под контролем" | обязательно |
| 4 | Gaps с цветом по приоритету | обязательно |
| 5 | Убрать секцию "Протоколы" из layout | хорошо бы |
| 6 | Иконки на карточках всадников | хорошо бы |
| 7 | Физические показатели в 2 колонки | хорошо бы |
| 8 | Тренд моноцитов | улучшение |
