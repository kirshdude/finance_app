import os

SERVICE_ACCOUNT_JSON = '''{
  "type": "service_account",
  "project_id": "personal-finance-401213",
  "private_key_id": "1755cdbadbd84880381aa84e83d1041d2c896817",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCwdFafmP23XAuM\nqmm2rfwwS2JXggDtGAjDj4RRY3myGRdgDJ81Qi5eIns6PRPbEO2x4BEAQMK/nh71\ngVIubo5E22+ESXNplZhA7NA9CZsBaAgy+RaE7dFiP2ZSKEcb/ei26rJou0djNhxZ\n1qVTSQM6hwRh162eZshvj6ThJuYzGfvwZ48VJD8T0kujO8JX9SWP22pvpy4IUO8U\npHNjrqA7Dh9huOiiJ9pd0Ewe/8R0hoAujI9Ysq46C6AxzXVI8uagvMeDRTVjbQnj\n3paYuvWVZWpne+xNJENFUhhs0pMiJ7rcVLsOFbZ3yClfVSqfL9PGR2lXjnyWA897\nupHXJdXhAgMBAAECggEAAeiwSze3fvVS9qmdTSmisc8O+E1ivy3kYmE6GDtQRLn6\nw8I/Mq9Nmx0aYi3o+hS7zZHT/UG2GaaXRSaqAfCWP250TWUSB5FjvUgSlKZ289Px\nSsPhF30PJ9XxwG/JHSdpDhmJ5pIoGo2qTtqAnV8L1uVBCeHwcedAwdw292yZTvIz\na0QWH/wZ4MraCXpVtW+Z4SS6e3Xk3tBnsvrjwz7nsv1T9TDkqy3Jx65LYeT2dYX8\njyDCpurCu4FGIDS92QFYJdPF0rfxQJ0PEy/lFP+Q+GoVTURNkMj5JKp9ufIp6kui\nFplna/pmg9n4jWsyFO17m2HTcgszSHwNBHyBxm0LZQKBgQDV88Kx/RtwZV1m5E96\nGhhAyiij2ra1phgD5ycKea182k6iiqVgr2twkLy4oNi3Dsh7mS057xLeJD7fbhtW\nMM6lrOhUcSIJ+psIs/ljsDRJY/OsewN+IilVRrditSUOlm+LNqhdPAXF/Q9G7AY6\nXOvSub9RWRFEJrwrl9a5TlUlGwKBgQDTIgNSxxKbFi6LzZe5VwaqAn//7ItAKW9B\nVbeiov5E/uNAtv6juYWLko5RWTLXD6Vva19pv8V9qjK1Zd1uQq3EUhkt7cD377+z\n1DGmIPry+GAm3ogEV47+u/AkaKSKhKk+XgDZh77hlaCMA3ePFgLRb6uKgD3qMiNa\nCZz7OLjsswKBgFrUvPBxgyepcQjQnsk4sNk4uh4uKWle1U064kE5PSUHTWEGOYWd\nk6BbYjOD3d2Bgi2u7xtsWvdCLgsPJL3nxKNjj9LhoNDZut3sAlGHKfuKWpX8N5Ri\nDmgsuIhIXS4fQcW5c6r5Y34VnFnAtDgs4NU6lHWFuaXUSAi90qQjFFTHAoGAKBEb\nWlknAcFq4eMJOQX34MmKqvGj13BFibuPltChukw4qi5QEpgBbORKF8v6pu90MLnK\nqJHZE6j56IzFQchrm4cM+jdVWHfqBGFvbpxxoyxZaubuHwzSuSrHPtGQ8CyOxaQn\nOyDUq5CuoAOEa+X8cOxlPGpr1YbgSJTscoxoI5sCgYAnrIpPzL4Exg4zDJRIYrOe\n4flrVdNp32G8BrU5XZ2Vr9d6VHteKO3+39AYswsykWWxbrJCjmFsVHxRdXLK97LV\nRtwltd3L5fqHOk+fZD5kzCCwdisrI2ZbEdhq1nN0UB3m5sBK7cSDf7Afvtb0nHeu\nuM2tpu/2Nr4I/kqhFd1tdA==\n-----END PRIVATE KEY-----\n",
  "client_email": "personal-finance-big-query@personal-finance-401213.iam.gserviceaccount.com",
  "client_id": "105596524279572202054",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/personal-finance-big-query%40personal-finance-401213.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
'''

OPEN_AI_MODEL = "gpt-3.5-turbo" #"gpt-4o"
PROJECT_ID = 'personal-finance-401213'