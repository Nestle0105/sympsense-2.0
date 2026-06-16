# Правка: метрики в карточке "Сердечно-сосудистые"

Файл для изменений: `apps/cli/src/sympsense/longevity_overview.py`

---

## Что изменить

В функции `build_longevity_overview`, в блоке `horsemen["cardiovascular"]`, заменить текущий список метрик на следующий:

**Было (5 метрик):**
```python
_metric("ldl", "ЛПНП", [...], ...),
_metric("apob", "ApoB", [...], ...),           # убрать
_metric("total_cholesterol", "Общий холестерин", [...], ...),
_metric("blood_pressure", "АД", [], ...),
_empty_marker("coronary_calcium_score", "Кальциевый скоринг", ...),
```

**Стало (5 метрик):**
```python
_metric("ldl", "ЛПНП", ["лпнп", "ldl", "низкой плотности"], labs=labs, checkups=checkups, as_of=as_of),
_metric("total_cholesterol", "Общий холестерин", ["холестерин общий", "общий холестерин"], labs=labs, checkups=checkups, as_of=as_of),
_condition_marker(
    "varicose",
    "Варикоз / вены",
    ["варикоз", "хвн", "варикозн", "венозн"],
    condition_rows=condition_rows,
    current_state=current_state if isinstance(current_state, dict) else None,
    problem_list=problem_list if isinstance(problem_list, dict) else None,
    as_of=as_of,
),
_empty_marker("coronary_calcium_score", "Кальциевый скоринг", source_kind="screening_calendar"),
_metric("blood_pressure", "АД, ЧСС покоя", ["артериальное давление", "ад", "blood pressure", "чсс"], labs=[], checkups=checkups, as_of=as_of),
```

## Суть изменений

1. **Убрать ApoB** — анализ редко сдаётся, всегда будет "нет данных", занимает место
2. **Добавить "Варикоз / вены"** — у пользователя есть ХВН (хроническая венозная недостаточность), данные есть в `condition_mentions_v1.ndjson` по терминам "варикоз", "хвн"
3. **Переименовать "АД" → "АД, ЧСС покоя"** — более точная метка
4. **Поменять порядок**: ЛПНП → Холестерин → Варикоз → Кальций → АД

Логика `_condition_marker` уже написана и используется в других зонах — просто добавить вызов с нужными алиасами.
