# 🤝 Contributing to YoVPN WebApp

Спасибо за интерес к проекту! Мы приветствуем любые contributions. 🎉

---

## 📋 Содержание

- [Code of Conduct](#code-of-conduct)
- [Как помочь](#как-помочь)
- [Процесс разработки](#процесс-разработки)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)
- [Bug Reports](#bug-reports)
- [Feature Requests](#feature-requests)

---

## 📜 Code of Conduct

### Наши стандарты

✅ **Делайте:**
- Будьте уважительны и профессиональны
- Приветствуйте новичков
- Принимайте конструктивную критику
- Фокусируйтесь на том, что лучше для сообщества

❌ **Не делайте:**
- Trolling, оскорбления, личные атаки
- Публикация личной информации других людей
- Harassment любого рода
- Unprofessional conduct

---

## 🎯 Как помочь

### Для новичков

Ищите issues с лейблами:
- `good first issue` - простые задачи для начала
- `help wanted` - нужна помощь сообщества
- `documentation` - улучшение документации

### Типы contributions

1. **Bug Fixes** - исправление ошибок
2. **Features** - новый функционал
3. **Documentation** - улучшение docs
4. **Tests** - написание тестов
5. **Refactoring** - улучшение кода
6. **Design** - UI/UX улучшения
7. **Translations** - переводы (будущее)

---

## 🔨 Процесс разработки

### 1. Fork репозитория

```bash
# Клонируйте ваш fork
git clone https://github.com/YOUR-USERNAME/yovpn.git
cd yovpn

# Добавьте upstream
git remote add upstream https://github.com/original/yovpn.git
```

### 2. Создайте ветку

```bash
# Обновите main
git checkout main
git pull upstream main

# Создайте feature ветку
git checkout -b feature/amazing-feature

# Или для bug fix
git checkout -b fix/bug-description
```

**Naming Convention:**
- `feature/feature-name` - новый функционал
- `fix/bug-name` - исправление бага
- `docs/description` - документация
- `refactor/description` - рефакторинг
- `test/description` - тесты

### 3. Разработка

#### Установка зависимостей

```bash
# Frontend
cd webapp
npm install

# Backend
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Запуск dev серверов

```bash
# Используйте скрипт
./start-webapp.sh

# Или вручную (2 терминала)
cd webapp && npm run dev
cd api && python -m app.main
```

#### Внесение изменений

- Следуйте [Code Style](#code-style)
- Пишите тесты для нового функционала
- Обновляйте документацию при необходимости
- Делайте atomic commits

### 4. Commit

Мы используем **Conventional Commits**:

```bash
# Формат
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat` - новый функционал
- `fix` - исправление бага
- `docs` - документация
- `style` - форматирование (без изменения кода)
- `refactor` - рефакторинг
- `test` - добавление тестов
- `chore` - обновление build tools, etc.

**Примеры:**

```bash
# Простой feature
git commit -m "feat(platform-selector): add Linux platform support"

# Bug fix с описанием
git commit -m "fix(api): correct HMAC validation for long init_data

The previous implementation failed when init_data exceeded 1024 chars.
This commit fixes the buffer size and adds proper error handling.

Fixes #123"

# Breaking change
git commit -m "feat(api)!: change subscription response format

BREAKING CHANGE: subscription_uri is now an object with { uri, qr_code }
instead of a plain string. Update frontend to use response.uri."
```

### 5. Push и Pull Request

```bash
# Push в ваш fork
git push origin feature/amazing-feature

# Откройте Pull Request на GitHub
```

---

## 🎨 Code Style

### Frontend (TypeScript/React)

#### ESLint + Prettier

```bash
# Установка
npm install --save-dev eslint prettier

# Проверка
npm run lint

# Автофикс
npm run lint:fix

# Форматирование
npm run format
```

#### Правила

```typescript
// ✅ Хорошо
interface UserProfile {
  userId: number;
  username: string;
  isActive: boolean;
}

const getUserProfile = async (userId: number): Promise<UserProfile> => {
  const response = await api.get(`/users/${userId}`);
  return response.data;
};

// ❌ Плохо
interface user_profile {
  user_id: number;
  user_name: string;
}

function get_user_profile(id) {
  return api.get('/users/' + id).then(r => r.data);
}
```

**Naming:**
- `PascalCase` - компоненты, типы, интерфейсы
- `camelCase` - переменные, функции
- `UPPER_SNAKE_CASE` - константы
- `kebab-case` - файлы CSS

**Components:**

```typescript
// ✅ Functional components с TypeScript
interface Props {
  title: string;
  onSelect: (id: number) => void;
}

export default function PlatformCard({ title, onSelect }: Props) {
  const [isHovered, setIsHovered] = useState(false);
  
  return (
    <div 
      className="platform-card"
      onMouseEnter={() => setIsHovered(true)}
    >
      {title}
    </div>
  );
}
```

### Backend (Python)

#### Black + isort + flake8

```bash
# Установка
pip install black isort flake8

# Форматирование
black .
isort .

# Проверка
flake8 .
```

#### Правила

```python
# ✅ Хорошо
from typing import Optional

from pydantic import BaseModel


class UserProfile(BaseModel):
    user_id: int
    username: str
    is_active: bool


async def get_user_profile(user_id: int) -> Optional[UserProfile]:
    """Get user profile by ID."""
    user = await db.users.find_one({"id": user_id})
    if not user:
        return None
    return UserProfile(**user)


# ❌ Плохо
def getUserProfile(id):
    user = db.users.find_one({'id': id})
    return user
```

**Naming:**
- `snake_case` - всё (функции, переменные, файлы)
- `PascalCase` - классы
- `UPPER_SNAKE_CASE` - константы

**Type Hints:**

```python
# Всегда используйте type hints
def process_data(
    data: dict[str, Any],
    user_id: int,
    options: Optional[dict] = None
) -> tuple[bool, str]:
    """Process user data."""
    # ...
    return True, "Success"
```

### Git

**Branch naming:**
```bash
feature/platform-linux-support
fix/api-cors-headers
docs/update-readme
refactor/cleanup-unused-imports
test/add-unit-tests
```

**Commit messages:**
```bash
feat(webapp): add dark mode toggle
fix(api): correct timezone handling
docs: update deployment guide
refactor: simplify state management
test: add integration tests for activation
```

---

## 🔄 Pull Request Process

### 1. Pre-PR Checklist

Перед созданием PR убедитесь:

- [ ] Код соответствует style guide
- [ ] Все тесты проходят (`npm test`, `pytest`)
- [ ] Линтеры не выдают ошибок
- [ ] Документация обновлена
- [ ] Коммиты следуют Conventional Commits
- [ ] Нет конфликтов с main
- [ ] PR описание заполнено

### 2. PR Template

```markdown
## Описание
Краткое описание изменений.

## Тип изменения
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change
- [ ] Documentation update

## Как протестировать
1. Шаг 1
2. Шаг 2
3. Проверить результат

## Checklist
- [ ] Код соответствует style guide
- [ ] Self-review выполнен
- [ ] Комментарии добавлены где нужно
- [ ] Документация обновлена
- [ ] Нет новых warnings
- [ ] Тесты добавлены/обновлены
- [ ] Все тесты проходят

## Screenshots (если применимо)
![Before](link)
![After](link)

## Связанные issues
Closes #123
Related to #456
```

### 3. Code Review Process

После создания PR:

1. **Automated checks** запустятся автоматически
   - Linting
   - Tests
   - Build

2. **Code review** от maintainers
   - Обычно в течение 2-3 дней
   - Могут попросить внести изменения

3. **Обсуждение**
   - Отвечайте на комментарии
   - Вносите правки по запросу
   - Push новые коммиты в ту же ветку

4. **Merge**
   - После approval PR будет смержен
   - Squash merge для чистой истории

---

## 🐛 Bug Reports

### Как создать хороший Bug Report

**Используйте template:**

```markdown
## Описание бага
Четкое описание того, что не работает.

## Шаги для воспроизведения
1. Перейти на '...'
2. Нажать на '...'
3. Увидеть ошибку

## Ожидаемое поведение
Что должно было произойти.

## Актуальное поведение
Что произошло на самом деле.

## Screenshots
Если применимо, добавьте скриншоты.

## Окружение
- OS: [e.g., macOS 14.0]
- Browser: [e.g., Chrome 120]
- Node.js version: [e.g., 18.17.0]
- WebApp version: [e.g., 1.0.0]

## Дополнительная информация
- Console errors
- Network errors
- Логи
```

### Labels для Issues

- `bug` - что-то не работает
- `enhancement` - новый функционал
- `documentation` - улучшение docs
- `good first issue` - для новичков
- `help wanted` - нужна помощь
- `question` - вопрос
- `wontfix` - не будет исправлено
- `duplicate` - дубликат

---

## 💡 Feature Requests

### Template

```markdown
## Описание фичи
Что вы хотите добавить?

## Проблема
Какую проблему это решает?

## Предлагаемое решение
Как это должно работать?

## Альтернативы
Какие альтернативные решения вы рассматривали?

## Дополнительная информация
Screenshots, mockups, etc.
```

---

## 🧪 Testing

### Frontend Tests

```bash
cd webapp

# Unit tests
npm test

# E2E tests (если есть)
npm run test:e2e

# Coverage
npm run test:coverage
```

### Backend Tests

```bash
cd api

# Run tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test
pytest tests/test_api.py::test_get_subscription
```

---

## 📚 Документация

### Когда обновлять docs

Обновляйте документацию при:

- Добавлении новой фичи
- Изменении API
- Изменении конфигурации
- Добавлении новой платформы
- Изменении deployment процесса

### Где обновлять

- `README.md` - общий обзор
- `WEBAPP_GUIDE.md` - подробное руководство
- `DEPLOYMENT.md` - деплой инструкции
- `ANIMATIONS.md` - анимации
- `webapp/README.md` - frontend docs
- `api/README.md` - backend docs

---

## ❓ Вопросы?

Если у вас есть вопросы:

1. Проверьте [документацию](./README.md)
2. Поищите в [Issues](https://github.com/yourusername/yovpn/issues)
3. Создайте новый Issue с лейблом `question`
4. Спросите в Telegram: [@yovpn_dev](https://t.me/yovpn_dev)

---

## 🙏 Благодарности

Все contributors будут добавлены в [Contributors](https://github.com/yourusername/yovpn/graphs/contributors).

Спасибо за ваш вклад! 🎉

---

**Happy Contributing! 🚀**
