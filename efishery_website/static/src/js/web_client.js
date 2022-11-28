odoo.define("efishery_website.WebClient", function (require) {
    "use strict";
    var WebClient = require("web.WebClient");
    var session = require("web.session");
    var Notification = require("web.Notification");
    require("bus.BusService");

    Notification.include({
        icon_mapping: {
            success: "fa-thumbs-up",
            danger: "fa-exclamation-triangle",
            warning: "fa-exclamation",
            info: "fa-info",
            default: "fa-lightbulb-o",
        },
        init: function () {
            this._super.apply(this, arguments);
            this.className = this.className.replace(" o_error", "");
            this.icon =
                this.type in this.icon_mapping
                    ? this.icon_mapping[this.type]
                    : this.icon_mapping.default;
            this.className += " o_" + this.type;
        },
    });

    WebClient.include({
        show_application: function () {
            var res = this._super();
            this.start_polling();
            return res;
        },
        start_polling: function () {
            this.channel_success = "notify_success_" + session.uid;
            this.channel_danger = "notify_danger_" + session.uid;
            this.channel_warning = "notify_warning_" + session.uid;
            this.channel_info = "notify_info_" + session.uid;
            this.channel_default = "notify_default_" + session.uid;
            this.all_channels = [
                this.channel_success,
                this.channel_danger,
                this.channel_warning,
                this.channel_info,
                this.channel_default,
            ];
            this.call("bus_service", "startPolling");

            if (this.call("bus_service", "isMasterTab")) {
                this.call("bus_service", "addChannel", this.channel_success);
                this.call("bus_service", "addChannel", this.channel_danger);
                this.call("bus_service", "addChannel", this.channel_warning);
                this.call("bus_service", "addChannel", this.channel_info);
                this.call("bus_service", "addChannel", this.channel_default);
            }
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