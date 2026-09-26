# ADR: Структура помощника ревью PR

Решение: использовать master prompt с Context Pack для анализа diff и генерации проверяемых выводов. Архитектурно разделить рабочий агент (Build) и тестовые запуски без инструментов.

## Архитектурная схема

```mermaid
sequenceDiagram
  participant User as Ревьюер
  participant Build as OpenCode Build
  participant Test as Тестовый агент (no tools)
  User->>Build: Подготовь артефакты и запуски
  Build->>Test: P1-01: diff, zero-shot
  Test-->>Build: Ответ P1-01
  Build->>Build: Сбор контекста, master prompt
  Build->>Test: P1-02: diff + master prompt
  Test-->>Build: Ответ P1-02
  Build-->>User: Сравнение и журнал
```

## Как использовали AI

Тип: фиксация архитектуры. См. prompts.md (P1-setup).
