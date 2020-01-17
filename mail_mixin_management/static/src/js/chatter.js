 //odoo/addons/mail/static/src/js/chatter.js

 _renderButtons: function () {
        var is_note_adder = false;
        var is_comment_adder = false;
        var is_activity_adder = false;
        var call1 = 0;
        var call2 = 0;
        var call3 = 0;
        console.log("========== Before",is_note_adder,is_comment_adder,is_activity_adder);
        this.getSession()
            .user_has_group('mail_mixin_management.note_managing_user').then(function (hasGroup){
                is_note_adder = hasGroup;
                call1 = 1;
                console.log("========== call1");
        });

        this.getSession()
            .user_has_group('mail_mixin_management.message_managing_user').then(function (hasGroup){
                is_comment_adder = hasGroup;
                call2 = 1;
                console.log("========== call2");
        });

        this.getSession()
            .user_has_group('mail_mixin_management.activity_managing_user').then(function (hasGroup){
                is_activity_adder = hasGroup;
                call3 = 1;
                console.log("========== call3");
        });
      /*  while(true){
            if(call1 && call2 && call3)
                break;
        }*/
        console.log("========== AFTER",is_note_adder,is_comment_adder,is_activity_adder);

        return QWeb.render('mail.chatter.Buttons', {
            newMessageButton: (!!this.fields.thread) && is_comment_adder,
            logNoteButton: (this.hasLogButton) && is_note_adder,
            scheduleActivityButton: (!!this.fields.activity) && is_activity_adder,
            isMobile: config.device.isMobile,
            disableAttachmentBox: this._disableAttachmentBox,
            displayCounter: !!this.fields.thread,
            count: this.record.data.message_attachment_count || 0,
        });
    },