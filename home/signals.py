from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InOut, DSCMaster

# @receiver(post_save, sender=InOut)
# def update_in_out_status(sender, instance, **kwargs):
#     """
#     Update the in_out_status field of the DSCMaster model whenever
#     an InOut record's direction is changed.
#     """
#     if instance.direction == 'incoming':
#         in_out_status = 0  # Incoming
#     elif instance.direction == 'outgoing':
#         in_out_status = 1  # Outgoing
#     else:
#         in_out_status = None  # Handle unexpected cases

#     # Fetch the related DSCMaster record and update its in_out_status
#     dsc_master = instance.dsc_number  # Corrected field name
#     if dsc_master:
#         dsc_master.in_out_status = in_out_status
#         dsc_master.save()
