import datetime
import pync
import weechat

SCRIPT_NAME = 'note'
SCRIPT_AUTHOR = 'Sindre Sorhus <sindresorhus@gmail.com>'
SCRIPT_VERSION = '1.3.0'
SCRIPT_LICENSE = 'MIT'
SCRIPT_DESC = 'Message notifications'

note_settings_default = {
    'sound': 'off',
    'sound_name': 'Glass',
    'activate_bundle_id': 'com.apple.Terminal',
    'ignore_old_messages': 'on',
    }

def notify(data, buffer, date, tags, displayed, highlight, prefix, message):
    own_nick = weechat.buffer_get_string(buffer, 'localvar_nick')
    if prefix in (own_nick, '@' + own_nick, '@root'):
        return weechat.WEECHAT_RC_OK

    # ignore messages older than 4 seconds
    if weechat.config_get_plugin('ignore_old_messages') == 'on':
        message_time = datetime.datetime.utcfromtimestamp(int(date))
        now_time = datetime.datetime.utcnow()

        if (now_time - message_time).seconds > 4:
            return weechat.WEECHAT_RC_OK

    # pass lambda to avoid playing default sound
    sound = (weechat.config_get_plugin('sound_name') if
             weechat.config_get_plugin('sound') == 'on' else lambda: None)
    activate_bundle_id = weechat.config_get_plugin('activate_bundle_id')
    pync.notify(message, title='{} [private]'.format(prefix), sound=sound,
                activate=activate_bundle_id)
    return weechat.WEECHAT_RC_OK

if __name__ == '__main__':
    if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
                        SCRIPT_LICENSE, SCRIPT_DESC, '', ''):
        # set default settings
        for key, val in note_settings_default.items():
            if not weechat.config_is_set_plugin(key):
                weechat.config_set_plugin(key, val)

        weechat.hook_print('', 'irc_privmsg', '', 1, 'notify', '')
