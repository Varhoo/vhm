from django.dispatch import Signal

vhm_project_update = Signal(providing_args=['instance'])
vhm_account_update = Signal(providing_args=['instance'])
vhm_process_update = Signal(providing_args=['instance'])

vhm_accont_delete = Signal(providing_args=['instance'])
