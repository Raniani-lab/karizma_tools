# -*- coding: utf-8 -*-

import logging
from fabric import Connection
import base64
import odoorpc
import xmlrpc.client as xmlrpclib
import os
import shutil
import traceback
from contextlib import contextmanager
from datetime import datetime, timedelta
from glob import iglob

from odoo import _, api, exceptions, fields, models, tools
from odoo.exceptions import ValidationError
from odoo.service import db

_logger = logging.getLogger(__name__)


class Instance(models.Model):
    _name = 'kzm.instance'
    _inherit = "mail.thread"

    name = fields.Char(
        compute="_compute_name",
        store=True,
        help="Summary of this backup process",
    )

    folder = fields.Char(
        default=lambda self: self._default_folder(),
        help='Absolute path for storing the backups',
        required=True
    )
    host = fields.Char(string="Host", )
    user = fields.Char(string="User",)
    port = fields.Char("Port", )
    ssh_key = fields.Text(string="SSH Key")

    db_name = fields.Char(string="DB name")
    db_user = fields.Char(string="DB user")
    db_port = fields.Integer(string="DB port")
    password_user_db = fields.Char(string="Password user")
    master_password = fields.Char(string="Master Password")

    method = fields.Selection(
        [("local", "Local disk"), ("sftp", "Remote SFTP server")],
        default="local",
        help="Choose the storage method for this backup.",
    )
    color = fields.Integer(default=6)
    # sftp_host = fields.Char(
    #     'SFTP Server',
    #     help=(
    #         "The host name or IP address from your remote"
    #         " server. For example 192.168.0.1"
    #     )
    # )
    # sftp_port = fields.Integer(
    #     "SFTP Port",
    #     default=22,
    #     help="The port on the FTP server that accepts SSH/SFTP calls."
    # )
    # sftp_user = fields.Char(
    #     'Username in the SFTP Server',
    #     help=(
    #         "The username where the SFTP connection "
    #         "should be made with. This is the user on the external server."
    #     )
    # )
    # sftp_password = fields.Char(
    #     "SFTP Password",
    #     help="The password for the SFTP connection. If you specify a private "
    #          "key file, then this is the password to decrypt it.",
    # )
    # sftp_private_key = fields.Char(
    #     "Private key location",
    #     help="Path to the private key file. Only the Odoo user should have "
    #          "read permissions for that file.",
    # )

    backup_format = fields.Selection(
        [
            ("zip", "zip (includes filestore)"),
            ("dump", "pg_dump custom format (without filestore)"),
            ("sql", "SGBD pg_dump custom format (without filestore)")
        ],
        default='zip',
        help="Choose the format for this backup."
    )

    backup_ids = fields.One2many('kzm.backup', 'instance_id')

    @api.model
    def _default_folder(self):
        """Default to ``backups`` folder inside current server datadir."""
        return os.path.join(
            tools.config["data_dir"],
            "backups",
            self.env.cr.dbname)

    def ssh_connection(self):
        self.ensure_one()

        host = self.host
        user = self.user

        _logger.debug(
            "Trying to connect to %s@%s with SSH" % (user, host),
        )

        connect_kwargs = {'password': self.ssh_key}

        # return Connection(**params)
        return Connection('%s@%s' % (user, host), connect_kwargs=connect_kwargs)

    def action_backup(self):
        backup = None
        for rec in self:
            dbname = rec.db_name
            dbuser = rec.db_user
            host = rec.host
            port = rec.port
            pswd_user = rec.password_user_db
            filename = self.filename(datetime.now(), ext=rec.backup_format)
            with rec.backup_log():
                # Directory must exist
                try:
                    os.makedirs(rec.folder)
                except OSError:
                    pass

                path = os.path.join(rec.folder, filename)
                if rec.backup_format == "sql":
                    try:
                        cnx = rec.ssh_connection()
                        cmd = 'export PGPASSWORD=%s && mkdir -p %s && pg_dump -U %s  %s > %s' % (
                                            pswd_user, rec.folder, dbuser, dbname, path
                        )

                        res = cnx.run(cmd)
                        print(res)
                        self.env['kzm.backup'].create({
                            "name": dbname,
                            "path": path,
                            "date": datetime.now(),
                            "statut": "success",
                            "instance_id": rec.id
                        })

                    except Exception as e:
                        self.env['kzm.backup'].create({
                            "name": dbname,
                            "path": path,
                            "date": datetime.now(),
                            "statut": "failed : "+str(e),
                            "instance_id": rec.id
                        })

                else:

                    try:
                        try:
                            os.makedirs(rec.folder+"/"+rec.db_name)
                        except OSError:
                            pass

                        #path = os.path.join(rec.folder, rec.db_name)
                        path = os.path.join(rec.folder+"/"+rec.db_name, filename)

                        sock = xmlrpclib.ServerProxy('http://' + rec.host + ':' + rec.port + '/xmlrpc/db')
                        all_database = sock.list()
                        print(all_database)
                        backup_file = open(path, 'wb')
                        if rec.db_name in all_database:
                            dump = base64.b64decode(sock.dump(rec.master_password, rec.db_name, rec.backup_format))
                            print (dump)
                            backup_file.write(dump)
                            backup_file.close()
                            self.env['kzm.backup'].create({
                                "name": dbname,
                                "path": path,
                                "date": datetime.now(),
                                "statut": "success",
                                "instance_id": rec.id

                            })
                        else:
                            msg = "No Database named %s in this host." % rec.db_name
                            raise ValidationError(msg)


                    except Exception as e:

                        self.env['kzm.backup'].create({
                            "name": dbname,
                            "path": path,
                            "date": datetime.now(),
                            "statut": "failed : " + str(e),
                            "instance_id": rec.id
                        })


    @api.multi
    @contextmanager
    def backup_log(self):
        """Log a backup result."""
        try:
            _logger.info("Starting database backup: %s", self.name)
            yield
        except Exception:
            _logger.exception("Database backup failed: %s", self.name)
            escaped_tb = tools.html_escape(traceback.format_exc())
            self.message_post(  # pylint: disable=translation-required
                "<p>%s</p><pre>%s</pre>" % (
                    _("Database backup failed."),
                    escaped_tb),
                subtype=self.env.ref(
                    "auto_backup.mail_message_subtype_failure"
                ),
            )
        else:
            _logger.info("Database backup succeeded: %s", self.name)
            self.message_post(_("Database backup succeeded."))

    @staticmethod
    def filename(when, ext='zip'):
        """Generate a file name for a backup.

        :param datetime.datetime when:
            Use this datetime instead of :meth:`datetime.datetime.now`.
        :param str ext: Extension of the file. Default: dump.zip
        """
        return "{:%Y_%m_%d_%H_%M_%S}.{ext}".format(
            when, ext='dump.zip' if ext == 'zip' else ext
        )

    @api.multi
    @api.depends("folder")
    def _compute_name(self):
        """Get the right summary for this job."""
        for rec in self:
            rec.name = "%s/%s" % (rec.folder, rec.db_name)

    def ping(self):
        for rec in self:
            cnx = self.ssh_connection()
            cnx.run("ping %s", self.host)

    @api.multi
    def send_mail_template(self):
        # Find the e-mail template
        template = self.env.ref('kzm_backup.kzm_backup_email_template')

        mail = self.env['mail.template'].browse(template.id)

        print("#######################################")
        print("Mail : ", mail)
        print("#######################################")

        mail.send_mail(self.id)
