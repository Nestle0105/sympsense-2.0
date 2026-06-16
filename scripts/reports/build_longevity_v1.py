from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(".").resolve()
SRC_ROOT = PROJECT_ROOT / "apps/cli/src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from sympsense.longevity_overview import build_longevity_overview


def _html() -> str:
    return """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Longevity overview</title>
<style>
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
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:Segoe UI,Arial,sans-serif}
.wrap{max-width:1480px;margin:0 auto;padding:22px}
.top{display:flex;justify-content:space-between;gap:16px;align-items:flex-start;margin-bottom:14px}
h1{font-size:34px;line-height:1.1;margin:0 0 6px;font-weight:800}
h2{font-size:18px;margin:0 0 8px}
h3{font-size:15px;margin:0}
h1,h2,h3{color:var(--text)}
a{color:var(--muted)}
.muted{color:var(--muted)}
.goal{border:1px solid var(--line);background:var(--panel);color:var(--text);border-radius:8px;padding:10px 12px;min-width:160px;text-align:right}
.goal .num{font-size:40px;font-weight:800}
.goal .label-top{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:0.08em}
.toolbar{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:12px 0}
button{border:1px solid var(--line);background:var(--panel2);color:var(--text);border-radius:8px;padding:7px 10px;cursor:pointer}
button:hover{background:var(--panel);border-color:var(--muted)}
.notice{padding:10px 12px;border:1px solid var(--line);background:var(--panel);border-radius:8px;margin:10px 0}
.grid{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:12px}
.section,.panel{grid-column:span 12;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px;min-width:0}
.half{grid-column:span 6}
.third{grid-column:span 4}
.zone{border:1px solid var(--line);border-radius:8px;padding:12px;background:var(--panel2);min-width:0}
.zones{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.zone-head{display:flex;justify-content:space-between;gap:8px;align-items:flex-start;margin-bottom:8px}
.badge{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:2px 8px;font-size:12px;white-space:nowrap}
.badge.green{background:var(--green-bg);color:var(--green-text);border-color:var(--green-line)}
.badge.amber{background:var(--amber-bg);color:var(--amber-text);border-color:var(--amber-line)}
.badge.red{background:var(--red-bg);color:var(--red-text);border-color:var(--red-line)}
.badge.gray{background:var(--gray-bg);color:var(--gray-text);border-color:var(--gray-line)}
.metrics{display:grid;gap:7px}
.metric{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;border-top:1px solid var(--line);padding-top:7px;align-items:start}
.metric:first-child{border-top:0;padding-top:0}
.metric .name{font-size:13px;color:var(--muted);font-weight:400;overflow-wrap:anywhere}
.metric .value{font-size:13px;color:var(--text);overflow-wrap:anywhere}
.metric .meta{font-size:12px;color:var(--muted);margin-top:2px}
.metrics-2col{grid-template-columns:1fr 1fr}
.metrics-2col .metric:nth-child(-n+2){border-top:0;padding-top:0}
.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-top:10px}
.kpi{border:1px solid var(--line);border-radius:8px;padding:10px;background:var(--panel2)}
.kpi .label{font-size:11px;color:var(--muted)}
.kpi .value{font-size:22px;font-weight:800;margin-top:2px}
.progress-track{height:8px;background:#2d3348;border-radius:999px;overflow:hidden;margin:10px 0 6px}
.progress-fill{height:100%;background:var(--green);width:0;transition:width 0.6s ease}
.horizon-bar-wrap{position:relative;margin:24px 0 6px}
.horizon-scale{display:flex;justify-content:space-between;font-size:11px;color:var(--muted);margin-top:4px}
.horizon-scale .mark-100{color:var(--green)}
.horizon-now{position:absolute;top:-30px;font-size:15px;font-weight:700;color:var(--text);white-space:nowrap;transform:translateX(-50%)}
.horizon-now::after{content:'↓';display:block;text-align:center;line-height:1.2;font-size:11px;font-weight:400;color:var(--muted)}
.list{display:grid;gap:8px}
.item{border-top:1px solid var(--line);padding-top:8px}
.item:first-child{border-top:0;padding-top:0}
.item-title{font-weight:700;overflow-wrap:anywhere}
.item-text{font-size:13px;color:var(--muted);margin-top:3px;overflow-wrap:anywhere}
.screening{display:grid;grid-template-columns:1.4fr .7fr .8fr .9fr;gap:8px;border-top:1px solid var(--line);padding:8px 0;align-items:start}
.screening:first-child{border-top:0}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.tag{border:1px solid var(--line);background:var(--panel2);color:var(--text);border-radius:999px;padding:4px 8px;font-size:12px}
.ti{display:inline-block;width:1em;margin-right:4px;text-align:center}
.ti-heart::before{content:'♡'}
.ti-bolt::before{content:'⚡'}
.ti-microscope::before{content:'⌕'}
.ti-brain::before{content:'◎'}
.ti-circle::before{content:'○'}
.disclaimer{font-size:12px;color:var(--muted);margin-top:10px}
.brow{display:grid;grid-template-columns:8px minmax(0,200px) minmax(0,1fr) minmax(0,140px) 110px;align-items:baseline;column-gap:14px;padding:9px 0;border-top:1px solid var(--line)}
.brow:first-child{border-top:0;padding-top:2px}
.brow-head .brow-col{font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}
.brow-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0;margin-top:4px}
.brow-name{font-size:13px;color:var(--text)}
.brow-val{font-size:17px;font-weight:700;color:var(--text)}
.brow-unit{font-size:12px;font-weight:400;color:var(--muted);margin-left:3px}
.brow-txt{font-size:13px;color:var(--muted)}
.brow-trend{font-size:11px;color:var(--muted);margin-top:3px}
.brow-ref{font-size:12px;color:var(--muted)}
.brow-date{font-size:12px;color:var(--muted);text-align:right}
.brow-date .fresh{font-size:11px;color:var(--muted);opacity:.7}
.gap-chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.gap-chip{display:inline-flex;align-items:center;gap:5px;font-size:12px;color:var(--muted);background:var(--panel2);border:1px solid var(--line);border-radius:6px;padding:3px 9px}
@media(max-width:900px){
  .top{display:block}
  .goal{text-align:left;margin-top:10px}
  .half,.third{grid-column:span 12}
  .zones{grid-template-columns:1fr}
  .kpis{grid-template-columns:repeat(2,minmax(0,1fr))}
  .metrics-2col{grid-template-columns:1fr}
  .screening{grid-template-columns:1fr}
}
</style>
</head>
<body>
<div class="wrap">
  <div style="display:flex;justify-content:space-between;align-items:baseline">
    <h1>Longevity overview</h1>
    <div style="display:flex;gap:20px;align-items:center">
      <a href="/ui" style="font-size:13px;color:var(--muted);text-decoration:none">← Документы</a>
      <a href="/longevity/checklist" style="font-size:13px;color:var(--muted);text-decoration:none">Чекап-план →</a>
    </div>
  </div>
  <div id="subtitle" style="font-size:12px;color:var(--muted);margin:3px 0 14px">Загрузка...</div>
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:22px;min-height:28px">
    <div id="summary-bar" style="display:none;font-size:13px"></div>
    <div style="display:flex;gap:8px">
      <button id="copyBtn" type="button" style="display:none" onclick="copyForClaude()">Скопировать для Claude ↗</button>
      <button id="reloadBtn" type="button" title="Обновить" style="font-size:15px;padding:5px 9px;line-height:1">↺</button>
    </div>
  </div>
  <div id="notice" class="notice">Загрузка...</div>
  <div id="app" class="grid" style="display:none"></div>
</div>
<script>
const $ = (id)=>document.getElementById(id);
let currentPayload = null;
function apiUrl(path){
  if(location.protocol === 'file:') return 'http://127.0.0.1:8000' + path;
  return path;
}
function e(value){
  return (value ?? '').toString().replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
}
function sendPrompt(text){
  const detail = {text: text || ''};
  window.dispatchEvent(new CustomEvent('sympsense:prompt', {detail}));
  console.log(detail.text);
}
function statusClass(s){ return ['green','amber','red','gray'].includes(s) ? s : 'gray'; }
function statusLabel(s){
  return {green:'под контролем',amber:'пробелы данных',red:'требует внимания',gray:'нет данных'}[s] || s || 'н/д';
}
function shortDate(d){ return d || 'н/д'; }
function daysText(days){
  const n = Number(days);
  if(!Number.isFinite(n)) return 'дата не определена';
  if(n <= 45) return `${n} дн назад`;
  if(n <= 365) return `${Math.round(n/30)} мес назад`;
  return `${Math.round(n/365)} г назад`;
}
function fmtTs(ts){
  if(!ts) return '';
  try{
    const d = new Date(ts);
    if(Number.isNaN(d.getTime())) return String(ts).slice(0, 10);
    return d.toLocaleString('ru-RU', {day:'numeric', month:'long', hour:'2-digit', minute:'2-digit'});
  }catch(e){
    return String(ts).slice(0, 10);
  }
}
function metricValue(m){
  if(m.value === null || m.value === undefined || m.value === '') return 'нет данных';
  const unit = m.unit ? ` ${m.unit}` : '';
  return `${m.value}${unit}`;
}
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
const dotColors = {green:'var(--dot-green)',amber:'var(--dot-amber)',red:'var(--dot-red)',gray:'var(--dot-gray)'};
const WHY = {
  ldl:                  'главный транспортёр холестерина в стенки артерий — основа атеросклероза',
  total_cholesterol:    'суммарная нагрузка липидов; читается в паре с ЛПН и ЛВП',
  blood_pressure:       'первый фактор инсульта и инфаркта; норма <120/80 в любом возрасте',
  homocysteine:         'повреждает эндотелий сосудов; высокий = двойной риск инфаркта и деменции',
  hs_crp:               'маркер хронического воспаления — тихого двигателя старения и атеросклероза',
  hba1c:                'средний сахар за 3 месяца; растёт за годы до постановки диабета',
  fasting_insulin:      'самый ранний сигнал инсулинорезистентности — раньше HbA1c и глюкозы',
  glucose:              'сахар натощак; при резистентности растёт последним из трёх маркеров',
  creatinine_egfr:      'фильтрация почек; незаметно снижается без симптомов годами',
  urea:                 'продукт белкового обмена; показывает, справляются ли почки с выведением',
  ferritin:             'запасы железа и маркер воспаления; избыток = оксидативное повреждение клеток',
  psa:                  'скрининг рака простаты — второго по частоте рака у мужчин; бессимптомен годами',
  tumor_markers:        'онкомаркеры; при росте важна динамика, а не разовое значение',
  dermatoscopy:         'меланома: выживаемость 99% при ранней стадии vs 20% при поздней',
  colonoscopy:          'полипы → рак кишечника; колоноскопия выявляет и удаляет за один визит',
  cognitive_baseline:   'базовый срез памяти и скорости обработки — нужен для отслеживания динамики',
  tsh:                  'регулятор щитовидной железы; дисфункция маскируется под усталость и депрессию',
  vitamin_d:            'скорее гормон, чем витамин; дефицит — иммунитет, онко, деменция, смертность',
  vo2max:               'сильнейший независимый предиктор долголетия — важнее давления и холестерина',
  grip_strength:        'прокси общей мышечной силы; предсказывает смертность сильнее BMI',
  balance:              '10 сек на одной ноге с закрытыми глазами — маркер нейромышечного контроля',
  body_composition:     '% жира важнее веса; саркопения (потеря мышц) — главный риск с 50 лет',
  bone_density:         'плотность костей снижается тихо; перелом шейки бедра часто первый симптом',
  musculoskeletal_status:'подвижность без боли — основа самостоятельности после 70',
  testosterone:         'гормон мышечной массы, энергии, настроения; у мужчин −1% в год с 30',
  monocytes:            'иммунные клетки-«уборщики»; хронически высокие — маркер воспаления',
  eosinophils:          'повышены при аллергии, паразитозах, аутоиммунных состояниях',
  ophthalmology:        'глаукома и отслоение сетчатки развиваются бессимптомно до критической стадии',
  dentistry:            'бактерии полости рта провоцируют системное воспаление и атеросклероз',
  abdominal_ultrasound: 'жировой гепатоз, кисты и ранние опухоли — без симптомов до поздней стадии',
  coronary_calcium_score:'прямой маркер атеросклероза коронарных артерий; предсказывает инфаркт за 10–15 лет',
};
function statusEmoji(s){ return {green:'✅',amber:'⚠️',red:'🔴',gray:'○'}[s]||'○'; }
function cleanDotValue(value){
  let s = String(value || '').replace(/^[↑↓▲▼+]+/, '').trim();
  const cut = s.indexOf('(');
  if(cut > 0 && s.length > 50) s = s.slice(0, cut).trim();
  return s.length > 60 ? s.slice(0, 57) + '…' : s;
}
function metricDotHtml(m){
  const dot = `<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${dotColors[m.status]||dotColors.gray};flex-shrink:0;margin-top:3px"></span>`;
  const hasVal = m.value !== null && m.value !== undefined && m.value !== '';
  const val = hasVal ? `${e(cleanDotValue(m.value))}${m.unit ? ' '+e(m.unit) : ''}` : '';
  const yr = m.event_date ? String(m.event_date).slice(0,4) : null;
  const valDisplay = hasVal
    ? `${val}${yr ? ` <span style="font-size:11px">(${yr})</span>` : ''}`
    : 'нет данных';
  const why = WHY[m.id] || '';
  return `<div class="metric" style="grid-template-columns:1fr auto;align-items:start">
    <div style="display:flex;gap:6px;align-items:flex-start">
      ${dot}
      <div>
        <div class="name" style="color:var(--text)">${e(m.label)}</div>
        ${why ? `<div style="font-size:11px;color:var(--muted);margin-top:2px;line-height:1.4">${e(why)}</div>` : ''}
      </div>
    </div>
    <div style="color:var(--muted);font-size:12px;text-align:right;white-space:nowrap;margin-left:8px">${valDisplay}</div>
  </div>`;
}
function zonePlanHtml(plan){
  if(!plan) return '';
  const refresh = plan.refresh || [];
  const first = plan.first_time || [];
  if(!refresh.length && !first.length) return '';
  let parts = [];
  if(refresh.length) parts.push(`<div style="font-size:11px;display:flex;gap:5px;align-items:flex-start"><span style="color:var(--amber);flex-shrink:0">↻</span><span><span style="color:var(--muted)">обновить: </span>${e(refresh.join(', '))}</span></div>`);
  if(first.length) parts.push(`<div style="font-size:11px;display:flex;gap:5px;align-items:flex-start"><span style="color:var(--muted);flex-shrink:0">+</span><span style="color:var(--muted)">впервые: ${e(first.join(', '))}</span></div>`);
  return `<div style="border-top:1px solid var(--line);margin-top:10px;padding-top:8px;display:flex;flex-direction:column;gap:4px">${parts.join('')}</div>`;
}
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
  const promptText = `${btnLabel} для зоны ${zone.title}`;
  return `<div class="zone">
    <div class="zone-head">
      <div>
        <h3><i class="ti ${icon}" aria-hidden="true"></i> ${e(zone.title)}</h3>
        ${subtitle ? `<div style="font-size:12px;color:var(--muted);margin-top:2px">${e(subtitle)}</div>` : ''}
      </div>
      <span class="badge ${statusClass(zone.status)}">${e(zone.status_label || statusLabel(zone.status))}</span>
    </div>
    <div class="metrics">${(zone.metrics||[]).map(metricDotHtml).join('')}</div>
    ${zonePlanHtml(zone.plan)}
    <button type="button" style="width:100%;margin-top:10px;text-align:center" data-prompt="${e(promptText)}" onclick="sendPrompt(this.dataset.prompt)">${e(btnLabel)} ↗</button>
  </div>`;
}
function metricSection(title, items){
  return `<div class="section half">
    <h2>${e(title)}</h2>
    <div class="metrics">${(items||[]).map(metricHtml).join('') || '<div class="muted">нет данных</div>'}</div>
  </div>`;
}
function physicalHtml(items){
  const icons = {
    vo2max:'ti-run',grip_strength:'ti-barbell',balance:'ti-walk',
    body_composition:'ti-refresh-dot',bone_density:'ti-bone',
    musculoskeletal_status:'ti-activity'
  };
  const tooltips = {
    vo2max:'Сильнейший предиктор долголетия. Норма >50 мл/кг/мин в 30-40 лет',
    grip_strength:'Предиктор общей смертности. Тест: кистевой динамометр',
    balance:'10+ сек на одной ноге с закрытыми глазами — хорошая норма',
    body_composition:'% жира важнее веса. DEXA — золотой стандарт',
    bone_density:'Остеопороз развивается бессимптомно. DEXA-скан с 40 лет при риске',
    musculoskeletal_status:'Подвижность и отсутствие боли — ключ к качеству жизни после 70'
  };
  function physMetricHtml(m){
    const icon = icons[m.id] || 'ti-circle';
    const why = WHY[m.id] || '';
    const dot = `<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${dotColors[m.status]||dotColors.gray};flex-shrink:0;margin-top:3px"></span>`;
    const rawVal = m.value !== null && m.value !== undefined && m.value !== '';
    let val = rawVal
      ? `${e(cleanDotValue(m.value))}${m.unit ? ' '+e(m.unit) : ''}`
      : (m.id === 'vo2max' ? 'не измерялся' : 'нет данных');
    return `<div class="metric" style="grid-template-columns:1fr auto;align-items:start">
      <div style="display:flex;gap:6px;align-items:flex-start">
        ${dot}
        <div>
          <div class="name" style="color:var(--text)"><i class="ti ${icon}" style="font-size:12px;margin-right:3px;color:var(--muted)" aria-hidden="true"></i>${e(m.label)}</div>
          ${why ? `<div style="font-size:11px;color:var(--muted);margin-top:2px;line-height:1.4">${e(why)}</div>` : ''}
        </div>
      </div>
      <div style="color:var(--muted);font-size:12px;text-align:right;white-space:nowrap;margin-left:8px">${val}</div>
    </div>`;
  }
  return `<div class="section" style="grid-column:span 12">
    <h2>Физические показатели</h2>
    <div class="metrics">${(items||[]).map(physMetricHtml).join('') || '<div class="muted">нет данных</div>'}</div>
  </div>`;
}
function actionsHtml(actions){
  const top = (actions||[]).slice(0,3);
  const rest = (actions||[]).slice(3,5);
  function actionItem(x,i){
    return `<div class="item">
      <span class="badge ${statusClass(x.priority)}">${e(statusLabel(x.priority))}</span>
      <div class="item-title" style="font-weight:500;margin-top:4px">${i+1}. ${e(x.title)}</div>
    </div>`;
  }
  return `<div class="section half">
    <h2>Приоритетные действия</h2>
    <div class="list">${top.map(actionItem).join('') || '<div class="muted">нет активных пунктов</div>'}</div>
    ${rest.length?`<details style="margin-top:8px"><summary style="font-size:12px;color:var(--muted);cursor:pointer;list-style:none;user-select:none">▸ ещё ${rest.length} пункта</summary><div class="list" style="margin-top:8px">${rest.map((x,i)=>actionItem(x,i+3)).join('')}</div></details>`:''}
  </div>`;
}
function biochemRowHtml(m){
  const dotColor = dotColors[m.status] || dotColors.gray;
  const rawVal = String(m.value ?? '').replace(/^\(\s*\)\s*/, '').trim();
  const isNumeric = rawVal !== '' && !isNaN(parseFloat(rawVal));
  let valHtml = '';
  if(isNumeric){
    valHtml = `<span class="brow-val">${e(rawVal)}</span>${m.unit ? `<span class="brow-unit">${e(m.unit)}</span>` : ''}`;
  } else if(rawVal){
    valHtml = `<span class="brow-txt">${e(rawVal)}</span>`;
  }
  const trend = (m.trend && m.trend.length > 1)
    ? m.trend.slice().reverse().slice(-5).map(t=>`<span style="color:${t.abnormal?'var(--amber)':'var(--muted)'}">${e(String(t.value||'?'))}</span>`).join(' → ')
    : '';
  const dateStr = m.event_date ? m.event_date.slice(0,7).replace('-','.') : '—';
  const fresh = m.days_since != null ? daysText(m.days_since) : '';
  return `<div class="brow">
    <div class="brow-dot" style="background:${dotColor}"></div>
    <div class="brow-name">${e(m.label)}</div>
    <div>${valHtml}${trend ? `<div class="brow-trend">${trend}</div>` : ''}</div>
    <div class="brow-ref">${m.reference ? e(m.reference) : ''}</div>
    <div class="brow-date">${dateStr}${fresh ? `<br><span class="fresh">${fresh}</span>` : ''}</div>
  </div>`;
}
function biochemHtml(items){
  const visible = (items||[]).filter(m => m.status !== 'gray');
  const hidden = (items||[]).filter(m => m.status === 'gray');
  const header = `<div class="brow brow-head" style="border-top:0;padding-top:0;padding-bottom:8px;border-bottom:1px solid var(--line)">
    <div></div>
    <div class="brow-col">Маркер</div>
    <div class="brow-col">Значение</div>
    <div class="brow-col">Норма</div>
    <div class="brow-col" style="text-align:right">Дата</div>
  </div>`;
  const gapSection = hidden.length ? `<div style="margin-top:14px;padding-top:12px;border-top:1px solid var(--line)">
    <div style="font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px">Ещё не сдавалось</div>
    <div class="gap-chips">${hidden.map(m=>`<span class="gap-chip"><span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--dot-gray)"></span>${e(m.label)}</span>`).join('')}</div>
  </div>` : '';
  return `<div class="section" style="grid-column:span 12">
    <div style="margin-bottom:14px">
      <h2 style="margin:0">Биохимия и гормоны</h2>
      <div style="font-size:11px;color:var(--muted);margin-top:2px">маркеры из анализов крови</div>
    </div>
    ${header}
    <div>${visible.map(biochemRowHtml).join('') || '<div class="muted" style="padding:10px 0">нет данных</div>'}</div>
    ${gapSection}
  </div>`;
}
function screeningStatus(s){
  if(s === 'ok' || s === 'done') return ['green', s === 'done' ? 'пройдено' : 'актуально'];
  if(s === 'upcoming') return ['amber','предстоит'];
  if(s === 'due') return ['amber','нужны данные'];
  if(s === 'overdue') return ['red','просрочено'];
  if(s === 'not_yet_due') return ['gray','не наступило'];
  return ['gray','неизвестно'];
}
function screeningHtml(rows){
  const desc = {
    colonoscopy:'Выявляет полипы и рак кишечника до симптомов. Самый предотвратимый вид рака — при раннем обнаружении лечится в 90%+ случаев.',
    coronary_calcium_score:'КТ-скан сердца. Показывает отложения кальция в коронарных артериях — предсказывает инфаркт за 10-15 лет до события.',
    psa:'Анализ крови на простат-специфический антиген. Скрининг рака простаты — второй по частоте рак у мужчин.',
    dermatoscopy:'Осмотр кожи дерматологом с лупой. Меланома лечится почти в 100% случаев при раннем обнаружении и убивает при позднем.',
    abdominal_ultrasound:'Осмотр печени, желчного пузыря, поджелудочной, почек. Выявляет жировой гепатоз, кисты, ранние опухоли.',
    ophthalmology:'При миопии — контроль прогрессирования и риска отслоения сетчатки. Также глаукома, которая развивается бессимптомно.',
    dentistry:'Здоровье зубов прямо связано с сердечно-сосудистым риском: бактерии полости рта провоцируют системное воспаление и атеросклероз.'
  };
  return `<div class="section" style="grid-column:span 12;margin-top:16px">
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px">
      <h2 style="margin:0">Скрининговый календарь</h2>
      <span style="font-size:12px;color:var(--muted)">обследования по возрасту и частоте</span>
    </div>
    <div class="screening" style="border-top:0;padding-top:0;padding-bottom:8px;border-bottom:1px solid var(--line)">
      <div style="font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.08em">Обследование</div>
      <div style="font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.08em">Последнее</div>
      <div style="font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.08em">Следующее</div>
      <div style="font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.08em">Статус</div>
    </div>
    ${(rows||[]).map(row=>{
      const [cls,label] = screeningStatus(row.status);
      const why = desc[row.screening_id] || '';
      const lastFmt = row.last_date ? row.last_date.slice(0,7).replace('-','.') : 'нет';
      const nextFmt = row.next_due_date ? row.next_due_date.slice(0,7).replace('-','.') : '—';
      return `<div class="screening">
        <div>
          <b>${e(row.title)}</b>
          <div class="muted" style="font-size:11px;margin-top:2px">с ${e(row.start_age)} лет</div>
          ${why?`<div style="font-size:11px;color:var(--muted);margin-top:3px;line-height:1.4">${e(why)}</div>`:''}
        </div>
        <div style="font-size:12px">${lastFmt}</div>
        <div style="font-size:12px">${nextFmt}</div>
        <div><span class="badge ${cls}">${e(label)}</span></div>
      </div>`;
    }).join('') || '<div class="muted">нет данных</div>'}
  </div>`;
}
function gapsHtml(gaps){
  return `<div class="section">
    <h2>Что нужно добавить</h2>
    <div class="tags">${(gaps||[]).slice(0,40).map(g=>`<span class="badge ${statusClass(g.priority)}">${e(g.title)}</span>`).join('') || '<span class="muted">пробелов нет</span>'}</div>
  </div>`;
}
function protocolsHtml(protocols){
  return `<div class="section third">
    <h2>Протоколы</h2>
    <div class="list">${(protocols||[]).map(p=>`<div class="item">
      <div class="item-title">${e(p.name || p.title || p.source_file || 'protocol')}</div>
      <div class="item-text">${e(p.category || '')} ${p.status ? '| '+e(p.status) : ''}</div>
    </div>`).join('') || '<div class="muted">нет protocol_*.json</div>'}</div>
  </div>`;
}
function copyForClaude(){
  if(!currentPayload) return;
  const p = currentPayload;
  const lines = [`Longevity-профиль [${new Date().toISOString().slice(0,7)}]`, ''];
  for(const zone of Object.values(p.horsemen||{})){
    lines.push(`${zone.title} [${zone.status_label || statusLabel(zone.status)}]`);
    for(const m of zone.metrics||[]){
      const yr = m.event_date ? ` (${m.event_date.slice(0,4)})` : '';
      lines.push(`  ${statusEmoji(m.status)} ${m.label}: ${metricValue(m)}${yr}`);
    }
    lines.push('');
  }
  if((p.physical_baselines||[]).length){
    lines.push('Физические показатели');
    for(const m of p.physical_baselines){
      const yr = m.event_date ? ` (${m.event_date.slice(0,4)})` : '';
      lines.push(`  ${statusEmoji(m.status)} ${m.label}: ${metricValue(m)}${yr}`);
    }
    lines.push('');
  }
  const biochem = [...(p.inflammation||[]),...(p.hormones||[])];
  if(biochem.length){
    lines.push('Биохимия / Гормоны');
    for(const m of biochem){
      const yr = m.event_date ? ` (${m.event_date.slice(0,4)})` : '';
      lines.push(`  ${statusEmoji(m.status)} ${m.label}: ${metricValue(m)}${yr}`);
    }
    lines.push('');
  }
  if((p.screening_calendar||[]).length){
    lines.push('Скрининги');
    for(const s of p.screening_calendar){
      const last = s.last_date ? s.last_date.slice(0,7) : 'нет данных';
      const st = s.status==='ok'||s.status==='done' ? '✅' : s.status==='overdue' ? '🔴' : '⚠️';
      lines.push(`  ${st} ${s.title}: последний ${last}`);
    }
  }
  navigator.clipboard.writeText(lines.join('\\n')).then(()=>{
    const btn = $('copyBtn');
    const orig = btn.textContent;
    btn.textContent = 'Скопировано ✓';
    setTimeout(()=>{ btn.textContent = orig; }, 2000);
  }).catch(()=>{ alert('Не удалось скопировать в буфер.'); });
}
function render(payload){
  currentPayload = payload;
  const scope = payload.scope || {};
  const h = payload.horizon || {};
  const _yMin = (scope.date_min||'').slice(0,4);
  const _yMax = (scope.date_max||'').slice(0,4);
  const _period = (_yMin && _yMax && _yMin !== _yMax) ? `${_yMin}–${_yMax}` : (_yMin||'');
  $('subtitle').textContent = `${scope.documents_total||0} документов${_period ? ' · '+_period : ''} · обновлено ${fmtTs(payload.generated_at)}`;
  const allMetrics = [
    ...Object.values(payload.horsemen||{}).flatMap(z=>z.metrics||[]),
    ...(payload.physical_baselines||[]),
    ...(payload.inflammation||[]),
    ...(payload.hormones||[])
  ];
  const gs = allMetrics.filter(m=>m.status==='green').length;
  const ar = allMetrics.filter(m=>m.status==='amber'||m.status==='red').length;
  const grs = allMetrics.filter(m=>m.status==='gray').length;
  const bar = $('summary-bar');
  bar.innerHTML = `<span style="color:var(--green)">●</span> ${gs} в норме &nbsp;<span style="color:var(--amber)">●</span> ${ar} требуют внимания &nbsp;<span style="color:var(--dot-gray)">●</span> ${grs} нет данных`;
  bar.style.display = 'block';
  $('copyBtn').style.display = '';
  const age = Number(h.current_age || 0);
  const target = Number(h.target_age || 100);
  const pct = Math.max(0, Math.min(100, target ? age / target * 100 : 0));
  const ageDisplay = age > 0 ? `${age} <span style="font-size:11px;font-weight:400">лет</span>` : '?';
  const horsemen = payload.horsemen || {};
  const app = $('app');
  app.innerHTML = `
    <div class="section">
      <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px">
        <h2 style="margin:0">Горизонт жизни</h2>
        <span class="muted" style="font-size:12px">оценка на основе текущих маркеров</span>
      </div>
      <div class="horizon-bar-wrap">
        <div class="horizon-now" style="left:${pct}%">${ageDisplay}</div>
        <div class="progress-track"><div class="progress-fill" style="width:${pct}%"></div></div>
        <div class="horizon-scale">
          <span>0</span><span>40</span><span>60</span><span>80</span><span class="mark-100">100</span>
        </div>
      </div>
      <div class="kpis">
        <div class="kpi"><div class="label">история данных</div><div class="value">${e(h.data_years ?? 0)} лет</div></div>
        <div class="kpi"><div class="label">маркеров отслеживается</div><div class="value">${e(h.tracked_markers ?? 0)} / ~40</div></div>
        <div class="kpi"><div class="label">зон под контролем</div><div class="value">${e(h.zones_under_control ?? 0)} из 4</div></div>
        <div class="kpi"><div class="label">действий требуют внимания</div><div class="value" style="color:${(h.actions_need_attention||0)>0?'var(--red)':'var(--text)'}">${e(h.actions_need_attention ?? 0)}</div></div>
      </div>
    </div>
    <div style="grid-column:span 12;font-size:11px;font-weight:600;letter-spacing:0.12em;color:var(--muted);text-transform:uppercase;padding:4px 0">Четыре главных риска</div>
    <div class="section">
      <div class="zones">${Object.values(horsemen).map(zoneHtml).join('')}</div>
    </div>
    ${physicalHtml(payload.physical_baselines || [])}
    ${biochemHtml([...(payload.inflammation || []), ...(payload.hormones || [])])}
    ${screeningHtml(payload.screening_calendar || [])}
  `;
  $('notice').style.display = 'none';
  app.style.display = 'grid';
}
async function load(){
  $('notice').style.display = 'block';
  $('notice').textContent = 'Загрузка...';
  $('app').style.display = 'none';
  try{
    const res = await fetch(apiUrl('/v1/longevity/overview'));
    if(!res.ok) throw new Error(`HTTP ${res.status}`);
    render(await res.json());
  }catch(err){
    $('notice').textContent = `Не удалось загрузить longevity payload: ${err.message}`;
  }
}
$('reloadBtn').addEventListener('click', load);
load();
</script>
</body>
</html>
"""


def build(project_root: Path | None = None) -> Path:
    root = (project_root or PROJECT_ROOT).resolve()
    out = root / "data/derived/reports/longevity_v1.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    build_longevity_overview(project_root=root, write_report=True)
    out.write_text(_html(), encoding="utf-8")
    return out


def main() -> None:
    path = build()
    print(str(path).replace("\\", "/"))


if __name__ == "__main__":
    main()
