# ТЗ: Longevity Dashboard — тёмная тема и редизайн карточек

Цель: привести внешний вид страницы `/longevity` к виду из согласованного макета.
Все правки — в `data/derived/reports/longevity_v1.html` и `scripts/reports/build_longevity_v1.py` (HTML-шаблон дублирован в функции `_html()`).

---

## 1. Тёмная цветовая схема (CSS variables)

Заменить весь блок `:root{...}` на:

```css
:root{
  --bg:#13161c;
  --bg2:#1c2029;
  --panel:#1e2230;
  --panel2:#252a38;
  --line:#2d3348;
  --text:#e8eaf0;
  --muted:#7b82a0;
  --green:#4ade80;
  --green-bg:#14281e;
  --green-text:#4ade80;
  --green-line:#1e4a2e;
  --amber:#f59e0b;
  --amber-bg:#2a1f0a;
  --amber-text:#fbbf24;
  --amber-line:#4a3210;
  --red:#f87171;
  --red-bg:#2a0f0f;
  --red-text:#f87171;
  --red-line:#4a1818;
  --gray-bg:#1e2230;
  --gray-text:#7b82a0;
  --gray-line:#2d3348;
  --dot-green:#4ade80;
  --dot-amber:#f59e0b;
  --dot-red:#f87171;
  --dot-gray:#4b5270;
}
body{background:var(--bg)}
.section,.panel{background:var(--panel);border-color:var(--line)}
.zone{background:var(--panel2);border-color:var(--line)}
.goal{background:var(--panel);border-color:var(--line);color:var(--text)}
.kpi{background:var(--panel2);border-color:var(--line)}
.notice{background:var(--panel);border-color:var(--line);color:var(--text)}
.progress-track{background:#2d3348}
.progress-fill{background:var(--green)}
button{background:var(--panel2);border-color:var(--line);color:var(--text)}
button:hover{background:var(--panel);border-color:var(--muted)}
.metric{border-color:var(--line)}
.item{border-color:var(--line)}
.screening{border-color:var(--line)}
.tag{background:var(--panel2);border-color:var(--line);color:var(--text)}
.badge.green{background:var(--green-bg);color:var(--green-text);border-color:var(--green-line)}
.badge.amber{background:var(--amber-bg);color:var(--amber-text);border-color:var(--amber-line)}
.badge.red{background:var(--red-bg);color:var(--red-text);border-color:var(--red-line)}
.badge.gray{background:var(--gray-bg);color:var(--gray-text);border-color:var(--gray-line)}
h1,h2,h3{color:var(--text)}
a{color:var(--muted)}
.muted{color:var(--muted)}
```

---

## 2. Шапка — goal block

Сделать цифру "100" крупнее и выровнять в топ-правом блоке:

```css
.goal .num{font-size:40px;font-weight:800}
.goal .label-top{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:0.08em}
```

В HTML шапки (функция `render` или статичный HTML):
```html
<div class="goal">
  <div class="label-top">цель</div>
  <div class="num">100 <span style="font-size:18px;font-weight:400">лет</span></div>
</div>
```

---

## 3. Горизонт жизни — progress bar с разметкой

Заменить текущий прогрессбар на вариант с масштабными метками и аннотацией "сейчас":

В CSS добавить:
```css
.horizon-bar-wrap{position:relative;margin:14px 0 6px}
.horizon-scale{display:flex;justify-content:space-between;font-size:11px;color:var(--muted);margin-top:4px}
.horizon-scale .mark-100{color:var(--green)}
.horizon-now{position:absolute;top:-18px;font-size:11px;color:var(--text);white-space:nowrap;transform:translateX(-50%)}
.horizon-now::after{content:'↓';display:block;text-align:center;line-height:1}
```

В `render()` заменить блок progress bar:
```js
const nowLabel = `${e(h.current_age ?? '?')} лет`;
app.innerHTML = `
  ...
  <div class="section">
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px">
      <h2 style="margin:0">Горизонт жизни</h2>
      <span class="muted" style="font-size:12px">оценка на основе текущих маркеров</span>
    </div>
    <div class="horizon-bar-wrap">
      <div style="position:absolute;left:${pct}%;top:-18px;font-size:11px;color:var(--text);white-space:nowrap;transform:translateX(-50%)">← сейчас</div>
      <div class="progress-track"><div class="progress-fill" style="width:${pct}%"></div></div>
      <div class="horizon-scale">
        <span>0</span><span>50</span><span>75</span><span class="mark-100">100 +</span>
      </div>
    </div>
    <div class="kpis">
      <div class="kpi"><div class="label">данных в системе</div><div class="value">${e(h.data_years ?? 0)} г</div></div>
      <div class="kpi"><div class="label">маркеров отслеживается</div><div class="value">${e(h.tracked_markers ?? 0)} / ~40</div></div>
      <div class="kpi"><div class="label">зон под контролем</div><div class="value">${e(h.zones_under_control ?? 0)} из 4</div></div>
      <div class="kpi"><div class="label">действий требуют внимания</div><div class="value" style="color:${(h.actions_need_attention||0)>0?'var(--red)':'var(--text)'}">${e(h.actions_need_attention ?? 0)}</div></div>
    </div>
  </div>
  ...
`;
```

---

## 4. Секционный заголовок "ЧЕТЫРЕ ГЛАВНЫХ РИСКА"

Добавить перед блоком всадников (внутри `render()`):

```js
<div style="grid-column:span 12;font-size:11px;font-weight:600;letter-spacing:0.12em;color:var(--muted);text-transform:uppercase;padding:4px 0">Четыре главных риска</div>
<div class="section">
  <div class="zones">${Object.values(horsemen).map(zoneHtml).join('')}</div>
</div>
```

Убрать `<h2>Четыре всадника</h2>` из `<div class="section">` — теперь он заменён на внешний секционный лейбл.

---

## 5. Карточки всадников — subtitle + метрики-точки + кнопка

### 5a. Подписи под названием зоны (hardcode)

В функцию `zoneHtml` добавить маппинг subtitle и кнопок:

```js
function zoneHtml(zone){
  const icons = {cardiovascular:'ti-heart',metabolic:'ti-bolt',cancer:'ti-microscope',neuro:'ti-brain'};
  const subtitles = {
    cardiovascular:'Главная причина ранней смерти',
    metabolic:'Инсулинорезистентность — за 15 лет до диагноза',
    cancer:'Раннее выявление = 90%+ выживаемость',
    neuro:'Альцгеймер начинается за 20 лет до симптомов'
  };
  const btnLabels = {
    cardiovascular:'Что сдать',
    metabolic:'Что сдать',
    cancer:'Скрининги',
    neuro:'Как начать'
  };
  const icon = icons[zone.id] || 'ti-circle';
  const subtitle = subtitles[zone.id] || '';
  const btnLabel = btnLabels[zone.id] || 'Подробнее';
  return `<div class="zone">
    <div class="zone-head">
      <div>
        <h3><i class="ti ${icon}" aria-hidden="true"></i> ${e(zone.title)}</h3>
        ${subtitle ? `<div style="font-size:12px;color:var(--muted);margin-top:2px">${e(subtitle)}</div>` : ''}
      </div>
      <span class="badge ${statusClass(zone.status)}">${e(zone.status_label || statusLabel(zone.status))}</span>
    </div>
    <div class="metrics">${(zone.metrics||[]).map(metricDotHtml).join('')}</div>
    <button type="button" style="width:100%;margin-top:10px;text-align:center" onclick="sendPrompt('${e(btnLabel)} для зоны ${e(zone.title)}')">${e(btnLabel)} ↗</button>
  </div>`;
}
```

### 5b. Новый формат строки метрики — точка + значение справа

Добавить функцию `metricDotHtml` (используется внутри карточек всадников):

```js
const dotColors = {green:'var(--dot-green)',amber:'var(--dot-amber)',red:'var(--dot-red)',gray:'var(--dot-gray)'};
function metricDotHtml(m){
  const dot = `<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${dotColors[m.status]||dotColors.gray};margin-right:6px;flex-shrink:0;margin-top:3px"></span>`;
  const val = m.value !== null && m.value !== undefined && m.value !== ''
    ? `${e(m.value)}${m.unit ? ' '+e(m.unit) : ''}` : 'нет данных';
  const yr = m.event_date ? m.event_date.slice(0,4) : null;
  const display = m.status === 'gray'
    ? `<span style="color:var(--muted)">${val}</span>`
    : `<span>${val}${yr ? ` <span style="color:var(--muted)">(${yr})</span>` : ''}</span>`;
  return `<div class="metric" style="grid-template-columns:1fr auto;align-items:start">
    <div class="name">${e(m.label)}</div>
    <div style="display:flex;align-items:flex-start;text-align:right;font-size:13px">${dot}${display}</div>
  </div>`;
}
```

В остальных секциях (физические показатели, воспаление, гормоны) оставить старый `metricHtml` с badge — он удобнее для детальных данных.

---

## 6. CSS дополнения для новых элементов

Добавить в `<style>`:

```css
.zone-head{align-items:flex-start}
.metric .name{font-size:13px;color:var(--muted);font-weight:400}
.kpi .label{font-size:11px}
.kpi .value{font-size:22px}
.progress-fill{transition:width 0.6s ease}
```

---

## 7. Ссылка "Documents UI"

Заменить ссылку в toolbar на стилизованную:

```html
<a href="/ui" style="font-size:13px;color:var(--muted);text-decoration:none">← Документы</a>
```

---

## Итого: что меняется

| Где | Что |
|-----|-----|
| CSS `:root` | Полная замена на тёмную палитру |
| Шапка `.goal` | Крупнее "100 лет", лейбл "цель" мелкий |
| Горизонт | Разметка 0/50/75/100, аннотация "← сейчас", "N из 4" в KPI |
| Заголовок всадников | Убрать `<h2>` из секции, добавить uppercase label снаружи |
| `zoneHtml` | Иконки, subtitle, кнопка с sendPrompt |
| Новая `metricDotHtml` | Точка + значение справа (для карточек всадников) |
| CSS добавки | font-size, weight, transition |

Функции `metricHtml`, `metricSection`, `screeningHtml`, `actionsHtml`, `gapsHtml` — оставить без изменений (только цвета подтянутся через CSS variables).
