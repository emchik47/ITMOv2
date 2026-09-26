# Журнал экспериментов Практики 2

Файл ведёт OpenCode по вашим запросам. Агент записывает фактические результаты экспериментов и вносит изменения в связанные файлы. Свою оценку сообщайте ему в чате; вручную заполнять шаблон не нужно.

- Выбранный слабый артефакт Практики 1: practices/practice_01/prompts.md (Master Prompt v1)
- Что в нём нужно улучшить: добавить калибрующие примеры (few-shot), уточнить обязательность evidence и воспроизводимых проверок, зафиксировать формат вывода.
- Как поймём, что изменение полезно: ответы становятся более доказательными (каждый риск со ссылкой и цитатой), формат соблюдается без отклонений; make step2 проходит; визуальная проверка показывает наличие примеров и уточнений в Master Prompt.

| Техника | Файл эксперимента | Изменённый файл Практики 1 | Конкретное изменение | Проверка | Что отклонили |
|---|---|---|---|---|---|
| Few-shot | [`few_shot/experiment.md`](few_shot/experiment.md) | practices/practice_01/prompts.md (Master Prompt v1) | Добавлены few-shot примеры «Хороший» и «Плохой»; уточнены поля evidence/check | make step2 проходит; визуально примеры на месте | Отклонено расширение >3 рисков |
| R.C.T.F. | [`rctf/experiment.md`](rctf/experiment.md) | practices/practice_01/prompts.md (Master Prompt v1) | Добавлен блок Role/Context/Task/Format в начале мастер‑промпта | make step2; визуальная проверка блока RCTF | Отклонены внешние источники |
| Chain of Verification | [`chain_of_verification/experiment.md`](chain_of_verification/experiment.md) | practices/practice_01/prompts.md (Master Prompt v1) | Уточнены требования к evidence: hunk, точная строка, побайтное совпадение | make step2; визуальная проверка уточнений | Отклонены ссылки на произвольные строки |
| Tree of Thoughts | [`tree_of_thoughts/experiment.md`](tree_of_thoughts/experiment.md) | practices/practice_01/prompts.md (Master Prompt v1) | Подтверждён выбор формата evidence: побайтная цитата + hunk + строка | make step2; визуальная проверка evidence | Отклонены альтернативы без hunk/номеров |
| RAG | [`rag/experiment.md`](rag/experiment.md) | practices/practice_01/prompts.md (Master Prompt v1) | Добавлены ссылки на внутренние источники (README/context) как основания | make step2; визуальная проверка ссылок | Отклонены внешние источники |
| ReAct | [`react/experiment.md`](react/experiment.md) | practices/practice_01/prompts.md (Master Prompt v1) | Добавлены шаги ReAct: перечисление hunks, подтверждение цитат перед рисками | make step2; визуальная проверка шагов | Отклонены непроверенные кандидаты |
