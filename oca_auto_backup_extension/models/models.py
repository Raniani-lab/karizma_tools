# © 2004-2009 Tiny SPRL (<http://tiny.be>).
# © 2015 Agile Business Group <http://www.agilebg.com>
# © 2016 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import os
import shutil
import traceback
from contextlib import contextmanager
from datetime import datetime, timedelta
from glob import iglob
from google.cloud import storage

from odoo import _, api, exceptions, fields, models, tools
from odoo.service import db

_logger = logging.getLogger(__name__)
try:
    import pysftp
except ImportError:  # pragma: no cover
    _logger.debug('Cannot import pysftp')

class DbBackup(models.Model):
    _inherit = 'db.backup'

    method = fields.Selection(
        [("local", "Local disk"),
         ("sftp", "Remote SFTP server"),
         ("gcloud", "Google cloud storage")],
        default="local",
        help="Choose the storage method for this backup.",
    )
    bucket_name = fields.Char(string="Bucket", help="https://console.cloud.google.com/storage/browser/[bucket-id]/")

    @api.multi
    def sftp_connection(self):
        """Return a new SFTP connection with found parameters."""
        self.ensure_one()
        if self.method != 'gcloud':

            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            params = {
                "host": self.sftp_host,
                "username": self.sftp_user,
                "port": self.sftp_port,
                "cnopts": cnopts,
            }
            _logger.debug(
                "Trying to connect to sftp://%(username)s@%(host)s:%(port)d",
                extra=params)
            if self.sftp_private_key:
                params["private_key"] = self.sftp_private_key
                if self.sftp_password:
                    params["private_key_pass"] = self.sftp_password
            else:
                params["password"] = self.sftp_password

            return pysftp.Connection(**params)
        else:

            client = storage.Client()
            # https://console.cloud.google.com/storage/browser/[bucket-id]/
            bucket = client.get_bucket('kzm')
            return bucket



# from google.cloud import storage
# client = storage.Client()
# # https://console.cloud.google.com/storage/browser/[bucket-id]/
# bucket = client.get_bucket('kzm')
# print(bucket)
# #======= SEND FILE ======
#
# # # Then do other things...
# # blob = bucket.get_blob('remote/path/to/file.txt')
# # print(blob.download_as_string())
# # blob.upload_from_string('New contents!')
# file_to_send = '/home/karizma3/Desktop/test.py'
# blob2 = bucket.blob('BOUGSTONE/ahmed.py')
# blob2.upload_from_filename(filename=file_to_send)
# print(file_to_send, " have been sended !!!!")
# #==========================
#
# blob3 = bucket.get_blob('BOUGSTONE/ahmed.py')
# print("Download from cloud==")
# print(blob3.download_as_string())