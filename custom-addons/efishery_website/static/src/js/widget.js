odoo.define("efishery_website.WebClient", function (require) {
    "use strict";
    var publicWidget = require('web.public.widget');
    var session = require("web.session");
    require("bus.BusService");

    publicWidget.registry.efisheryWidget = publicWidget.Widget.extend({
        selector: '#wrapwrap',
        start: function () {
            var res = this._super();
            this.start_polling();
            return res;
        },
        start_polling: function () {
            if (!session.user_id){
                return
            }
            this.channel_success = "notify_success_" + session.user_id;
            this.channel_danger = "notify_danger_" + session.user_id;
            this.channel_warning = "notify_warning_" + session.user_id;
            this.channel_info = "notify_info_" + session.user_id;
            this.channel_default = "notify_default_" + session.user_id;
            this.all_channels = [
                this.channel_success,
                this.channel_danger,
                this.channel_warning,
                this.channel_info,
                this.channel_default,
            ];
            this.call("bus_service", "startPolling");
            this.call("bus_service", "addChannel", this.channel_success);
            this.call("bus_service", "addChannel", this.channel_danger);
            this.call("bus_service", "addChannel", this.channel_warning);
            this.call("bus_service", "addChannel", this.channel_info);
            this.call("bus_service", "addChannel", this.channel_default);
            this.call("bus_service", "on", "notification", this, this.bus_notification);
        },
        bus_notification: function (notifications) {
            var self = this;
            _.each(notifications, function (notification) {
                var channel = notification[0];
                var message = notification[1];
                if (
                    self.all_channels !== null &&
                    self.all_channels.indexOf(channel) > -1
                ) {
                    self.on_message(message);
                }
            });
        },
        on_message: function (message) {
            return this.call("notification", "notify", {
                type: message.type,
                title: message.title,
                message: message.message,
                sticky: message.sticky,
                className: message.className,
            });
        },
    });
});