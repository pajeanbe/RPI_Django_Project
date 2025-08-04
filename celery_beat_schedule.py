from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'collect-metrics': {
        'task': 'monitoring.tasks.collect_metrics',
        'schedule': 30.0,  # Every 30 seconds
    },
    'cleanup-old-metrics': {
        'task': 'monitoring.tasks.cleanup_old_metrics',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
}