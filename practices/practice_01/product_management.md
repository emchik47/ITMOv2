# Use cases и user stories

## Use cases
- UC1: Ревью одного PR по diff → получить описание, риски, проверки.
- UC2: Повторный запуск с master prompt → улучшенные выводы.

```gherkin
Feature: Review assistant
  Scenario: Analyze diff and propose risks
    Given a pull request diff is provided
    When the assistant analyzes the diff
    Then it returns a short change summary
    And up to three risks with file and line references and evidence
    And a list of checks to run
```

## User stories
- Как ревьюер, хочу видеть ссылки и доказательства, чтобы быстро проверить риск.
- Как студент, хочу воспроизводимые шаги запусков P1-01 и P1-02.

## Как использовали AI

Тип: формулировка сценариев. См. prompts.md (P1-setup).
