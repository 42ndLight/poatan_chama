from celery.schedules import crontab


app.conf.beat_schedule = {
    'check-payout-cycles': {
        'task': 'payouts.tasks.check_payout_cycles',
        'schedule': crontab(hour=0, minute=0),
    },
}