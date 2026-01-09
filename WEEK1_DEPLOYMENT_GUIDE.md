# НЕДЕЛЯ 1: ДЕТАЛЬНЫЙ ГАЙД РАЗВЕРТЫВАНИЯ

**Дата начала**: 10 января 2026, 09:00 MSK
**Статус**: PRODUCTION DEPLOYMENT WEEK
**Целевая дата запуска**: 14 января 2026, 11:00 MSK

---

## ДЕНЬ 1 (10 ЯНВАРЯ) - ИНФРАСТРУКТУРА И ДОМЕН

### ЭТАП 1: РЕГИСТРАЦИЯ ДОМЕНА (09:00-11:00)

#### Шаг 1.1: Зарегистрировать домен

```bash
# Вариант A: Cloudflare (РЕКОМЕНДУЕТСЯ для России)
Вебсайт: https://www.cloudflare.com/
Домен: mismatch-recruiter.ru
Желательная длительность: 2 года
Стоимость: ~$0.88-1.50 в год
Бенефиты:
  - DDoS protection (бесплатно)
  - WAF (Web Application Firewall)
  - DNS hosting
  - SSL/TLS termination
  - Faster performance

# Вариант B: Beget (для России)
Вебсайт: https://beget.com/ru/
Домен: mismatch-recruiter.ru
Стоимость: 149-249 руб в год
Бенефиты:
  - Русская поддержка
  - Хостинг опции
  - Email hosting
```

**Действие**: Выполнить регистрацию на выбранной платформе

#### Шаг 1.2: Настроить DNS записи в Cloudflare

```bash
# Войти в Cloudflare dashboard
# https://dash.cloudflare.com/

# Добавить DNS records:

# 1. A Record (основной домен)
Тип: A
Имя: mismatch-recruiter.ru
IPv4 адрес: [YOUR_PRODUCTION_IP]
TTL: Auto
Proxied: Yes (для защиты от DDoS)

# 2. CNAME для приложения
Тип: CNAME
Имя: app
Target: mismatch-recruiter.ru
TTL: Auto
Proxied: Yes

# 3. CNAME для API
Тип: CNAME
Имя: api
Target: mismatch-recruiter.ru
TTL: Auto
Proxied: Yes

# 4. CNAME для www
Тип: CNAME
Имя: www
Target: mismatch-recruiter.ru
TTL: Auto
Proxied: Yes

# 5. MX Record (если нужна почта)
Тип: MX
Приоритет: 10
Значение: mail.mismatch-recruiter.ru

# Проверить распространение
nslookup app.mismatch-recruiter.ru
dig app.mismatch-recruiter.ru
```

**Статус**: PENDING IP ADDRESS (нужно получить после provisioning)

#### Шаг 1.3: Включить Cloudflare защиту

```bash
# В Cloudflare dashboard:

1. SSL/TLS Mode: Full (strict)
   - Требует valid SSL на origin
   - Лучше всего для production

2. Включить HSTS
   - Max Age: 31536000 (1 год)
   - Include subdomains: YES
   - Preload: YES

3. Настроить WAF (Web Application Firewall)
   - Enable OWASP ModSecurity Core Rule Set
   - Sensitivity: Medium

4. Rate Limiting
   - 20 requests per 10 seconds
   - Block action

5. Browser Caching
   - Browser Cache TTL: 30 minutes
```

**Сложность**: СРЕДНЯЯ | **Время**: 45 минут

---

### ЭТАП 2: PROVISIONING PRODUCTION СЕРВЕРОВ (11:00-18:00)

#### Шаг 2.1: Выбрать хостинг провайдера

```
ОПЦИЯ A: Amvera Cloud (https://amvera.ru) - РЕКОМЕНДУЕТСЯ
✓ Российский провайдер
✓ Локальное размещение данных (GDPR compliant)
✓ Хорошая поддержка на русском
✓ Адекватные цены

Структура:
├─ 2x App Servers (Ubuntu 22.04 LTS)
│  ├─ CPU: 4 cores
│  ├─ RAM: 8GB
│  ├─ Storage: 100GB SSD
│  └─ Cost: ~$30/month each = $60/month
│
├─ 1x Database Server (Ubuntu 22.04 LTS)
│  ├─ CPU: 8 cores
│  ├─ RAM: 16GB
│  ├─ Storage: 500GB SSD
│  └─ Cost: ~$80/month
│
└─ 1x Cache Server (Ubuntu 22.04 LTS)
   ├─ CPU: 2 cores
   ├─ RAM: 4GB
   ├─ Storage: 50GB SSD
   └─ Cost: ~$20/month

Итого: ~$160/месяц


ОПЦИЯ B: AWS EC2 (https://aws.amazon.com)
✓ Глобальная инфраструктура
✓ Масштабируемость
✓ Высокая надежность
⚠ Может быть дороже (~$250/месяц)
⚠ Сложнее настраивать


ОПЦИЯ C: DigitalOcean (https://www.digitalocean.com)
✓ Простота использования
✓ Хорошая документация
✓ Экономно (~$100/месяц)
⚠ Может быть медленнее
```

**Рекомендация**: Amvera Cloud для России

#### Шаг 2.2: Создать VPC и Security Groups

```bash
# На Amvera или выбранном провайдере:

1. Создать Virtual Private Cloud (VPC)
   Name: mismatch-recruiter-vpc
   CIDR: 10.0.0.0/16

2. Создать subnets
   Public Subnet 1: 10.0.1.0/24 (Zone 1)
   Public Subnet 2: 10.0.2.0/24 (Zone 2)
   Private Subnet:  10.0.3.0/24 (Database)

3. Создать Security Group: mismatch-sg
   Inbound Rules:
   - SSH (22): от вашего IP
   - HTTP (80): от 0.0.0.0/0
   - HTTPS (443): от 0.0.0.0/0
   - PostgreSQL (5432): от 10.0.0.0/16 (internal)
   - Redis (6379): от 10.0.0.0/16 (internal)
   
   Outbound Rules:
   - All traffic: allow
```

#### Шаг 2.3: Запустить серверы

```bash
# Для каждого сервера:

#!/bin/bash
# Пример для Amvera или DigitalOcean CLI

# 1. APP SERVER 1
amvera-cli vm create \
  --name mismatch-app-1 \
  --image ubuntu-22.04-lts \
  --size 4-8gb-cpu \
  --region msk \
  --key-pair mismatch-key \
  --subnet 10.0.1.0/24

# 2. APP SERVER 2
amvera-cli vm create \
  --name mismatch-app-2 \
  --image ubuntu-22.04-lts \
  --size 4-8gb-cpu \
  --region msk \
  --key-pair mismatch-key \
  --subnet 10.0.2.0/24

# 3. DATABASE SERVER
amvera-cli vm create \
  --name mismatch-db \
  --image ubuntu-22.04-lts \
  --size 8-16gb-cpu \
  --region msk \
  --key-pair mismatch-key \
  --subnet 10.0.3.0/24 \
  --volume 500gb-ssd

# 4. CACHE SERVER
amvera-cli vm create \
  --name mismatch-cache \
  --image ubuntu-22.04-lts \
  --size 2-4gb-cpu \
  --region msk \
  --key-pair mismatch-key \
  --subnet 10.0.3.0/24
```

**Статус**: Дождаться создания серверов (обычно 5-10 минут)

#### Шаг 2.4: Получить IP адреса

```bash
# После создания серверов получить их IP адреса

# Пример вывода:
APP_SERVER_1_IP=192.168.1.10
APP_SERVER_2_IP=192.168.1.11
DB_SERVER_IP=192.168.1.20
CACHE_SERVER_IP=192.168.1.21
LOAD_BALANCER_IP=192.168.1.5  # или использовать DNS

# Сохранить в файл для использования
cat > servers.conf << 'SERVERS'
APP_SERVER_1_IP=<actual_ip>
APP_SERVER_2_IP=<actual_ip>
DB_SERVER_IP=<actual_ip>
CACHE_SERVER_IP=<actual_ip>
DOMAIN=app.mismatch-recruiter.ru
SERVERS

# ⚠️ ВАЖНО: Обновить A record в Cloudflare с основным IP
```

**Сложность**: СРЕДНЯЯ | **Время**: 1 час 30 минут

---

## ДЕНЬ 2 (11 ЯНВАРЯ) - SSL И ОСНОВНАЯ КОНФИГУРАЦИЯ

### ЭТАП 3: SSL СЕРТИФИКАТЫ (09:00-12:00)

#### Шаг 3.1: Установить Certbot

```bash
# На каждом APP SERVER

ssh admin@APP_SERVER_1_IP

# Обновить систему
sudo apt-get update
sudo apt-get upgrade -y

# Установить Certbot
sudo apt-get install -y certbot python3-certbot-nginx python3-certbot-dns-cloudflare

# Создать Cloudflare API токен
# 1. Логин в Cloudflare
# 2. Account > API Tokens > Create Token
# 3. Permissions: Zone.Zone:Read, Zone.DNS:Edit
# 4. Скопировать токен

# Создать конфиг файл
mkdir -p ~/.cloudflare
cat > ~/.cloudflare/cloudflare.ini << 'CLOUDFLARE'
dns_cloudflare_api_token = <YOUR_API_TOKEN>
CLOUDFLARE

chmod 600 ~/.cloudflare/cloudflare.ini
```

#### Шаг 3.2: Получить SSL сертификат

```bash
# Запросить сертификат для всех доменов

sudo certbot certonly \
  --dns-cloudflare \
  --dns-cloudflare-credentials ~/.cloudflare/cloudflare.ini \
  --agree-tos \
  --no-eff-email \
  --email admin@mismatch-recruiter.ru \
  -d mismatch-recruiter.ru \
  -d app.mismatch-recruiter.ru \
  -d api.mismatch-recruiter.ru

# Проверить установку
sudo certbot certificates

# Вывод должен быть:
# Certificate Name: mismatch-recruiter.ru
# Domains: mismatch-recruiter.ru, app.mismatch-recruiter.ru, api.mismatch-recruiter.ru
# Path: /etc/letsencrypt/live/mismatch-recruiter.ru/
```

#### Шаг 3.3: Настроить автоматическое обновление

```bash
# Включить systemd timer для автоматического обновления

sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Проверить статус
sudo systemctl status certbot.timer

# Тестировать обновление
sudo certbot renew --dry-run

# Должно быть:
# Cert not yet due for renewal
```

**Сложность**: СРЕДНЯЯ | **Время**: 1 час

---

