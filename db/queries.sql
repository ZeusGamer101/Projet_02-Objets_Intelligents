-- 1) 10 dernières mesures
SELECT id, ts_utc, device, topic, value, unit
FROM telemetry
ORDER BY id DESC
LIMIT 10;

-- 2) 10 derniers événements
SELECT id, ts_utc, device, topic, payload
FROM events
ORDER BY id DESC
LIMIT 10;

-- 3) Compter le volume
SELECT (SELECT COUNT(*) FROM telemetry) AS n_telemetry,
(SELECT COUNT(*) FROM events) AS n_events;